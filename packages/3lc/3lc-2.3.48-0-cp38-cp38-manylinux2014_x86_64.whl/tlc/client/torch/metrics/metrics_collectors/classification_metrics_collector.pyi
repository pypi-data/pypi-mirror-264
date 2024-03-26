import torch
from _typeshed import Incomplete
from tlc.client.torch.metrics.metrics_collectors.metrics_collector_base import MetricsCollector as MetricsCollector
from tlc.core.builtins.types import MetricData as MetricData, SampleData as SampleData
from tlc.core.schema import Float32Value as Float32Value, Int32Value as Int32Value, Schema as Schema
from typing import Any, Callable

class ClassificationMetricsCollector(MetricsCollector):
    '''Collects classification metrics `loss` and `prediction`.

    This class is a specialized version of `MetricsCollector` and is designed to collect metrics relevant to
    classification problems.

    You can set up data transformation pipelines by using the `transforms`, `transform`, and `target_transform`
    parameters.

    :Example:

    ```python
    model = SomeTorchModel()
    collector = ClassificationMetricsCollector(model)
    ```

    :param model: The PyTorch model for which the metrics are to be collected.
    :param criterion: Unreduced (per-sample) loss function to use for calculating the loss metric. Default is
        `torch.nn.CrossEntropyLoss(reduction="none")`.
    :param predicted_schema: Schema for the predicted output. Can be `None`.
    :param transforms: A callable for common transforms to both input and target. Optional.
    :param transform: A callable for transforming the input data before prediction. Keyword only.
    :param target_transform: A callable for transforming the target data before loss computation. Keyword only.
    '''
    device: Incomplete
    criterion: Incomplete
    predicted_schema: Incomplete
    def __init__(self, model: torch.nn.Module, criterion: Callable[[torch.Tensor, torch.Tensor], torch.Tensor] = ..., predicted_schema: Schema | None = None, compute_aggregates: bool = True) -> None: ...
    def compute_metrics(self, batch: SampleData, predictions: torch.Tensor, _: Any) -> dict[str, MetricData]: ...
    @property
    def column_schemas(self) -> dict[str, Schema]: ...
