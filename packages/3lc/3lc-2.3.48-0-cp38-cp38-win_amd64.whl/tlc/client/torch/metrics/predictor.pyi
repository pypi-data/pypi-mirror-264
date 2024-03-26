import torch
from _typeshed import Incomplete
from torch.utils.hooks import RemovableHandle as RemovableHandle
from typing import Any, Sequence

class Predictor:
    """A class which can be used to make predictions on a batch of inputs using a model."""
    hook_outputs: Incomplete
    module_to_layer_index: Incomplete
    layers: Incomplete
    model: Incomplete
    hook_handles: Incomplete
    device: Incomplete
    def __init__(self, model: torch.nn.Module, layers: Sequence[int] | None = None) -> None: ...
    def __call__(self, inputs: Any) -> tuple[list[dict[str, Any]], dict[int, torch.Tensor]]:
        """Call the model on a batch of inputs."""
    def __del__(self) -> None: ...
