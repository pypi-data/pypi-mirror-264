import os
from typing import Dict

from model_explorer_adapter import \
    _pywrap_convert_wrapper as convert_wrapper  # type: ignore

from .adapter import Adapter, AdapterMetadata
from .types import AdapterConvertResponse
from .utils import convert_builtin_resp


class BuiltinTfDirectAdapter(Adapter):
  """Built-in tf adapter by parsing .pb file."""

  metadata = AdapterMetadata(id='builtin_tf_direct',
                             name='TF adapter (direct)',
                             description='A built-in adapter that converts a TF saved model to Model Explorer format by directly parsing the .pb file.',
                             fileExts=['pb'])

  def __init__(self):
    super().__init__()

  def convert(self, model_path: str, settings: Dict) -> AdapterConvertResponse:
    # Construct config.
    config = convert_wrapper.VisualizeConfig()
    if 'const_element_count_limit' in settings:
      config.const_element_count_limit = settings['const_element_count_limit']

    # Normalize model_path
    model_dir = model_path
    if model_path.endswith('.pb'):
      model_dir = os.path.dirname(model_path)
      file_name = os.path.basename(model_path)

      # Rename file to saved_model.pb
      if file_name != 'saved_model.pb':
        os.rename(model_path, os.path.join(model_dir, 'saved_model.pb'))

    # Run
    resp_json_str = convert_wrapper.ConvertSavedModelDirectlyToJson(
        config, model_dir)
    return {'graphCollections': convert_builtin_resp(resp_json_str)}
