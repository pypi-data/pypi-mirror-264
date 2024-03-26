"""Corvic system op graph executeor protocol."""

from typing import Protocol

import pyarrow as pa

from corvic import op_graph


class OpGraphExecutor(Protocol):
    """Execute table op graphs."""

    def execute(self, op: op_graph.Op) -> pa.RecordBatchReader:
        """Execute an op pgraph.

        Render the resulting table as a stream of rows.
        """
        ...
