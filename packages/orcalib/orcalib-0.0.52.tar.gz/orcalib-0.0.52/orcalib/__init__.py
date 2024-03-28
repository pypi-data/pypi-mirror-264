from typing import Any, Optional

from orca_common import TableCreateMode
from orcalib.database import with_default_database_method
from pandas import DataFrame

from .batched_scan_result import BatchedScanResult
from .client import OrcaClient
from .data_classes import VectorScanResult
from .database import OrcaDatabase
from .exceptions import OrcaException, OrcaNotFoundException
from .file_ingestor import (
    CSVIngestor,
    JSONIngestor,
    JSONLIngestor,
    ParquetIngestor,
    PickleIngestor,
)
from .hf_utils import HFAutoModelWrapper, HFDatasetIngestor
from .index_handle import IndexHandle
from .index_query import DefaultIndexQuery, VectorIndexQuery
from .orca_expr import ColumnHandle, OrcaExpr
from .orca_types import (
    BFloat16T,
    BoolT,
    DocumentT,
    EnumT,
    Float16T,
    Float32T,
    Float64T,
    FloatT,
    ImageT,
    Int8T,
    Int16T,
    Int32T,
    Int64T,
    IntT,
    NumericTypeHandle,
    OrcaTypeHandle,
    TextT,
    UInt8T,
    UInt16T,
    UInt32T,
    UInt64T,
    VectorT,
)
from .table import TableHandle
from .temp_database import TemporaryDatabase, TemporaryTable


def set_credentials(*, api_key: str, secret_key: str, endpoint: Optional[str] = None) -> None:
    """
    Set the credentials for the Orca client. This must be called before any other Orca functions. This can also be
    called multiple times to change the credentials.
    :param api_key: API key
    :param secret_key: Secret key
    :param endpoint: Endpoint (optional)

    example:
    >>> import orcalib as orca
    >>> orca.set_credentials(api_key, secret_key)
    """
    OrcaClient.set_credentials(api_key=api_key, secret_key=secret_key, endpoint=endpoint)


@with_default_database_method
def create_table(
    db: OrcaDatabase,
    table_name: str,
    if_table_exists: TableCreateMode = TableCreateMode.ERROR_IF_TABLE_EXISTS,
    **columns: OrcaTypeHandle,
) -> TableHandle:
    """
    Create a table in the default database. This is a convenience function that calls `create_table` on the default db.
    :param table_name: Name of the table
    :param if_table_exists: What to do if the table already exists (default: TableCreateMode.ERROR_IF_TABLE_EXISTS)
    :param columns: Columns of the table (name -> type mapping)
    :return: TableHandle

    example:
    >>> import orcalib as orca
    >>> orca.create_table("my_table", id=orca.Int64T, name=orca.TextT)
    """
    return db.create_table(table_name, if_table_exists, **columns)


@with_default_database_method
def get_table(db: OrcaDatabase, table_name: str) -> TableHandle:
    """
    Get a table from the default database. This is a convenience function that calls `get_table` on the default db.
    :param table_name: Name of the table
    :return: TableHandle

    example:
    >>> import orcalib as orca
    >>> orca.get_table("my_table")
    """
    return db.get_table(table_name)


@with_default_database_method
def list_tables(db: OrcaDatabase) -> list[str]:
    """
    List tables in the default database. This is a convenience function that calls `list_tables` on the default db.
    :return: List of table names

    example:
    >>> import orcalib as orca
    >>> orca.list_tables()
    """
    return db.list_tables()


@with_default_database_method
def backup(db: OrcaDatabase) -> tuple[str, str]:
    """
    Backup the default database. This is a convenience function that calls `backup` on the default db.
    :return: Backup path and backup name

    example:
    >>> import orcalib as orca
    >>> orca.backup()
    """
    return db.backup()


@with_default_database_method
def default_vectorize(db: OrcaDatabase, text: str) -> list[float]:
    """
    Vectorize text using the default database. This is a convenience function that calls `default_vectorize` on the default db.
    :param text: Text to vectorize
    :return: Vector

    example:
    >>> import orcalib as orca
    >>> orca.default_vectorize("hello world")
    """
    return db.default_vectorize(text)


@with_default_database_method
def get_index(db: OrcaDatabase, index_name: str) -> IndexHandle:
    """
    Get an index from the default database. This is a convenience function that calls `get_index` on the default db.
    :param index_name: Name of the index
    :return: IndexHandle

    example:
    >>> import orcalib as orca
    >>> orca.get_index("my_index")
    """
    return db.get_index(index_name)


@with_default_database_method
def create_vector_index(
    db: OrcaDatabase,
    index_name: str,
    table_name: str,
    column: str,
    error_if_exists: bool = True,
) -> None:
    """
    Create a vector index for default db. This is a convenience function that calls `create_vector_index` on the default db.
    :param index_name: Name of the index
    :param table_name: Name of the table
    :param column: Name of the column
    :param error_if_exists: Whether to raise an error if the index already exists (default: True)

    example:
    >>> import orcalib as orca
    >>> orca.create_vector_index("my_index", "my_table", "my_column")
    """
    db.create_vector_index(index_name, table_name, column, error_if_exists)


@with_default_database_method
def create_document_index(
    db: OrcaDatabase,
    index_name: str,
    table_name: str,
    column: str,
    error_if_exists: bool = True,
) -> None:
    """
    Create a document index for default db. This is a convenience function that calls `create_document_index` on the default db.
    :param index_name: Name of the index
    :param table_name: Name of the table
    :param column: Name of the column
    :param error_if_exists: Whether to raise an error if the index already exists (default: True)

    example:
    >>> import orcalib as orca
    >>> orca.create_document_index("my_index", "my_table", "my_column")
    """
    db.create_document_index(index_name, table_name, column, error_if_exists)


@with_default_database_method
def create_text_index(
    db: OrcaDatabase,
    index_name: str,
    table_name: str,
    column: str,
    error_if_exists: bool = True,
) -> None:
    """
    Create a text index for default db. This is a convenience function that calls `create_text_index` on the default db.
    :param index_name: Name of the index
    :param table_name: Name of the table
    :param column: Name of the column
    :param error_if_exists: Whether to raise an error if the index already exists (default: True)

    example:
    >>> import orcalib as orca
    >>> orca.create_text_index("my_index", "my_table", "my_column")
    """
    db.create_text_index(index_name, table_name, column, error_if_exists)


@with_default_database_method
def create_btree_index(
    db: OrcaDatabase,
    index_name: str,
    table_name: str,
    column: str,
    error_if_exists: bool = True,
) -> None:
    """
    Create a btree index for default db. This is a convenience function that calls `create_btree_index` on the default db.
    :param index_name: Name of the index
    :param table_name: Name of the table
    :param column: Name of the column
    :param error_if_exists: Whether to raise an error if the index already exists (default: True)

    example:
    >>> import orcalib as orca
    >>> orca.create_btree_index("my_index", "my_table", "my_column")
    """
    db.create_btree_index(index_name, table_name, column, error_if_exists)


@with_default_database_method
def drop_index(db: OrcaDatabase, index_name: str, error_if_not_exists: bool = True) -> None:
    """
    Drop an index from the default database. This is a convenience function that calls `drop_index` on the default db.
    :param index_name: Name of the index
    :param error_if_not_exists: Whether to raise an error if the index does not exist (default: True)

    example:
    >>> import orcalib as orca
    >>> orca.drop_index("my_index")
    """
    db.drop_index(index_name, error_if_not_exists)


@with_default_database_method
def drop_table(db: OrcaDatabase, table_name: str, error_if_not_exists: bool = True) -> None:
    """
    Drop a table from the default database. This is a convenience function that calls `drop_table` on the default db.
    :param table_name: Name of the table
    :param error_if_not_exists: Whether to raise an error if the table does not exist (default: True)

    example:
    >>> import orcalib as orca
    >>> orca.drop_table("my_table")
    """
    db.drop_table(table_name, error_if_not_exists)


@with_default_database_method
def search_memory(
    db: OrcaDatabase,
    index_name: str,
    query: list[float],
    limit: int,
    columns: Optional[list[str]] = None,
) -> Any:
    """
    Search memory for default db. This is a convenience function that calls `search_memory` on the default db.
    :param index_name: Name of the index
    :param query: Query
    :param limit: Limit
    :param columns: Columns to return (optional)

    example:
    >>> import orcalib as orca
    >>> orca.search_memory("my_index", [1.0, 2.0], 10)
    """
    return db.search_memory(index_name, query, limit, columns)


@with_default_database_method
def scan_index(
    db: OrcaDatabase,
    index_name: str,
    query: Any,
) -> DefaultIndexQuery:
    """
    Scan an index for default db. This is a convenience function that calls `scan_index` on the default db.
    :param index_name: Name of the index
    :param query: Query
    :return: DefaultIndexQuery

    example:
    >>> import orcalib as orca
    >>> orca.scan_index("my_index", orca.OrcaExpr("$EQ", (orca.ColumnHandle("my_table", "my_column"), 42)))
    """
    return db.scan_index(index_name, query)


@with_default_database_method
def vector_scan_index(
    db: OrcaDatabase,
    index_name: str,
    query: Any,
) -> VectorIndexQuery:
    """
    Scan a vector index for default db. This is a convenience function that calls `vector_scan_index` on the default db.
    :param index_name: Name of the index
    :param query: Query
    :return: VectorIndexQuery

    example:
    >>> import orcalib as orca
    >>> orca.vector_scan_index("my_index", orca.OrcaExpr("$EQ", (orca.ColumnHandle("my_table", "my_column"), 42)))
    """
    return db.vector_scan_index(index_name, query)


@with_default_database_method
def full_vector_memory_join(
    db: OrcaDatabase,
    *,
    index_name: str,
    memory_index_name: str,
    num_memories: int,
    query_columns: list[str],
    page_index: int,
    page_size: int,
) -> dict[str, list[tuple[list[float], Any]]]:
    """
    Join a vector index with a memory index for default db. This is a convenience function that calls `full_vector_memory_join` on the default db.
    :param index_name: Name of the index
    :param memory_index_name: Name of the memory index
    :param num_memories: Number of memories
    :param query_columns: Query columns
    :param page_index: Page index
    :param page_size: Page size
    :return: Results

    example:
    >>> import orcalib as orca
    >>> orca.full_vector_memory_join("my_index", "my_memory_index", 10, ["my_column"], 0, 10)
    """
    return db.full_vector_memory_join(index_name, memory_index_name, num_memories, query_columns, page_index, page_size)


@with_default_database_method
def query(db: OrcaDatabase, query: str, params: list[None | int | float | bytes | str] = []) -> DataFrame:
    """
    Execute a raw SQL query. This is a convenience function that calls `query` on the default db.
    :param query: Query
    :param params: Parameters (optional)
    :return: DataFrame

    example:
    >>> import orcalib as orca
    >>> orca.query("SELECT * FROM my_table")
    """
    return db.query(query, params)


@with_default_database_method
def record_model_scores(db: OrcaDatabase, run_ids: list[int] | int, scores: list[float] | float) -> None:
    """
    Record model scores in the default database. This is a convenience function that calls `record_model_scores` on the default db.
    :param run_ids: Run IDs
    :param scores: Scores (list of floats or a single float)

    example:
    >>> import orcalib as orca
    >>> orca.record_model_scores(1, 0.5)
    """
    db.record_model_scores(run_ids, scores)


@with_default_database_method
def record_model_input_output(
    db: OrcaDatabase, run_ids: list[int] | int, inputs: list[Any] | Any, outputs: list[Any] | Any
) -> None:
    """
    Record model inputs and outputs in the default database. This is a convenience function that calls `record_model_input_output` on the default db.
    :param run_ids: Run IDs
    :param inputs: Inputs
    :param outputs: Outputs

    example:
    >>> import orcalib as orca
    >>> orca.record_model_input_output(1, "input", "output")
    """
    db.record_model_input_output(run_ids, inputs, outputs)
