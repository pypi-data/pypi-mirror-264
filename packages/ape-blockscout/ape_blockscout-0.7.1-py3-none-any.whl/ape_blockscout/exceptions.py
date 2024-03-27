import os
from typing import TYPE_CHECKING, Union

from ape.exceptions import ApeException
from requests import Response

from ape_blockscout.utils import API_KEY_ENV_KEY_MAP

if TYPE_CHECKING:
    from ape_blockscout.types import BlockscoutResponse, ResponseValue


class BlockscoutException(ApeException):
    """
    A base exception in the ape-blockscout plugin.
    """


class UnsupportedEcosystemError(BlockscoutException):
    """
    Raised when there is no Blockscout buildout for ecosystem.
    """

    def __init__(self, ecosystem: str):
        super().__init__(f"Unsupported Ecosystem: {ecosystem}")


class UnsupportedNetworkError(BlockscoutException):
    """
    Raised when there is no Blockscout buildout for ecosystem.
    """

    def __init__(self, ecosystem_name: str, network_name: str):
        super().__init__(f"Unsupported Network for Ecosystem '{ecosystem_name}': {network_name}")


class BlockscoutResponseError(BlockscoutException):
    """
    Raised when the response is not correct.
    """

    def __init__(self, response: Union[Response, "BlockscoutResponse"], message: str):
        if not isinstance(response, Response):
            response = response.response

        self.response = response
        super().__init__(f"Response indicated failure: {message}")


class UnhandledResultError(BlockscoutResponseError):
    """
    Raised in specific client module where the result from Blockscout
    has an unhandled form.
    """

    def __init__(self, response: Union[Response, "BlockscoutResponse"], value: "ResponseValue"):
        message = f"Unhandled response format: {value}"
        super().__init__(response, message)


class BlockscoutTooManyRequestsError(BlockscoutResponseError):
    """
    Raised after being rate-limited by Blockscout.
    """

    def __init__(self, response: Union[Response, "BlockscoutResponse"], ecosystem: str):
        message = "Blockscout API server rate limit exceeded."
        api_key_name = API_KEY_ENV_KEY_MAP[ecosystem]
        if not os.environ.get(api_key_name):
            message = f"{message}. Try setting {api_key_name}'."

        super().__init__(response, message)


def get_request_error(response: Response, ecosystem: str) -> BlockscoutResponseError:
    response_data = response.json()
    if "result" in response_data and response_data["result"]:
        message = response_data["result"]
    elif "message" in response_data:
        message = response_data["message"]
    else:
        message = response.text

    if "max rate limit reached" in response.text.lower():
        return BlockscoutTooManyRequestsError(response, ecosystem)

    return BlockscoutResponseError(response, message)
