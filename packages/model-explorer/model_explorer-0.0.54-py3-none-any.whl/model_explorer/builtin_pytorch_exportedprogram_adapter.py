from typing import Dict

import torch
import torch.fx

from .adapter import Adapter, AdapterMetadata
from .types import AdapterConvertResponse
from .pytorch_exported_program_adater_impl import PytorchExportedProgramAdapterImpl


class BuiltinPytorchExportedProgramAdapter(Adapter):
  """Built-in pytorch adapter using ExportedProgram."""

  metadata = AdapterMetadata(
      id='builtin_pytorch_exportedprogram',
      name='Pytorch adapter (exported program)',
      description=(
          'A built-in adapter that converts a Pytorch exported program to Model'
          ' Explorer format.'
      ),
      fileExts=['pt2'],
  )

  def __init__(self):
    super().__init__()

  def convert(self, model_path: str, settings: Dict) -> AdapterConvertResponse:
    ep = torch.export.load(model_path)
    return PytorchExportedProgramAdapterImpl(ep).convert()
