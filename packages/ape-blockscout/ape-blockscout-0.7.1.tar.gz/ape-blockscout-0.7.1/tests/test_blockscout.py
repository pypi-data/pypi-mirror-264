import pytest
from ape import config

from ape_blockscout import NETWORKS
from ape_blockscout.exceptions import BlockscoutTooManyRequestsError

# A map of each mock response to its contract name for testing `get_contract_type()`.
EXPECTED_CONTRACT_NAME_MAP = {
    "get_contract_response": "BoredApeYachtClub",
    "get_proxy_contract_response": "MIM-UST-f",
    "get_vyper_contract_response": "yvDAI",
}
TRANSACTION = "0x0da22730986e96aaaf5cedd5082fea9fd82269e41b0ee020d966aa9de491d2e6"
PUBLISH_GUID = "123"

# Every supported ecosystem / network combo as `[("ecosystem", "network") ... ]`
ecosystems_and_networks = [
    p
    for plist in [
        [(e, n) for n in nets] + [(e, f"{n}-fork") for n in nets] for e, nets in NETWORKS.items()
    ]
    for p in plist
]
base_url_test = pytest.mark.parametrize(
    "ecosystem,network,url",
    [
        # Base
        ("base", "mainnet", "base.blockscout.com"),
        ("base", "mainnet-fork", "base.blockscout.com"),
        # Ethereum
        ("ethereum", "mainnet", "eth.blockscout.com"),
        ("ethereum", "mainnet-fork", "eth.blockscout.com"),
        ("ethereum", "goerli", "eth-goerli.blockscout.com"),
        ("ethereum", "goerli-fork", "eth-goerli.blockscout.com"),
        ("ethereum", "sepolia", "eth-sepolia.blockscout.com"),
        ("ethereum", "sepolia-fork", "eth-sepolia.blockscout.com"),
        # Gnosis
        ("gnosis", "mainnet", "gnosis.blockscout.com"),
        ("gnosis", "mainnet-fork", "gnosis.blockscout.com"),
        ("gnosis", "chiado", "gnosis-chiado.blockscout.com"),
        ("gnosis", "chiado-fork", "gnosis-chiado.blockscout.com"),
        # Optimism
        ("optimism", "mainnet", "optimism.blockscout.com"),
        ("optimism", "mainnet-fork", "optimism.blockscout.com"),
        ("optimism", "goerli", "optimism-goerli.blockscout.com"),
        ("optimism", "goerli-fork", "optimism-goerli.blockscout.com"),
        ("optimism", "sepolia", "optimism-sepolia.blockscout.com"),
        ("optimism", "sepolia-fork", "optimism-sepolia.blockscout.com"),
        # Polygon
        ("polygon", "mainnet", "polygon.blockscout.com"),
        ("polygon", "mainnet-fork", "polygon.blockscout.com"),
    ],
)


@base_url_test
def test_get_address_url(ecosystem, network, url, address, get_explorer):
    expected = f"https://{url}/address/{address}"
    explorer = get_explorer(ecosystem, network)
    actual = explorer.get_address_url(address)
    assert actual == expected


@base_url_test
def test_get_transaction_url(ecosystem, network, url, get_explorer):
    expected = f"https://{url}/tx/{TRANSACTION}"
    explorer = get_explorer(ecosystem, network)
    actual = explorer.get_transaction_url(TRANSACTION)
    assert actual == expected


@pytest.mark.parametrize("ecosystem,network", ecosystems_and_networks)
def test_get_contract_type_ecosystems_and_networks(
    mock_backend,
    ecosystem,
    network,
    get_explorer,
):
    # This test parametrizes getting contract types across ecosystem / network combos
    mock_backend.set_network(ecosystem, network)
    response = mock_backend.setup_mock_get_contract_type_response("get_contract_response")
    explorer = get_explorer(ecosystem, network)
    actual = explorer.get_contract_type(response.expected_address)
    contract_type_from_lowered_address = explorer.get_contract_type(
        response.expected_address.lower()
    )
    assert actual is not None
    assert actual == contract_type_from_lowered_address

    actual = actual.name
    expected = EXPECTED_CONTRACT_NAME_MAP[response.file_name]
    assert actual == expected


@pytest.mark.parametrize(
    "file_name", ("get_proxy_contract_response", ("get_vyper_contract_response"))
)
def test_get_contract_type_additional_types(mock_backend, file_name, explorer):
    # This test parametrizes getting edge-case contract types.
    # NOTE: Purposely not merged with test above to avoid adding a new dimension
    #  to the parametrization.
    response = mock_backend.setup_mock_get_contract_type_response(file_name)
    actual = explorer.get_contract_type(response.expected_address).name
    expected = EXPECTED_CONTRACT_NAME_MAP[response.file_name]
    assert actual == expected


def test_get_contract_type_with_rate_limiting(mock_backend, explorer):
    """
    This test ensures the rate limiting logic in the Explorer client works.
    """

    file_name = "get_vyper_contract_response"
    setter_upper = mock_backend.setup_mock_get_contract_type_response_with_throttling
    throttler, response = setter_upper(file_name)

    # We still eventually get the response.
    actual = explorer.get_contract_type(response.expected_address).name
    expected = EXPECTED_CONTRACT_NAME_MAP[response.file_name]
    assert actual == expected
    assert throttler.counter == 2  # Prove that it actually throttled.


def test_too_many_requests_error(no_api_key, response):
    actual = str(BlockscoutTooManyRequestsError(response, "ethereum"))
    assert "BLOCKSCOUT_API_KEY" in actual


@pytest.mark.parametrize("ecosystem", NETWORKS.keys())
def test_config_ecosystem_exists(ecosystem):
    cfg = config.get_config("blockscout")
    assert hasattr(cfg, ecosystem), f"No configuration for ecosystem {ecosystem}"
