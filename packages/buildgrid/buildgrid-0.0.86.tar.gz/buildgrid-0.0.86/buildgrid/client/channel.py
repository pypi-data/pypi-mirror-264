# Copyright (C) 2019 Bloomberg LP
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

from collections import namedtuple
from typing import TYPE_CHECKING, Any, List, Optional, Tuple, Union, cast
from urllib.parse import urlparse

import grpc
from grpc import aio

from buildgrid._exceptions import InvalidArgumentError
from buildgrid._protos.build.bazel.remote.execution.v2 import remote_execution_pb2
from buildgrid.client.authentication import (
    AsyncAuthMetadataClientInterceptor,
    AuthMetadataClientInterceptor,
    load_tls_channel_credentials,
)
from buildgrid.settings import REQUEST_METADATA_HEADER_NAME, REQUEST_METADATA_TOOL_NAME, REQUEST_METADATA_TOOL_VERSION
from buildgrid.utils import insecure_uri_schemes, secure_uri_schemes


def setup_channel(
    remote_url: str,
    auth_token: Optional[str] = None,
    auth_token_refresh_seconds: Optional[int] = None,
    client_key: Optional[str] = None,
    client_cert: Optional[str] = None,
    server_cert: Optional[str] = None,
    action_id: Optional[str] = None,
    tool_invocation_id: Optional[str] = None,
    correlated_invocations_id: Optional[str] = None,
    asynchronous: bool = False,
    timeout: Optional[float] = None,
) -> Tuple[grpc.Channel, Tuple[Optional[str], ...]]:
    """Creates a new gRPC client communication chanel.

    If `remote_url` does not point to a socket and does not specify a
    port number, defaults 50051.

    Args:
        remote_url (str): URL for the remote, including protocol and,
            if not a Unix domain socket, a port.
        auth_token (str): Authorization token file path.
        auth_token_refresh_seconds(int): Time in seconds to read the authorization token again from file
        server_cert(str): TLS certificate chain file path.
        client_key (str): TLS root certificate file path.
        client_cert (str): TLS private key file path.
        action_id (str): Action identifier to which the request belongs to.
        tool_invocation_id (str): Identifier for a related group of Actions.
        correlated_invocations_id (str): Identifier that ties invocations together.
        timeout (float): Request timeout in seconds.

    Returns:
        Channel: Client Channel to be used in order to access the server
            at `remote_url`.

    Raises:
        InvalidArgumentError: On any input parsing error.
    """
    url = urlparse(remote_url)

    url_is_socket = url.scheme == "unix"
    if url_is_socket:
        remote = remote_url
    else:
        remote = f"{url.hostname}:{url.port or 50051}"

    details: Tuple[Optional[str], Optional[str], Optional[str]] = None, None, None
    credentials_provided = any((server_cert, client_cert, client_key))

    if asynchronous:
        async_interceptors = _create_async_interceptors(
            auth_token=auth_token,
            auth_token_refresh_seconds=auth_token_refresh_seconds,
            action_id=action_id,
            tool_invocation_id=tool_invocation_id,
            correlated_invocations_id=correlated_invocations_id,
            timeout=timeout,
        )

        if url.scheme in insecure_uri_schemes or (url_is_socket and not credentials_provided):
            async_channel = aio.insecure_channel(remote, interceptors=async_interceptors)
        elif url.scheme in secure_uri_schemes or (url_is_socket and credentials_provided):
            credentials, details = load_tls_channel_credentials(client_key, client_cert, server_cert)
            if not credentials:
                raise InvalidArgumentError("Given TLS details (or defaults) could be loaded")
            async_channel = aio.secure_channel(remote, credentials, interceptors=async_interceptors)
        else:
            raise InvalidArgumentError("Given remote does not specify a protocol")

        # TODO use overloads to make this return an async channel when asynchronous == True
        return async_channel, details  # type: ignore[return-value]

    else:
        sync_interceptors = _create_sync_interceptors(
            auth_token=auth_token,
            auth_token_refresh_seconds=auth_token_refresh_seconds,
            action_id=action_id,
            tool_invocation_id=tool_invocation_id,
            correlated_invocations_id=correlated_invocations_id,
            timeout=timeout,
        )

        if url.scheme in insecure_uri_schemes or (url_is_socket and not credentials_provided):
            sync_channel = grpc.insecure_channel(remote)
        elif url.scheme in secure_uri_schemes or (url_is_socket and credentials_provided):
            credentials, details = load_tls_channel_credentials(client_key, client_cert, server_cert)
            if not credentials:
                raise InvalidArgumentError("Given TLS details (or defaults) could be loaded")
            sync_channel = grpc.secure_channel(remote, credentials)
        else:
            raise InvalidArgumentError("Given remote does not specify a protocol")

        for interceptor in sync_interceptors:
            sync_channel = grpc.intercept_channel(sync_channel, interceptor)

        return sync_channel, details


class RequestMetadataInterceptorBase:
    def __init__(
        self,
        action_id: Optional[str] = None,
        tool_invocation_id: Optional[str] = None,
        correlated_invocations_id: Optional[str] = None,
    ) -> None:
        """Appends optional `RequestMetadata` header values to each call.

        Args:
            action_id (str): Action identifier to which the request belongs to.
            tool_invocation_id (str): Identifier for a related group of Actions.
            correlated_invocations_id (str): Identifier that ties invocations together.
        """
        self._action_id = action_id
        self._tool_invocation_id = tool_invocation_id
        self._correlated_invocations_id = correlated_invocations_id

        self.__header_field_name = REQUEST_METADATA_HEADER_NAME
        self.__header_field_value = self._request_metadata()

    def _request_metadata(self) -> bytes:
        """Creates a serialized RequestMetadata entry to attach to a gRPC
        call header. Arguments should be of type str or None.
        """
        request_metadata = remote_execution_pb2.RequestMetadata()
        request_metadata.tool_details.tool_name = REQUEST_METADATA_TOOL_NAME
        request_metadata.tool_details.tool_version = REQUEST_METADATA_TOOL_VERSION

        if self._action_id:
            request_metadata.action_id = self._action_id
        if self._tool_invocation_id:
            request_metadata.tool_invocation_id = self._tool_invocation_id
        if self._correlated_invocations_id:
            request_metadata.correlated_invocations_id = self._correlated_invocations_id

        return request_metadata.SerializeToString()

    def _amend_call_details(  # type: ignore[no-untyped-def] # wait for client lib updates here
        self, client_call_details, grpc_call_details_class: Any
    ):
        if client_call_details.metadata is not None:
            new_metadata = list(client_call_details.metadata)
        else:
            new_metadata = []

        new_metadata.append((self.__header_field_name, self.__header_field_value))

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
class RequestMetadataInterceptor(
    RequestMetadataInterceptorBase,
    grpc.UnaryUnaryClientInterceptor,  # type: ignore[type-arg]
    grpc.UnaryStreamClientInterceptor,  # type: ignore[type-arg]
    grpc.StreamUnaryClientInterceptor,  # type: ignore[type-arg]
    grpc.StreamStreamClientInterceptor,  # type: ignore[type-arg]
):
    def __init__(
        self,
        action_id: Optional[str] = None,
        tool_invocation_id: Optional[str] = None,
        correlated_invocations_id: Optional[str] = None,
    ) -> None:
        RequestMetadataInterceptorBase.__init__(
            self,
            action_id=action_id,
            tool_invocation_id=tool_invocation_id,
            correlated_invocations_id=correlated_invocations_id,
        )

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
class AsyncRequestMetadataInterceptor(
    RequestMetadataInterceptorBase,
    aio.UnaryUnaryClientInterceptor,  # type: ignore[type-arg]
    aio.UnaryStreamClientInterceptor,  # type: ignore[type-arg]
    aio.StreamUnaryClientInterceptor,  # type: ignore[type-arg]
    aio.StreamStreamClientInterceptor,  # type: ignore[type-arg]
):
    def __init__(
        self,
        action_id: Optional[str] = None,
        tool_invocation_id: Optional[str] = None,
        correlated_invocations_id: Optional[str] = None,
    ) -> None:
        RequestMetadataInterceptorBase.__init__(
            self,
            action_id=action_id,
            tool_invocation_id=tool_invocation_id,
            correlated_invocations_id=correlated_invocations_id,
        )

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


class TimeoutInterceptorBase:
    def __init__(self, timeout: float) -> None:
        """Applies a request timeout to each call.

        Args:
            timeout (float): Request timeout in seconds.
        """
        self._timeout = timeout

    def _amend_call_details(  # type: ignore[no-untyped-def] # wait for client lib updates here
        self, client_call_details, grpc_call_details_class: Any
    ):
        # If there are multiple timeouts, apply the shorter timeout (earliest deadline wins)
        if client_call_details.timeout is not None:
            new_timeout = min(self._timeout, client_call_details.timeout)
        else:
            new_timeout = self._timeout

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
            new_timeout,
            client_call_details.credentials,
            client_call_details.metadata,
            client_call_details.wait_for_ready,
        )


# TODO Set Interceptors type args when grpc is updated.
class TimeoutInterceptor(
    TimeoutInterceptorBase,
    grpc.UnaryUnaryClientInterceptor,  # type: ignore[type-arg]
    grpc.UnaryStreamClientInterceptor,  # type: ignore[type-arg]
    grpc.StreamUnaryClientInterceptor,  # type: ignore[type-arg]
    grpc.StreamStreamClientInterceptor,  # type: ignore[type-arg]
):
    def __init__(self, timeout: float) -> None:
        TimeoutInterceptorBase.__init__(self, timeout=timeout)

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
class AsyncTimeoutInterceptor(
    TimeoutInterceptorBase,
    aio.UnaryUnaryClientInterceptor,  # type: ignore[type-arg]
    aio.UnaryStreamClientInterceptor,  # type: ignore[type-arg]
    aio.StreamUnaryClientInterceptor,  # type: ignore[type-arg]
    aio.StreamStreamClientInterceptor,  # type: ignore[type-arg]
):
    def __init__(self, timeout: float) -> None:
        TimeoutInterceptorBase.__init__(self, timeout=timeout)

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


if TYPE_CHECKING:
    SyncInterceptorsList = List[
        Union[
            grpc.UnaryUnaryClientInterceptor[Any, Any],
            grpc.UnaryStreamClientInterceptor[Any, Any],
            grpc.StreamUnaryClientInterceptor[Any, Any],
            grpc.StreamStreamClientInterceptor[Any, Any],
        ]
    ]


def _create_sync_interceptors(
    auth_token: Optional[str] = None,
    auth_token_refresh_seconds: Optional[int] = None,
    action_id: Optional[str] = None,
    tool_invocation_id: Optional[str] = None,
    correlated_invocations_id: Optional[str] = None,
    timeout: Optional[float] = None,
) -> "SyncInterceptorsList":
    interceptors: "SyncInterceptorsList" = []
    interceptors.append(
        RequestMetadataInterceptor(
            action_id=action_id,
            tool_invocation_id=tool_invocation_id,
            correlated_invocations_id=correlated_invocations_id,
        )
    )

    if auth_token is not None:
        interceptors.append(
            AuthMetadataClientInterceptor(
                auth_token_path=auth_token, auth_token_refresh_seconds=auth_token_refresh_seconds
            )
        )

    if timeout is not None:
        interceptors.append(TimeoutInterceptor(timeout))

    return interceptors


def _create_async_interceptors(
    auth_token: Optional[str] = None,
    auth_token_refresh_seconds: Optional[int] = None,
    action_id: Optional[str] = None,
    tool_invocation_id: Optional[str] = None,
    correlated_invocations_id: Optional[str] = None,
    timeout: Optional[float] = None,
) -> List[aio.ClientInterceptor]:
    # FIXME Types not happy...  "list" has incompatible type "..."; expected "_PartialStubMustCastOrIgnore"
    interceptors: List[Any] = []
    interceptors.append(
        AsyncRequestMetadataInterceptor(
            action_id=action_id,
            tool_invocation_id=tool_invocation_id,
            correlated_invocations_id=correlated_invocations_id,
        )
    )

    if auth_token is not None:
        interceptors.append(
            AsyncAuthMetadataClientInterceptor(
                auth_token_path=auth_token, auth_token_refresh_seconds=auth_token_refresh_seconds
            )
        )

    if timeout is not None:
        interceptors.append(AsyncTimeoutInterceptor(timeout))

    return cast(List[aio.ClientInterceptor], interceptors)
