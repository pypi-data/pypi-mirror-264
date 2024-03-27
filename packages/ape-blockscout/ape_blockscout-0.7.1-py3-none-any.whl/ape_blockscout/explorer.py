import json
from json.decoder import JSONDecodeError
from typing import Optional

from ape.api import ExplorerAPI
from ape.contracts import ContractInstance
from ape.exceptions import APINotImplementedError, ProviderNotConnectedError
from ape.logging import logger
from ape.types import AddressType, ContractType

from ape_blockscout.client import ClientFactory, get_blockscout_uri


class Blockscout(ExplorerAPI):
    def get_address_url(self, address: str) -> str:
        ecosystem_uri = get_blockscout_uri(
            ecosystem_name=self.network.ecosystem.name,
            network_name=self.network.name.replace("-fork", ""),
        )

        return f"{ecosystem_uri}/address/{address}"

    def get_transaction_url(self, transaction_hash: str) -> str:
        ecosystem_uri = get_blockscout_uri(
            ecosystem_name=self.network.ecosystem.name,
            network_name=self.network.name.replace("-fork", ""),
        )

        return f"{ecosystem_uri}/tx/{transaction_hash}"

    @property
    def _client_factory(self) -> ClientFactory:
        return ClientFactory(
            ecosystem_name=self.network.ecosystem.name,
            network_name=self.network.name.replace("-fork", ""),
        )

    def get_contract_type(self, address: AddressType) -> Optional[ContractType]:
        if not self.conversion_manager.is_type(address, AddressType):
            # Handle non-checksummed addresses
            address = self.conversion_manager.convert(str(address), AddressType)

        client = self._client_factory.get_contract_client(address)

        source_code = client.get_source_code()
        if not (abi_string := source_code.abi):
            return None

        try:
            abi = json.loads(abi_string)
        except JSONDecodeError as err:
            logger.error(f"Error with contract ABI: {err}")
            return None

        contract_type = ContractType(abi=abi, contractName=source_code.name)
        if source_code.name == "Vyper_contract" and "symbol" in contract_type.view_methods:
            try:
                contract = ContractInstance(address, contract_type)
                contract_type.name = contract.symbol() or contract_type.name
            except ProviderNotConnectedError:
                pass

        return contract_type

    def publish_contract(self, address: AddressType):
        raise APINotImplementedError("Publishing contracts is not supported by Blockscout")
