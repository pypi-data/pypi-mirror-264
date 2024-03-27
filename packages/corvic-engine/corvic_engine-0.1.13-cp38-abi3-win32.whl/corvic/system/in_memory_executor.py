"""Staging-agnostic in-memory executor."""

import pyarrow as pa

from corvic import op_graph, sql
from corvic.system.staging import StagingDB


class InMemoryExecutor:
    """Executes op_graphs in memory (after staging queries)."""

    def __init__(self, staging_db: StagingDB):
        self._staging_db = staging_db

    def _staging_query_generator(self, blob_names: list[str], column_names: list[str]):
        return self._staging_db.query_for_blobs(blob_names, column_names)

    def execute(self, op: op_graph.Op) -> pa.RecordBatchReader:
        query = sql.parse_op_graph(op, self._staging_query_generator)
        return self._staging_db.run_select_query(query)
