import torch
from _typeshed import Incomplete
from tlc.client.helpers import active_run as active_run
from tlc.client.sample_type import SegmentationPILImage as SegmentationPILImage
from tlc.client.torch.metrics.metrics_collectors.metrics_collector_base import MetricsCollector as MetricsCollector
from tlc.core.builtins.types import MetricData as MetricData, SampleData as SampleData
from tlc.core.schema import Schema as Schema
from tlc.core.url import Url as Url
from typing import Callable

BASE_PREDICTION_FOLDER: str

class SegmentationMetricsCollector(MetricsCollector):
    """Collects predicted mask from model.

    This class is a specialized version of `MetricsCollector` and is designed to collect metrics relevant to
    segmentation mask problems.

    :param segmentation_model: The PyTorch model for which the metrics are to be collected.
    :param id2label: A dictionary mapping class ids to class labels.
    :param post_process_function: Function used to post process inference.
    :param example_id_start: The starting index for the example id. Default is 0.
    :param predictions_folder_location: The location where the predictions are to be stored. Default is inside the run
    :param compute_aggregates: Whether to compute aggregates for the collected metrics. Default is True.
    """
    segmentation_model: Incomplete
    id2label: Incomplete
    post_process_function: Incomplete
    device: Incomplete
    example_id_start: Incomplete
    predictions_folder_location: Incomplete
    def __init__(self, segmentation_model: torch.nn.Module, id2label: dict[int, str], post_process_function: Callable[..., list[torch.Tensor]], example_id_start: int = 0, predictions_folder_location: str | Url | None = None, compute_aggregates: bool = True) -> None: ...
    def compute_metrics(self, batch: SampleData, predictions: SampleData | None = None, hook_outputs: dict[int, torch.Tensor] | None = None) -> dict[str, MetricData]: ...
    @property
    def column_schemas(self) -> dict[str, Schema]: ...
