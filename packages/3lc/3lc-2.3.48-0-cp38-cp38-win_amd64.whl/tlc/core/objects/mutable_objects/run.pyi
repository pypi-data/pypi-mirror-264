from _typeshed import Incomplete
from tlc.core.builtins.constants.column_names import EXAMPLE_ID as EXAMPLE_ID, FOREIGN_TABLE_ID as FOREIGN_TABLE_ID, RUN_STATUS as RUN_STATUS, RUN_STATUS_CANCELLED as RUN_STATUS_CANCELLED, RUN_STATUS_COLLECTING as RUN_STATUS_COLLECTING, RUN_STATUS_COMPLETED as RUN_STATUS_COMPLETED, RUN_STATUS_EMPTY as RUN_STATUS_EMPTY, RUN_STATUS_PAUSED as RUN_STATUS_PAUSED, RUN_STATUS_POST_PROCESSING as RUN_STATUS_POST_PROCESSING, RUN_STATUS_RUNNING as RUN_STATUS_RUNNING
from tlc.core.builtins.constants.string_roles import STRING_ROLE_URL as STRING_ROLE_URL
from tlc.core.builtins.schemas import ExampleIdSchema as ExampleIdSchema, ForeignTableIdSchema as ForeignTableIdSchema
from tlc.core.builtins.types import MetricData as MetricData, MetricTableInfo as MetricTableInfo
from tlc.core.object import Object as Object
from tlc.core.object_registry import ObjectRegistry as ObjectRegistry
from tlc.core.object_type_registry import ObjectTypeRegistry as ObjectTypeRegistry
from tlc.core.objects.mutable_object import MutableObject as MutableObject
from tlc.core.objects.table import Table as Table
from tlc.core.schema import DictValue as DictValue, DimensionNumericValue as DimensionNumericValue, Float64Value as Float64Value, Int64Value as Int64Value, MapElement as MapElement, Schema as Schema, StringValue as StringValue
from tlc.core.url import Url as Url
from tlc.core.utils.object_lock import tlc_object_lock as tlc_object_lock
from typing import Any, Literal

logger: Incomplete

class Run(MutableObject):
    """A collection of metadata about a run."""
    description: Incomplete
    project_name: Incomplete
    metrics: Incomplete
    constants: Incomplete
    status: Incomplete
    def __init__(self, url: Url | None = None, created: str | None = None, last_modified: str | None = None, description: str | None = None, metrics: list[dict[str, Any]] | None = None, constants: dict[str, Any] | None = None, status: float | None = None, init_parameters: Any = None) -> None: ...
    def copy(self, run_name: str | None = None, project_name: str | None = None, root_url: Url | str | None = None, if_exists: Literal['raise', 'rename', 'overwrite'] = 'raise', *, destination_url: Url | None = None) -> Run:
        """Create a copy of this run.

        The copy is performed to:
          1. A URL derived from the given run_name, project_name, and root_url if given
          2. destination_url, if given
          3. A generated URL derived from the run's URL, if none of the above are given

        :param run_name: The name of the run to create.
        :param project_name: The name of the project to create the run in.
        :param root_url: The root URL to create the run in.
        :param if_exists: What to do if the destination URL already exists.
        :param destination_url: The URL to copy the run to.
        :return: The copied run.
        """
    @staticmethod
    def add_run_properties_to_schema(schema: Schema, include_url: bool, include_last_modified: bool, include_is_url_writable: bool) -> None:
        """
        Adds the properties for a Run to a schema
        """
    def add_input_table(self, input_table: Table | Url | str) -> None:
        """Adds an input table to the run.

        This updates the Run object to include the input table in the list of inputs to the Run.

        :param input_table: The input table to add.
        """
    def add_input_value(self, input_value: dict[str, Any]) -> None:
        """Adds a value to the inputs of the run.

        :param input_value: The value to add.
        """
    def add_output_value(self, output_value: dict[str, Any]) -> None:
        """Adds a value to the outputs of the run.

        :param output_value: The value to add.
        """
    def set_parameters(self, parameters: dict[str, Any]) -> None:
        """Set the parameters of the run.

        :param parameters: The parameters to set.
        """
    def set_description(self, description: str) -> None:
        """Set the description of the run.

        :param description: The description to set.
        """
    @classmethod
    def from_url(cls, url: Url | str) -> Run:
        """Creates a Run object from a URL.

        :param url: The URL to the Run object.

        :return: The Run object.
        """
    @property
    def metrics_tables(self) -> list[Table]:
        """
        Returns a list of the metrics tables for this run.
        """
    def reduce_embeddings_by_foreign_table_url(self, foreign_table_url: Url, delete_source_tables: bool = False, **kwargs: Any) -> dict[Url, Url]:
        """Reduces all metrics tables in a Run using a reducer trained on the embeddings in a specified metrics table.

        See
        {func}`tlc.reduce_embeddings_by_foreign_table_url<tlc.client.reduce.reduce.reduce_embeddings_by_foreign_table_url>`
        for more information.

        :param foreign_table_url: The Url of the foreign table to use for reduction.
        :param delete_source_tables: If True, the source metrics tables will be deleted after reduction.

        :returns: A dictionary mapping the original table URLs to the reduced table URLs.
        """
    def reduce_embeddings_per_dataset(self, delete_source_tables: bool = False, **kwargs: Any) -> dict[Url, Url]:
        """
        Reduces the embeddings for each dataset in this run.

        See
        {func}`tlc.reduce_embeddings_per_dataset<tlc.client.reduce.reduce.reduce_embeddings_per_dataset>`
        for more information.

        :param delete_source_tables: If True, the source metrics tables will be deleted after reduction.

        :returns: A dictionary mapping the original table URLs to the reduced table URLs.
        """
    def update_metrics_table_urls(self, url_mapping: dict[Url, Url]) -> None:
        """Replace metrics table URLs in this run with the new table URLs.

        :param url_mapping: A dictionary mapping the original table URLs to the new table URLs.
        """
    def update_metric_table_infos(self, metric_infos: list[MetricTableInfo], url_mapping: dict[Url, Url]) -> list[MetricTableInfo]:
        """Update metrics table with new URL, file size, and row count details.

        :param metric_infos: A list of MetricTableInfo dicts.
        :param url_mapping: A dictionary mapping the original table URLs to the new table URLs.

        :returns: A list of updated MetricTableInfo dicts.
        """
    def update_metrics(self, metric_infos: list[MetricTableInfo] = []) -> None:
        """Update the metrics field of a run."""
    def add_metrics_data(self, metrics: dict[str, MetricData], override_column_schemas: dict[str, Schema] = {}, input_table_url: Url | str | None = None, table_writer_base_name: str = 'metrics', stream_name: str = '') -> list[MetricTableInfo]:
        """Write the given metrics to a Table and updates the run with the table info.

        :param metrics: The metrics data (dict of column-names to columns) to write.
        :param override_column_schemas: A dictionary of schemas to override the default schemas for the columns.
        :param input_table_url: The URL of the table used to generate the metrics data. If provided, the metrics data
            will be augmented with extra columns to identify the example id and example table. Should only be provided
            if the metrics data corresponds 1-1 with the rows in the table.
        :param table_writer_base_name: The base name of the written tables.
        :param table_writer_key: A key used to further identify the written tables.

        :returns: The written table infos.

        :raises ValueError: If the number of rows in the metrics data does not match the number of rows in the table,
            or the input_table_url is not a valid URL.
        :raises FileNotFoundError: If the input_table_url can not be found.
        """
