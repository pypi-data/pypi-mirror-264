import json
from dataclasses import asdict
from typing import Any, Union

from .types import GraphCollection, AdapterConvertResponse


def get_instance_method(instance: object, fn_name: str) -> Union[Any, None]:
  """Gets the given method from the given class instance."""
  method = getattr(instance, fn_name, None)
  if not callable(method):
    return None
  return method


def convert_builtin_resp(resp_json_str: str) -> list[GraphCollection]:
  """Converts the json string response from the built-in adapters."""
  resp = json.loads(resp_json_str)
  return [GraphCollection(label=item['label'],
                          graphs=item['subgraphs']) for item in resp]


def convert_adapter_response(resp: AdapterConvertResponse):
  """Converts the given adapter convert response to python object."""
  if 'graphs' in resp:
    return {'graphs':
            [asdict(x) for x in resp['graphs']]}
  if 'graphCollections' in resp:
    return {'graphCollections':
            [asdict(x) for x in resp['graphCollections']]}
