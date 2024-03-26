"""Node2Vec embeddings."""

from __future__ import annotations

import functools
from collections.abc import Mapping
from typing import Any, TypeVar

import numpy as np
import numpy.typing as npt
import polars as pl
from tqdm.auto import trange

from corvic import engine
from corvic.result import BadArgumentError

_MAX_SENTENCE_LEN = 10000

K = TypeVar("K")


class KeyedVectors:
    """Vectors whose entries are keyed by an arbitrary value.

    Used to represent embeddings.
    """

    _vectors: npt.NDArray[np.float32]
    _index_to_key: pl.Series

    def __init__(self, *, dim: int, index_to_key: pl.Series):
        """Create keyed vectors.

        Args:
          dim: dimension of vectors
          key_to_index: mapping of key to index
          index_to_key: mapping of index to key
        """
        self.dim = dim
        self._index_to_key = index_to_key
        self._vectors = self._initial_vectors(len(index_to_key), dim)

    @classmethod
    def _initial_vectors(cls, nrows: int, dim: int):
        rng = np.random.default_rng()
        vectors = rng.random((nrows, dim), dtype=np.float32)
        vectors *= 2.0
        vectors -= 1.0
        vectors /= dim
        return vectors

    def __len__(self):
        """Return the number of keys."""
        return len(self.index_to_key)

    def __getitem__(self, key: Any) -> npt.NDArray[np.float32]:
        """Return vector for key."""
        return self.vectors[self.key_to_index[key]]

    @functools.cached_property
    def key_to_index(self) -> Mapping[str, int]:
        """Return a mapping from keys to index."""
        return {name: i for i, name in enumerate(self._index_to_key)}

    @property
    def index_to_key(self) -> pl.Series:
        """Return a mapping from index to key."""
        return self._index_to_key

    @property
    def vectors(self) -> npt.NDArray[np.float32]:
        """Return raw vectors keyed by index space.

        Use KeyedVectors[key] to retrieve vectors by original key.
        """
        return self._vectors


class Space:
    """A feature space, i.e., a graph."""

    graph: engine.CSRGraph
    _index_to_key: pl.Series

    def __init__(
        self,
        edges: pl.DataFrame,
        *,
        directed: bool = True,
    ):
        """Create a space from a sequence of edges."""
        if len(edges.columns) != 2:  # noqa: PLR2004
            raise BadArgumentError("edges DataFrame should have exactly two columns")

        start_name, end_name = edges.columns[0], edges.columns[1]
        nodes = (
            pl.DataFrame(
                {"id": pl.concat([edges[start_name], edges[end_name]]).unique()}
            )
            .with_row_index()
            .with_columns(pl.col("index").cast(pl.UInt32))
        )

        if len(edges):
            edge_starts_by_index = (
                edges.select([start_name])
                .join(nodes, left_on=start_name, right_on="id", how="left")
                .select(["index"])
                .rename({"index": "start"})
            )
            edge_ends_by_index = (
                edges.select([end_name])
                .join(nodes, left_on=end_name, right_on="id", how="left")
                .select(["index"])
                .rename({"index": "end"})
            )
            edge_array = pl.concat(
                [edge_starts_by_index, edge_ends_by_index], how="horizontal"
            ).to_numpy()
        else:
            edge_array = np.empty((0, 2), dtype=np.uint32)

        self.directed = directed
        self.graph = engine.csr_from_edges(edges=edge_array, directed=directed)
        self._index_to_key = nodes["id"]

    @classmethod
    def _ensure_node(
        cls, key: K, key_to_index: dict[K, int], index_to_key: list[K]
    ) -> int:
        if key not in key_to_index:
            idx = len(index_to_key)
            key_to_index[key] = idx
            index_to_key.append(key)
            return idx
        return key_to_index[key]

    def make_keyed_vectors(self, dim: int) -> KeyedVectors:
        """Make keyed vectors appropriate to the space."""
        return KeyedVectors(dim=dim, index_to_key=self._index_to_key)


class Node2Vec:
    """Node to vector algorithm."""

    _params: engine.Node2VecParams
    _keyed_vectors: KeyedVectors
    _space: Space
    # TODO(ddn): Use seed
    _seed: int | None

    _syn1neg: npt.NDArray[np.float32] | None

    def __init__(  # noqa: PLR0913
        self,
        space: Space,
        dim: int,
        walk_length: int,
        window: int,
        p: float = 1.0,
        q: float = 1.0,
        batch_words: int | None = None,
        alpha: float = 0.025,
        seed: int | None = None,
        workers: int | None = None,
        min_alpha: float = 0.0001,
        negative: int = 5,
    ):
        """Create a new instance of Node2Vec.

        Args:
            space: Graph object whose nodes are to be embedded.
            dim: The dimensionality of the embedding
            walk_length: Length of the random walk to be computed
            window: Size of the window. This is half of the context,
                as the context is all nodes before `window` and
                after `window`.
            p: The higher the value, the lower the probability to return to
                the previous node during a walk.
            q: The higher the value, the lower the probability to return to
                a node connected to a previous node during a walk.
            alpha: Initial learning rate
            min_alpha: Final learning rate
            negative: Number of negative samples
            seed: Random seed
            batch_words: Target size (in nodes) for batches of examples passed
                to worker threads
            workers: Number of threads to use. Default is to select number of threads
                as needed. Setting this to a non-default value incurs additional
                thread pool creation overhead.
        """
        batch_words = batch_words or _MAX_SENTENCE_LEN
        self._params = engine.Node2VecParams(
            p=p,
            q=q,
            start_alpha=alpha,
            end_alpha=min_alpha,
            window=window,
            batch_size=batch_words // (walk_length or 1),
            num_negative=negative,
            max_walk_length=walk_length,
            workers=workers,
        )

        self._space = space
        self._keyed_vectors = space.make_keyed_vectors(dim)

        self._seed = seed
        self._layer1_size = dim

        self._syn1neg = None

        self._syn1neg = np.zeros(
            (len(self._keyed_vectors), self._layer1_size), dtype=np.float32
        )

    def train(
        self,
        *,
        epochs: int,
        verbose: bool = True,
    ):
        """Train the model and compute the node embedding.

        Args:
            epochs: Number of epochs to train the model for.
            verbose: Whether to show loading bar.
        """
        assert self._syn1neg is not None

        for _ in trange(
            epochs,
            dynamic_ncols=True,
            desc="Epochs",
            leave=False,
            disable=not verbose,
        ):
            gen = np.random.Generator(np.random.get_bit_generator())
            next_random = gen.integers(  # pyright: ignore[reportUnknownMemberType]
                np.int32(2**31 - 1), dtype=np.int32
            )
            engine.train_node2vec_epoch(
                graph=self._space.graph,
                params=self._params,
                embeddings=self._keyed_vectors.vectors,
                hidden_layer=self._syn1neg,
                next_random=np.uint64(next_random),
            )

    @property
    def wv(self) -> KeyedVectors:
        """Return computed embeddings."""
        return self._keyed_vectors
