# Copyright (C) 2018 Bloomberg LP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#  <http://www.apache.org/licenses/LICENSE-2.0>
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import base64
import os
from collections import namedtuple
from typing import Any, Optional, Tuple

import grpc
from grpc import aio

from buildgrid._exceptions import InvalidArgumentError
from buildgrid.client.auth_token_loader import AuthTokenLoader
from buildgrid.utils import read_file


def load_tls_channel_credentials(
    client_key: Optional[str] = None, client_cert: Optional[str] = None, server_cert: Optional[str] = None
) -> Tuple[grpc.ChannelCredentials, Tuple[Optional[str], Optional[str], Optional[str]]]:
    """Looks-up and loads TLS gRPC client channel credentials.

    Args:
        client_key(str, optional): Client certificate chain file path.
        client_cert(str, optional): Client private key file path.
        server_cert(str, optional): Serve root certificate file path.

    Returns:
        ChannelCredentials: Credentials to be used for a TLS-encrypted gRPC
            client channel.
    """
    if server_cert and os.path.exists(server_cert):
        server_cert_pem = read_file(server_cert)
    else:
        server_cert_pem = None
        server_cert = None

    if client_key and os.path.exists(client_key):
        client_key_pem = read_file(client_key)
    else:
        client_key_pem = None
        client_key = None

    if client_key_pem and client_cert and os.path.exists(client_cert):
        client_cert_pem = read_file(client_cert)
    else:
        client_cert_pem = None
        client_cert = None

    credentials = grpc.ssl_channel_credentials(
        root_certificates=server_cert_pem, private_key=client_key_pem, certificate_chain=client_cert_pem
    )

    return credentials, (
        client_key,
        client_cert,
        server_cert,
    )


class AuthMetadataClientInterceptorBase:
    def __init__(
        self,
        auth_token_path: Optional[str] = None,
        auth_token_refresh_seconds: Optional[int] = None,
        auth_secret: Optional[bytes] = None,
    ) -> None:
        """Initialises a new :class:`AuthMetadataClientInterceptorBase`.

        Important:
            One of `auth_token_path` or `auth_secret` must be provided.

        Args:
            auth_token_path (str, optional): Authorization token as a string.
            auth_token_refresh_seconds (str, optional): TIme in seconds to reaload auth token in
            auth_secret (bytes, optional): Authorization secret as bytes.

        Raises:
            InvalidArgumentError: If neither `auth_token_path` or `auth_secret` are
                provided.
        """
        self._auth_token_loader: Optional[AuthTokenLoader] = None
        self.__secret: Optional[str] = None

        if auth_token_path:
            self._auth_token_loader = AuthTokenLoader(
                token_path=auth_token_path, refresh_in_seconds=auth_token_refresh_seconds
            )

        elif auth_secret:
            self.__secret = base64.b64encode(auth_secret.strip()).decode()

        else:
            raise InvalidArgumentError("A secret or token must be provided")

        self.__header_field_name = "authorization"

    def _get_secret(self) -> str:
        if self._auth_token_loader:
            token = self._auth_token_loader.get_token()
        else:
            assert self.__secret is not None
            token = self.__secret
        return f"Bearer {token}"

    def _amend_call_details(  # type: ignore[no-untyped-def] # wait for client lib updates here
        self, client_call_details, grpc_call_details_class: Any
    ):
        """Appends an authorization field to given client call details."""
        if client_call_details.metadata is not None:
            new_metadata = list(client_call_details.metadata)
        else:
            new_metadata = []

        new_metadata.append(
            (
                self.__header_field_name,
                self._get_secret(),
            )
        )

        class _ClientCallDetails(
            namedtuple(
                "_ClientCallDetails",
                (
                    "method",
                    "timeout",
                    "credentials",
                    "metadata",
                    "wait_for_ready",
                ),
            ),
            grpc_call_details_class,  # type: ignore
        ):
            pass

        return _ClientCallDetails(
            client_call_details.method,
            client_call_details.timeout,
            client_call_details.credentials,
            new_metadata,
            client_call_details.wait_for_ready,
        )


# TODO Set Interceptors type args when grpc is updated.
class AuthMetadataClientInterceptor(
    AuthMetadataClientInterceptorBase,
    grpc.UnaryUnaryClientInterceptor,  # type: ignore[type-arg]
    grpc.UnaryStreamClientInterceptor,  # type: ignore[type-arg]
    grpc.StreamUnaryClientInterceptor,  # type: ignore[type-arg]
    grpc.StreamStreamClientInterceptor,  # type: ignore[type-arg]
):
    def __init__(
        self,
        auth_token_path: Optional[str] = None,
        auth_token_refresh_seconds: Optional[int] = None,
        auth_secret: Optional[bytes] = None,
    ) -> None:
        AuthMetadataClientInterceptorBase.__init__(self, auth_token_path, auth_token_refresh_seconds, auth_secret)

    def intercept_unary_unary(  # type: ignore[no-untyped-def] # wait for client lib updates here
        self, continuation, client_call_details, request
    ):
        new_details = self._amend_call_details(client_call_details, grpc.ClientCallDetails)

        return continuation(new_details, request)

    def intercept_unary_stream(  # type: ignore[no-untyped-def] # wait for client lib updates here
        self, continuation, client_call_details, request
    ):
        new_details = self._amend_call_details(client_call_details, grpc.ClientCallDetails)

        return continuation(new_details, request)

    def intercept_stream_unary(  # type: ignore[no-untyped-def] # wait for client lib updates here
        self, continuation, client_call_details, request_iterator
    ):
        new_details = self._amend_call_details(client_call_details, grpc.ClientCallDetails)

        return continuation(new_details, request_iterator)

    def intercept_stream_stream(  # type: ignore[no-untyped-def] # wait for client lib updates here
        self, continuation, client_call_details, request_iterator
    ):
        new_details = self._amend_call_details(client_call_details, grpc.ClientCallDetails)

        return continuation(new_details, request_iterator)


# TODO Set Interceptors type args when grpc is updated.
class AsyncAuthMetadataClientInterceptor(
    AuthMetadataClientInterceptorBase,
    aio.UnaryUnaryClientInterceptor,  # type: ignore[type-arg]
    aio.UnaryStreamClientInterceptor,  # type: ignore[type-arg]
    aio.StreamUnaryClientInterceptor,  # type: ignore[type-arg]
    aio.StreamStreamClientInterceptor,  # type: ignore[type-arg]
):
    def __init__(
        self,
        auth_token_path: Optional[str] = None,
        auth_token_refresh_seconds: Optional[int] = None,
        auth_secret: Optional[bytes] = None,
    ) -> None:
        AuthMetadataClientInterceptorBase.__init__(self, auth_token_path, auth_token_refresh_seconds, auth_secret)

    async def intercept_unary_unary(  # type: ignore[no-untyped-def] # wait for client lib updates here
        self, continuation, client_call_details, request
    ):
        new_details = self._amend_call_details(client_call_details, aio.ClientCallDetails)

        return await continuation(new_details, request)

    async def intercept_unary_stream(  # type: ignore[no-untyped-def] # wait for client lib updates here
        self, continuation, client_call_details, request
    ):
        new_details = self._amend_call_details(client_call_details, aio.ClientCallDetails)

        return await continuation(new_details, request)

    async def intercept_stream_unary(  # type: ignore[no-untyped-def] # wait for client lib updates here
        self, continuation, client_call_details, request_iterator
    ):
        new_details = self._amend_call_details(client_call_details, aio.ClientCallDetails)

        return await continuation(new_details, request_iterator)

    async def intercept_stream_stream(  # type: ignore[no-untyped-def] # wait for client lib updates here
        self, continuation, client_call_details, request_iterator
    ):
        new_details = self._amend_call_details(client_call_details, aio.ClientCallDetails)

        return await continuation(new_details, request_iterator)
