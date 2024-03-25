from typing import ClassVar, Dict, Tuple, cast

from ape_ethereum.ecosystem import (
    BaseEthereumConfig,
    Ethereum,
    NetworkConfig,
    create_network_config,
)

NETWORKS = {
    # chain_id, network_id
    "mainnet": (369, 369),
    "testnet_v4": (943, 943),
}


class PulseChainConfig(BaseEthereumConfig):
    NETWORKS: ClassVar[Dict[str, Tuple[int, int]]] = NETWORKS
    mainnet: NetworkConfig = create_network_config(block_time=2, required_confirmations=1)
    mumbai: NetworkConfig = create_network_config(block_time=2, required_confirmations=1)


class PulseChain(Ethereum):
    fee_token_symbol: str = "PLS"

    @property
    def config(self) -> PulseChainConfig:  # type: ignore[override]
        return cast(PulseChainConfig, self.config_manager.get_config("pulsechain"))
