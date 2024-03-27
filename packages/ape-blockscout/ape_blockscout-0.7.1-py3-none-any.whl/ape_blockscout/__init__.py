from ape import plugins

from .config import BlockscoutConfig
from .explorer import Blockscout
from .utils import NETWORKS


@plugins.register(plugins.ExplorerPlugin)
def explorers():
    for ecosystem_name in NETWORKS:
        for network_name in NETWORKS[ecosystem_name]:
            yield ecosystem_name, network_name, Blockscout
            yield ecosystem_name, f"{network_name}-fork", Blockscout


@plugins.register(plugins.Config)
def config_class():
    return BlockscoutConfig
