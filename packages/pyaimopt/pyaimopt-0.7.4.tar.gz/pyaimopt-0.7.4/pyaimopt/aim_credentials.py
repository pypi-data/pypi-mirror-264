"""
Python client for Microsoft Research Analog Inference Machine (AIM).

Copyright (c) Microsoft Corporation.
Licensed under the MIT License.
"""

# pylint: disable=eval-used, global-statement

# Standard Library
import json
import os

# from threading import Lock, Thread, get_ident
import threading
import time
from datetime import datetime

# 3rd party
from azure.core import exceptions as azure_exceptions
from azure.identity import (
    AuthenticationRecord,
    InteractiveBrowserCredential,
    TokenCachePersistenceOptions,
)
from .constants import full_name_for_file

#
# Constants
#
AIM_CREDENTIALS_VERSION = "20230808a"
MICROSOFT_ONMICROSOFT = "72f988bf-86f1-41af-91ab-2d7cd011db47"
GREGOSLIVECO_ONMICROSOFT = "791cf287-d56f-4591-97a1-dbca68a63415"
_AIM_CREDENTIAL_CACHE = "AimCredentials"

# All AimCredential instances share one global credential instance.
# This makes sense because the real credentials are not scoped by python constructs.
# Instead, they lie buried in various caches of Microsoft libraries, or something.
# Also, this avoids some racy threading behaviour if each refreshes its own.
# And ensures a tidy termination of the refresh thread when python process exits.
# A reentrant RLock avoids blocking if you try to acquire it while already holding it.
# Sounds a bit dodgy, but is friendlier for future mods than a non-reentrant Lock.
_GLOBAL_REENTRANT_LOCK = threading.RLock()
_GLOBAL_CREDENTIALS = None
_GLOBAL_TOKEN = None


def token_renew_func(**kwargs):
    """
    Thread to renew non-expired OAUTH access token before it expires.
    """

    time.sleep(int(kwargs["sleep"]))
    tenant_id = kwargs["tenant_id"]
    az_url = kwargs["az_url"]

    with _GLOBAL_REENTRANT_LOCK:
        global _GLOBAL_TOKEN

        tok_change = "new"
        scope = f"{az_url}.default"  # black
        new_tok = _GLOBAL_CREDENTIALS.get_token(scope)  # attempt to renew
        if new_tok == _GLOBAL_TOKEN:
            tok_change = "same"
        _GLOBAL_TOKEN = new_tok
        lifetime = datetime.fromtimestamp(_GLOBAL_TOKEN.expires_on) - datetime.now()

    life_seconds = lifetime.total_seconds()
    if "verbose" in kwargs and kwargs["verbose"] is True:
        mess = f"{datetime.now()} thread({threading.get_ident()})"
        mess = f"{mess} {tok_change} token: OAUTH2 lifetime {life_seconds} seconds."
        print(mess)
    if life_seconds <= 0:
        life_seconds = 20
    half_life = life_seconds / 2
    dict_args = {"sleep": half_life, "tenant_id": tenant_id, "az_url": az_url}
    thread = threading.Thread(None, token_renew_func, kwargs=dict_args, daemon=True)
    thread.start()


def guest_account_name(account_name: str) -> str:
    """
    Construct demo tenant guest account name from account name.

    :param account_name: account name to be converted to guest account name
    :type account_name: Returns guest account name
    """
    tail_name = "#EXT#@gregosliveco.onmicrosoft.com"
    account_name = account_name.replace("@", "_")
    return account_name + tail_name


def _authentication_record_file_name() -> str:
    """Name of file where to store authentication information."""
    short_name = f".{_AIM_CREDENTIAL_CACHE}.ini"
    return full_name_for_file(short_name)


def delete_user_credentials():
    """Delete the user credentials file."""
    credentials_filename = _authentication_record_file_name()
    if os.path.exists(credentials_filename):
        os.remove(credentials_filename)


def print_user_credentials(detailed: bool = False):
    """
    Print information about the credentials used to authenticate user.

    :param detailed: if True, print the full authentication record
    """
    filename = _authentication_record_file_name()
    if not os.path.exists(filename):
        print("No user credentials file found.")
        return

    with open(filename, "r", encoding="utf-8") as handler:
        record = json.load(handler)

        print("Username: ", record["username"])
        if detailed:
            print("Authentication Record: ", record)


class AimCredentialsException(Exception):
    """
    Exception type thrown by AimCredentials class.
    """

    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)
        self.message = message


class AimCredentials:
    """
    Class to provide AIM python clients with compliant IETF OAUTH2 credentials.
    """

    # https://www.rfc-editor.org/rfc/rfc6750
    # https://azuresdkdocs.blob.core.windows.net/$web/python/azure-identity/1.2.0/azure.identity.html#:~:text=get_token%28%2Ascopes%2C%20%2A%2Akwargs%29%20%5Bsource%5D%20%C2%B6%20Request%20an%20access%20token,a%20refresh%20token%20upon%20redeeming%20the%20authorization%20code.

    __slots__ = [
        "username",
        "tenant_id",
        "az_url",
        "verbose",
        "guest_username",
    ]

    def __init__(
        self,
        username: str = "",
        tenant_id: str = GREGOSLIVECO_ONMICROSOFT,
        az_url: str = "https://aimdemorsa.blob.core.windows.net/",
        verbose: bool = False,
    ):
        self.username: str = username
        if self.username is None:
            self.username = ""

        self.tenant_id = tenant_id
        os.environ["AZURE_TENANT_ID"] = self.tenant_id
        self.az_url = az_url
        self.verbose = verbose
        try:
            # global GLOBAL_REENTRANT_LOCK
            # global GLOBAL_CREDENTIALS
            with _GLOBAL_REENTRANT_LOCK:
                if _GLOBAL_CREDENTIALS is None:
                    self._init_persistent_credential_cache()
                else:
                    self.username = _GLOBAL_CREDENTIALS._auth_record.username
                    self.guest_username = guest_account_name(self.username)

        except azure_exceptions.ClientAuthenticationError as ex:
            err_auth = f"Azure failed to authenticate {username.lower()}"
            raise AimCredentialsException(err_auth) from ex
        os.environ["AZURE_USERNAME"] = self.username
        self._print_if_verbose(
            f"Using credential for {self.username} and {self.guest_username}"
        )

    def _init_persistent_credential_cache(self):
        """Init use of persistent credential cache and authentication record file."""
        credentials_filename = _authentication_record_file_name()
        if self.username == "" and os.path.exists(credentials_filename):
            with open(credentials_filename, "r", encoding="utf-8") as file_json:
                dict_json = json.load(file_json)
            self.username = dict_json["username"]
        elif self.username == "":
            self.authenticate()
        self.guest_username = guest_account_name(self.username)

        #
        # Attempt to retrieve a cred from the persisted cache.
        # First, recover the AuthenticationRecord from cleartext file.
        # The AuthenticationRecord acts as a record locator within the cache.
        #
        with open(credentials_filename, "r", encoding="utf-8") as fr_json:
            record = fr_json.read()

        dict_json = json.loads(record)
        if "username" not in dict_json:
            mess = "'username' not in authentication_record"
            raise AimCredentialsException(mess)  # black

        if dict_json["username"] != self.username:
            actual = dict_json["username"]
            mess = f"authenticated({actual}) expected({self.username})"
            raise AimCredentialsException(mess)
        authentication_record = AuthenticationRecord.deserialize(record)

        #
        # Use the AuthenticationRecord to recover a cred from the persisted cred cache.
        #
        persist_credential = InteractiveBrowserCredential(
            cache_persistence_options=TokenCachePersistenceOptions(
                allow_unencrypted_storage=True
            ),
            authentication_record=authentication_record,
        )

        #
        # From the credential get a token for the demo tenant's storage account.
        # The AIM web function will expect an access token for this storage account.
        #
        global _GLOBAL_CREDENTIALS
        global _GLOBAL_TOKEN
        _GLOBAL_CREDENTIALS = persist_credential
        _GLOBAL_TOKEN = _GLOBAL_CREDENTIALS.get_token(f"{self.az_url}.default")
        dict_args = {
            "sleep": 0,
            "tenant_id": self.tenant_id,
            "az_url": self.az_url,
            "verbose": self.verbose,
        }
        thread = threading.Thread(
            group=None, target=token_renew_func, kwargs=dict_args, daemon=True
        )
        thread.start()

    def authenticate(self):
        """Obtain fresh OAUTH2 credentials and save to persistent cache."""
        # global GLOBAL_REENTRANT_LOCK
        with _GLOBAL_REENTRANT_LOCK:
            global _GLOBAL_CREDENTIALS
            global _GLOBAL_TOKEN
            _GLOBAL_CREDENTIALS = InteractiveBrowserCredential(
                logging_enable=True,
                tenant_id=self.tenant_id,
                cache_persistence_options=TokenCachePersistenceOptions(
                    name=_AIM_CREDENTIAL_CACHE, allow_unencrypted_storage=True
                ),
            )
            authentication_record_raw = _GLOBAL_CREDENTIALS.authenticate()
            if self.username == "":
                self.username = authentication_record_raw.username
            authentication_record_json = authentication_record_raw.serialize()
            _GLOBAL_TOKEN = _GLOBAL_CREDENTIALS.get_token(f"{self.az_url}.default")

        credentials_filename = _authentication_record_file_name()
        with open(credentials_filename, "w", encoding="utf-8") as f_json:
            f_json.write(authentication_record_json)

    def _print_if_verbose(self, message: str):
        if self.verbose:
            print(message)

    def _get_username(self) -> str:
        """Return the username for this credential."""
        return self.username

    def _get_guest_username(self) -> str:
        """Return the guest form of username for this credential."""
        return self.guest_username

    def _get_credentials(self):
        return _GLOBAL_CREDENTIALS

    def _get_token(self):
        return _GLOBAL_TOKEN

    def _is_expired(self) -> bool:
        """True iff token has remaining valid lifetime, false if token expired."""
        if self.token_valid_seconds() <= 0:
            return True
        return False

    def token_valid_seconds(self) -> int:
        """Remaining seconds per IETF for which the OAUTH2 token is valid."""
        snap_tok = self.Token
        abs_lifetime = datetime.fromtimestamp(snap_tok.expires_on)
        rel_lifetime = abs_lifetime - datetime.now()
        return int(rel_lifetime.total_seconds())

    @staticmethod
    def version() -> str:
        """Returns the version of this class."""
        return AIM_CREDENTIALS_VERSION

    # Properties go below this line.
    Username = property(
        fget=_get_username,
        fset=None,
        doc="Authenticated username.",
    )
    GuestUsername = property(
        fget=_get_guest_username,
        fset=None,
        doc="Authenticated username.",
    )
    Credentials = property(
        fget=_get_credentials,
        fset=None,
        doc="OpenID Connect credential.",
    )
    Token = property(
        fget=_get_token,
        fset=None,
        doc="OAUTH2 token.",
    )
    is_expired = property(
        fget=_is_expired,
        fset=None,
        doc="True iff the token has expired.",
    )
