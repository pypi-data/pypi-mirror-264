from importlib.metadata import version

from .adapter import Adapter, AdapterMetadata
from .consts import PACKAGE_NAME
from .graph import Graph, GraphNode, IncomingEdge
from .server import start
from . import pytorch

# Default 'exports'.
#
# This allow users to do:
#
# import model_explorer
# model_explorer.start()
__all__ = ['start', 'Adapter', 'AdapterMetadata',
           'Graph', 'GraphNode', 'IncomingEdge', 'pytorch']

__version__ = version(PACKAGE_NAME)
