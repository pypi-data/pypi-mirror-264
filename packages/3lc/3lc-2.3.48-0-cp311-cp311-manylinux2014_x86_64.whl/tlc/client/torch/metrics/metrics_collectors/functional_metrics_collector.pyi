import torch
from _typeshed import Incomplete
from tlc.client.torch.metrics.metrics_collectors.metrics_collector_base import MetricsCollector as MetricsCollector
from tlc.core.builtins.types import SampleData as SampleData
from tlc.core.schema import Schema as Schema
from typing import Any, Callable

class FunctionalMetricsCollector(MetricsCollector):
    """A metrics collector which uses a function to collect metrics.

    :param collection_fn: A function which takes a batch of inputs, a batch of predictions, and a dictionary of hook
        outputs and returns a dictionary of metrics.
    :param column_schemas: A dictionary of schemas for the columns. If no schemas are provided, the schemas will be
        inferred from the columns.
    :param model: The model to use when collecting metrics.
    """
    device: Incomplete
    def __init__(self, collection_fn: Callable[[Any, Any, Any], dict[str, Any]], column_schemas: dict[str, Schema] | None = None, model: Any | None = None, compute_aggregates: bool = True) -> None: ...
    def compute_metrics(self, batch: SampleData, predictions: SampleData | None = None, hook_outputs: dict[int, torch.Tensor] | None = None) -> dict[str, Any]: ...
    @property
    def column_schemas(self) -> dict[str, Schema]: ...
