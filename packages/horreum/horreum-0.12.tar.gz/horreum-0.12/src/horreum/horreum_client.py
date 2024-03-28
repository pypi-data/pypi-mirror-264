from importlib.metadata import version

from kiota_abstractions.authentication import AuthenticationProvider
from kiota_abstractions.authentication.access_token_provider import AccessTokenProvider
from kiota_abstractions.authentication.anonymous_authentication_provider import AnonymousAuthenticationProvider
from kiota_abstractions.authentication.base_bearer_token_authentication_provider import (
    BaseBearerTokenAuthenticationProvider)
from kiota_http.httpx_request_adapter import HttpxRequestAdapter

from .keycloak_access_provider import KeycloakAccessProvider
from .raw_client.horreum_raw_client import HorreumRawClient


async def setup_auth_provider(base_url: str, username: str, password: str) -> AccessTokenProvider:
    # Use not authenticated client to fetch the auth mechanism
    auth_provider = AnonymousAuthenticationProvider()
    req_adapter = HttpxRequestAdapter(auth_provider)
    req_adapter.base_url = base_url
    auth_client = HorreumRawClient(req_adapter)

    auth_config = await auth_client.api.config.keycloak.get()
    # TODO: we could generalize using a generic OIDC client
    return KeycloakAccessProvider(auth_config, username, password)


class HorreumClient:
    __base_url: str
    __username: str
    __password: str

    # Raw client, this could be used to interact with the low-level api
    raw_client: HorreumRawClient
    auth_provider: AuthenticationProvider

    def __init__(self, base_url: str, username: str = None, password: str = None):
        self.__base_url = base_url
        self.__username = username
        self.__password = password

    async def setup(self):
        """
        Set up the authentication provider, based on the Horreum configuration, and the low-level horreum api client
        """

        if self.__username is not None:
            # Bearer token authentication
            access_provider = await setup_auth_provider(self.__base_url, self.__username, self.__password)
            self.auth_provider = BaseBearerTokenAuthenticationProvider(access_provider)
        elif self.__password is not None:
            raise RuntimeError("providing password without username, have you missed something?")
        else:
            # Anonymous authentication
            self.auth_provider = AnonymousAuthenticationProvider()

        req_adapter = HttpxRequestAdapter(self.auth_provider)
        req_adapter.base_url = self.__base_url

        self.raw_client = HorreumRawClient(req_adapter)

    ##################
    # High-level API #
    ##################

    @staticmethod
    def version() -> str:
        return version("horreum")


async def new_horreum_client(base_url: str, username: str = None, password: str = None) -> HorreumClient:
    """
    Initialize the horreum client
    :param base_url: horreum api base url
    :param username: auth username
    :param password: auth password
    :return: HorreumClient instance
    """
    client = HorreumClient(base_url, username, password)
    await client.setup()

    return client
