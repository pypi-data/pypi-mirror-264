from typing import Any, Callable, Tuple

import torch

from .pytorch_exported_program_adater_impl import \
    PytorchExportedProgramAdapterImpl
from .types import AdapterConvertResponse


def convert(model: Callable, inputs: Tuple[Any, ...]) -> AdapterConvertResponse:
  """Converts the given pytorch model with inputs into model explorer format."""
  exported = torch.export.export(model, inputs)
  adapter = PytorchExportedProgramAdapterImpl(exported)
  return adapter.convert()
