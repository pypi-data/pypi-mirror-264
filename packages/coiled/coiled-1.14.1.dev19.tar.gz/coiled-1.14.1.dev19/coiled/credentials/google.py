import datetime
import logging
import os
from typing import Tuple

logger = logging.getLogger(__name__)

try:
    from google.oauth2.credentials import Credentials

    class CoiledShippedCredentials(Credentials):
        def __init__(
            self,
            token=None,
            refresh_token=None,
            id_token=None,
            token_uri=None,
            client_id=None,
            client_secret=None,
            scopes=None,
            default_scopes=None,
            quota_project_id=None,
            expiry=None,
            rapt_token=None,
            refresh_handler=None,
            enable_reauth_refresh=False,
            granted_scopes=None,
        ):
            env_token = self.get_shipped_token()
            if token and env_token and token != env_token:
                raise ValueError(
                    "Specified Google OAuth2 token does not match "
                    "token shipped by Coiled in CLOUDSDK_AUTH_ACCESS_TOKEN.\n"
                    "We recommend not specifying a token and using the shipped token."
                )
            if token and not env_token:
                logger.warning(
                    "Instantiating credentials with explicit token, no shipped token "
                    "found in CLOUDSDK_AUTH_ACCESS_TOKEN. Refresh (which uses CLOUDSDK_AUTH_ACCESS_TOKEN) "
                    "is unlikely to work."
                )

            super().__init__(token=env_token, refresh_handler=self.coiled_token_refresh_handler)

        @staticmethod
        def get_shipped_token():
            token = os.environ.get("CLOUDSDK_AUTH_ACCESS_TOKEN")

            if not token:
                # It's not the normal use-case, but Coiled can also set this env on local client machine
                # so that you can use `CoiledShippedCredentials` (with same OAuth2 token) locally and on cluster.
                token = os.environ.get("COILED_LOCAL_CLOUDSDK_AUTH_ACCESS_TOKEN")

            if not token:
                logger.warning("No Google OAuth2 token found, CLOUDSDK_AUTH_ACCESS_TOKEN env var not set")
            return token

        @staticmethod
        def get_token_expiry(token: str) -> datetime.datetime:
            import httpx

            result = httpx.get(f"https://oauth2.googleapis.com/tokeninfo?access_token={token}")
            data = result.json()
            timestamp = int(data["exp"])
            # note that refresh_handler is expected to return naive utc datetime
            expiry = datetime.datetime.utcfromtimestamp(timestamp)
            return expiry

        def coiled_token_refresh_handler(self, request, scopes) -> Tuple[str, datetime.datetime]:
            # this relies on other Coiled mechanisms to have already shipped a non-expired token to the cluster
            token = self.get_shipped_token()

            if not token:
                from google.auth.exceptions import RefreshError

                raise RefreshError(
                    "Coiled was unable to find Google OAuth2 token on the cluster. "
                    "See https://docs.coiled.io/user_guide/remote-data-access.html#gcp for details about shipping "
                    "OAuth2 tokens from the client to the cluster."
                )

            expiry = self.get_token_expiry(token)

            logger.info(f"CoiledShippedCredentials have been refreshed, new expiration is {expiry}")

            return token, expiry
except ImportError:
    raise ImportError("Unable to create Google Credentials object because google-cloud-iam is not installed.") from None
