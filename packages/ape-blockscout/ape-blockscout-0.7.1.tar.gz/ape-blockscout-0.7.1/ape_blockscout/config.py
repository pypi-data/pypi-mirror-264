from ape.api.config import PluginConfig


class EcosystemConfig(PluginConfig):
    rate_limit: int = 5  # Requests per second
    retries: int = 5  # Number of retries before giving up


class BlockscoutConfig(PluginConfig):
    base: EcosystemConfig = EcosystemConfig()
    ethereum: EcosystemConfig = EcosystemConfig()
    gnosis: EcosystemConfig = EcosystemConfig()
    optimism: EcosystemConfig = EcosystemConfig()
    polygon: EcosystemConfig = EcosystemConfig()
