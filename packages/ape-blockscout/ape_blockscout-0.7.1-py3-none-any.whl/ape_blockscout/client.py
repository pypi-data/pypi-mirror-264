import json
import os
import random
import time
from io import StringIO
from typing import Dict, Iterator, List, Optional

from ape.logging import logger
from ape.utils import USER_AGENT, ManagerAccessMixin
from requests import Session
from yarl import URL

from ape_blockscout.exceptions import (
    UnhandledResultError,
    UnsupportedEcosystemError,
    UnsupportedNetworkError,
)
from ape_blockscout.types import BlockscoutResponse, ContractCreationResponse, SourceCodeResponse
from ape_blockscout.utils import API_KEY_ENV_KEY_MAP, NETWORKS


def get_blockscout_uri(ecosystem_name: str, network_name: str) -> str:
    if ecosystem_name not in API_KEY_ENV_KEY_MAP.keys():
        raise UnsupportedEcosystemError(ecosystem_name)

    if network_name not in NETWORKS[ecosystem_name]:
        raise UnsupportedNetworkError(ecosystem_name, network_name)

    # Blockscout uses "eth" for ethereum, but we use "ethereum" in ape.
    ecosystem_name = "eth" if ecosystem_name == "ethereum" else ecosystem_name

    path_name = ecosystem_name if network_name == "mainnet" else f"{ecosystem_name}-{network_name}"

    return f"https://{path_name}.blockscout.com"


class _APIClient(ManagerAccessMixin):
    DEFAULT_HEADERS = {"User-Agent": USER_AGENT}
    session: Session = Session()
    ecosystem_name: str

    def __init__(self, ecosystem_name: str, network_name: str, module_name: str):
        self._ecosystem_name = ecosystem_name
        self._network_name = network_name
        self._module_name = module_name
        self._last_call = 0.0

    @property
    def base_uri(self) -> str:
        return get_blockscout_uri(self._ecosystem_name, self._network_name) + "/api"

    @property
    def base_params(self) -> Dict:
        return {"module": self._module_name}

    @property
    def _rate_limit(self) -> int:
        config = self.config_manager.get_config("blockscout")
        return getattr(config, self.network_manager.ecosystem.name.lower()).rate_limit

    @property
    def _retries(self) -> int:
        config = self.config_manager.get_config("blockscout")
        return getattr(config, self.network_manager.ecosystem.name.lower()).retries

    @property
    def _min_time_between_calls(self) -> float:
        return 1 / self._rate_limit  # seconds / calls per second

    @property
    def _clean_uri(self) -> str:
        url: URL = URL(self.base_uri).with_user(None).with_password(None)
        return f"{url.with_path('')}/[hidden]" if url.path else f"{url}"

    def _get(
        self,
        params: Optional[Dict] = None,
        headers: Optional[Dict[str, str]] = None,
        raise_on_exceptions: bool = True,
    ) -> BlockscoutResponse:
        params = self.__authorize(params)

        # Rate limit
        if time.time() - self._last_call < self._min_time_between_calls:
            time_to_sleep = self._min_time_between_calls - (time.time() - self._last_call)
            logger.debug(f"Sleeping {time_to_sleep} seconds to avoid rate limit")
            # NOTE: Sleep time is in seconds (float for subseconds)
            time.sleep(time_to_sleep)

        self._last_call = time.time()

        return self._request(
            "GET",
            params=params,
            headers=headers,
            raise_on_exceptions=raise_on_exceptions,
        )

    def _post(
        self, json_dict: Optional[Dict] = None, headers: Optional[Dict[str, str]] = None
    ) -> BlockscoutResponse:
        data = self.__authorize(json_dict)
        return self._request("POST", data=data, headers=headers)

    def _request(
        self,
        method: str,
        raise_on_exceptions: bool = True,
        headers: Optional[Dict] = None,
        params: Optional[Dict] = None,
        data: Optional[Dict] = None,
    ) -> BlockscoutResponse:
        headers = headers or self.DEFAULT_HEADERS
        for i in range(self._retries):
            logger.debug(f"Request sent to {self._clean_uri}.")
            response = self.session.request(
                method.upper(),
                self.base_uri,
                headers=headers,
                params=params,
                data=data,
                timeout=1024,
            )
            if response.status_code == 429:
                time_to_sleep = 2**i
                logger.debug(f"Request was throttled. Retrying in {time_to_sleep} seconds.")
                time.sleep(time_to_sleep)
                continue

            # Recieved a real response unrelated to rate limiting.
            if raise_on_exceptions:
                response.raise_for_status()
            elif not 200 <= response.status_code < 300:
                logger.error(f"Response was not successful: {response.text}")

            break

        return BlockscoutResponse(response, self.ecosystem_name, raise_on_exceptions)

    def __authorize(self, params_or_data: Optional[Dict] = None) -> Optional[Dict]:
        env_var_key = API_KEY_ENV_KEY_MAP.get(self.ecosystem_name)
        if not env_var_key:
            return params_or_data

        api_key = os.environ.get(env_var_key)
        if api_key and (not params_or_data or "apikey" not in params_or_data):
            params_or_data = params_or_data or {}
            api_key = random.choice(api_key.split(","))
            params_or_data["apikey"] = api_key.strip()

        return params_or_data


class ContractClient(_APIClient):
    def __init__(self, ecosystem_name: str, network_name: str, address: str):
        self._address = address
        self.ecosystem_name = ecosystem_name

        super().__init__(
            ecosystem_name=ecosystem_name, network_name=network_name, module_name="contract"
        )

    def get_source_code(self) -> SourceCodeResponse:
        params = {
            **self.base_params,
            "action": "getsourcecode",
            "address": self._address,
        }

        result = self._get(params=params)

        if not (result_list := result.value or []):
            return SourceCodeResponse()

        elif len(result_list) > 1:
            raise UnhandledResultError(result, result_list)

        data = result_list[0]
        if not isinstance(data, dict):
            raise UnhandledResultError(result, data)

        abi = data.get("ABI") or ""
        name = data.get("ContractName") or "unknown"
        return SourceCodeResponse(abi, name)

    def verify_source_code(
        self,
        standard_json_output: Dict,
        compiler_version: str,
        contract_name: Optional[str] = None,
        optimization_used: bool = False,
        optimization_runs: Optional[int] = 200,
        constructor_arguments: Optional[str] = None,
        evm_version: Optional[str] = None,
        license_type: Optional[int] = None,
        libraries: Optional[Dict[str, str]] = None,
    ) -> str:
        libraries = libraries or {}
        if len(libraries) > 10:
            raise ValueError(f"Can only have up to 10 libraries (received {len(libraries)}).")

        if not compiler_version.startswith("v"):
            compiler_version = f"v{compiler_version}"

        if "sourceCode" in standard_json_output:
            source_code = standard_json_output["sourceCode"]
            code_format = "solidity-single-file"
        else:
            source_code = StringIO(json.dumps(standard_json_output))
            code_format = "solidity-standard-json-input"

        json_dict = {
            **self.base_params,
            "action": "verifysourcecode",
            "codeformat": code_format,
            "compilerversion": compiler_version,
            "constructorArguments": constructor_arguments,
            "contractaddress": self._address,
            "contractname": contract_name,
            "evmversion": evm_version,
            "licenseType": license_type,
            "optimizationUsed": int(optimization_used),
            "runs": optimization_runs,
            "sourceCode": source_code,
        }
        iterator = 1
        for lib_address, lib_name in libraries.items():
            json_dict[f"libraryname{iterator}"] = lib_name
            json_dict[f"libraryaddress{iterator}"] = lib_address
            iterator += 1

        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        return str(self._post(json_dict=json_dict, headers=headers).value)

    def check_verify_status(self, guid: str) -> str:
        json_dict = {**self.base_params, "action": "checkverifystatus", "guid": guid}
        response = self._get(params=json_dict, raise_on_exceptions=False)
        return str(response.value)

    def get_creation_data(self) -> List[ContractCreationResponse]:
        params = {
            **self.base_params,
            "action": "getcontractcreation",
            "contractaddresses": [self._address],
        }
        result = self._get(params=params)
        items = result.value or []
        if not isinstance(items, list):
            raise ValueError("Expecting list.")

        return [ContractCreationResponse(**item) for item in items]


class AccountClient(_APIClient):
    def __init__(self, ecosystem_name: str, network_name: str, address: str):
        self._address = address
        self.ecosystem_name = ecosystem_name

        super().__init__(
            ecosystem_name=ecosystem_name, network_name=network_name, module_name="account"
        )

    def get_all_normal_transactions(
        self,
        start_block: Optional[int] = None,
        end_block: Optional[int] = None,
        offset: int = 100,
        sort: str = "asc",
    ) -> Iterator[Dict]:
        page_num = 1
        last_page_results = offset  # Start at offset to trigger iteration
        while last_page_results == offset:
            page = self._get_page_of_normal_transactions(
                page_num, start_block, end_block, offset=offset, sort=sort
            )

            if len(page):
                yield from page

            last_page_results = len(page)
            page_num += 1

    def _get_page_of_normal_transactions(
        self,
        page: int,
        start_block: Optional[int] = None,
        end_block: Optional[int] = None,
        offset: int = 100,
        sort: str = "asc",
    ) -> List[Dict]:
        params = {
            **self.base_params,
            "action": "txlist",
            "address": self._address,
            "startblock": start_block,
            "endblock": end_block,
            "page": page,
            "offset": offset,
            "sort": sort,
        }
        result = self._get(params=params)

        if not isinstance(result.value, list):
            raise UnhandledResultError(result, result.value)

        return result.value


class ClientFactory:
    def __init__(self, ecosystem_name: str, network_name: str):
        self._ecosystem_name = ecosystem_name
        self._network_name = network_name

    def get_contract_client(self, contract_address: str) -> ContractClient:
        return ContractClient(
            ecosystem_name=self._ecosystem_name,
            network_name=self._network_name,
            address=contract_address,
        )

    def get_account_client(self, account_address: str) -> AccountClient:
        return AccountClient(
            ecosystem_name=self._ecosystem_name,
            network_name=self._network_name,
            address=account_address,
        )
