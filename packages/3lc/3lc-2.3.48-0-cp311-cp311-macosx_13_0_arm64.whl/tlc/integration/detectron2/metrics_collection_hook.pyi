from _typeshed import Incomplete
from detectron2.config import CfgNode as CfgNode
from detectron2.engine.hooks import HookBase
from tlc.client.torch.metrics import MetricsCollector as MetricsCollector
from tlc.client.torch.metrics.collect_dataset import collect_metrics as collect_metrics
from tlc.core.builtins.schemas.schemas import EpochSchema as EpochSchema, IterationSchema as IterationSchema
from torch.utils.data import DataLoader as DataLoader

logger: Incomplete

class MetricsCollectionHook(HookBase):
    """Hook that collects 3LC metrics on a detectron dataset.

    :param dataset_name: The name of the dataset to collect metrics on.
            This name should be registered in the MetadataCatalog.
    :param metrics_collectors: The metrics collectors to use.
    :param cfg: The detectron config. If None, the config will be loaded from the trainer.
    :param collection_start_iteration: The iteration to start collecting metrics on.
    :param collection_frequency: The frequency with which to collect metrics.
    :param collect_metrics_before_train: Whether to collect metrics at the beginning of training.
    :param collect_metrics_after_train: Whether to collect metrics at the end of training.
    :param metric_collection_batch_size: The batch size to use for collecting metrics.
    """
    def __init__(self, dataset_name: str, metrics_collectors: list[MetricsCollector], cfg: CfgNode | None = None, collection_start_iteration: int = 0, collection_frequency: int = -1, collect_metrics_before_train: bool = False, collect_metrics_after_train: bool = False, metric_collection_batch_size: int = 8) -> None: ...
    def before_train(self) -> None:
        """Creates a test-dataloader from the trainer and collects metrics if required."""
    def after_train(self) -> None:
        """Collects metrics if required."""
    def before_step(self) -> None: ...
    def after_step(self) -> None:
        """Collects 3LC metrics at regular intervals."""
