import torch
from _typeshed import Incomplete
from tlc.client.torch.metrics.metrics_collectors.metrics_collector_base import MetricsCollector as MetricsCollector
from tlc.core.builtins.constants.number_roles import NUMBER_ROLE_NN_EMBEDDING as NUMBER_ROLE_NN_EMBEDDING
from tlc.core.builtins.types import MetricData as MetricData, SampleData as SampleData
from tlc.core.schema import DimensionNumericValue as DimensionNumericValue, Float32Value as Float32Value, Schema as Schema
from typing import Callable

logger: Incomplete

class EmbeddingsMetricsCollector(MetricsCollector):
    '''Metrics collector that prepares NN-embeddings for storage.

    Returns metrics batches with a column named "embeddings_{layer}" for each layer in the model.
    The outputs of intermediate model modules could have arbitrary shapes, but in order to write them to a table,
    they must be reshaped to 1D arrays (flattened).

    Will ensure all layers are flattened according to `reshape_strategy[layer]`.
    '''
    def __init__(self, model: torch.nn.Module, layers: list[int], reshape_strategy: dict[int, str] | dict[int, Callable[[torch.Tensor], torch.Tensor]] | None = None) -> None:
        '''Create a new embeddings metrics collector.

        :param model: The model to collect embeddings from.
        :param layers: The layers to collect embeddings from.
        :param reshape_strategy: The reshaping strategy to use for each layer.
            Can be either "mean", which takes the mean across all non-first dimensions (excluding batch dimension),
            or "flatten", which flattens all dimensions after the batch dimension.
            Could also be a callable which performs the flattening.
        '''
    def compute_metrics(self, _1: SampleData, _2: SampleData | None = None, hook_outputs: dict[int, torch.Tensor] | None = None) -> dict[str, MetricData]:
        """Collect large NN-embeddings from pytorch models.

        :param hook_outputs: The outputs from the model hooks.
        :returns: A dictionary of column names to batch of flattened embeddings.
        """
    @property
    def column_schemas(self) -> dict[str, Schema]: ...
