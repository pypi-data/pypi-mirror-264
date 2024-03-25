from ape_ethereum.transactions import TransactionType

from ape_pulsechain.ecosystem import PulseChainConfig


def test_gas_limit(pulsechain):
    assert pulsechain.config.local.gas_limit == "max"


def test_default_transaction_type(pulsechain):
    assert pulsechain.config.mainnet.default_transaction_type == TransactionType.DYNAMIC


def test_mainnet_fork_not_configured():
    obj = PulseChainConfig.model_validate({})
    assert obj.mainnet_fork.required_confirmations == 0


def test_mainnet_fork_configured():
    data = {"mainnet_fork": {"required_confirmations": 555}}
    obj = PulseChainConfig.model_validate(data)
    assert obj.mainnet_fork.required_confirmations == 555


def test_custom_network():
    data = {"apenet": {"required_confirmations": 333}}
    obj = PulseChainConfig.model_validate(data)
    assert obj.apenet.required_confirmations == 333
