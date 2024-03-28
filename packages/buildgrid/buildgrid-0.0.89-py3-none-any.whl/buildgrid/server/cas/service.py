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


"""
CAS services
==================

Implements the Content Addressable Storage API and ByteStream API.
"""

import itertools
import logging
import re
from typing import Iterator, Tuple, cast

import grpc

import buildgrid.server.context as context_module
from buildgrid._enums import ByteStreamResourceType
from buildgrid._exceptions import (
    InvalidArgumentError,
    NotFoundError,
    OutOfRangeError,
    PermissionDeniedError,
    RetriableError,
    StorageFullError,
)
from buildgrid._protos.build.bazel.remote.execution.v2.remote_execution_pb2 import DESCRIPTOR as RE_DESCRIPTOR
from buildgrid._protos.build.bazel.remote.execution.v2.remote_execution_pb2 import (
    BatchReadBlobsRequest,
    BatchReadBlobsResponse,
    BatchUpdateBlobsRequest,
    BatchUpdateBlobsResponse,
    FindMissingBlobsRequest,
    FindMissingBlobsResponse,
    GetTreeRequest,
    GetTreeResponse,
)
from buildgrid._protos.build.bazel.remote.execution.v2.remote_execution_pb2_grpc import (
    ContentAddressableStorageServicer,
    add_ContentAddressableStorageServicer_to_server,
)
from buildgrid._protos.google.bytestream import bytestream_pb2, bytestream_pb2_grpc
from buildgrid._protos.google.bytestream.bytestream_pb2 import (
    QueryWriteStatusRequest,
    QueryWriteStatusResponse,
    ReadRequest,
    ReadResponse,
    WriteRequest,
    WriteResponse,
)
from buildgrid._protos.google.rpc import code_pb2, status_pb2
from buildgrid.server.auth.manager import authorize_stream_unary, authorize_unary_stream, authorize_unary_unary
from buildgrid.server.cas.instance import (
    EMPTY_BLOB,
    EMPTY_BLOB_DIGEST,
    ByteStreamInstance,
    ContentAddressableStorageInstance,
)
from buildgrid.server.metrics_names import (
    CAS_BATCH_READ_BLOBS_TIME_METRIC_NAME,
    CAS_BATCH_UPDATE_BLOBS_TIME_METRIC_NAME,
    CAS_BYTESTREAM_READ_TIME_METRIC_NAME,
    CAS_BYTESTREAM_WRITE_TIME_METRIC_NAME,
    CAS_FIND_MISSING_BLOBS_TIME_METRIC_NAME,
    CAS_GET_TREE_TIME_METRIC_NAME,
)
from buildgrid.server.metrics_utils import DurationMetric, generator_method_duration_metric
from buildgrid.server.request_metadata_utils import printable_request_metadata
from buildgrid.server.servicer import InstancedServicer
from buildgrid.server.utils.decorators import track_request_id, track_request_id_generator

LOGGER = logging.getLogger(__name__)


class ContentAddressableStorageService(
    ContentAddressableStorageServicer, InstancedServicer[ContentAddressableStorageInstance]
):
    REGISTER_METHOD = add_ContentAddressableStorageServicer_to_server
    FULL_NAME = RE_DESCRIPTOR.services_by_name["ContentAddressableStorage"].full_name

    @authorize_unary_unary(lambda r: cast(str, r.instance_name))
    @context_module.metadatacontext()
    @track_request_id
    @DurationMetric(CAS_FIND_MISSING_BLOBS_TIME_METRIC_NAME)
    def FindMissingBlobs(
        self, request: FindMissingBlobsRequest, context: grpc.ServicerContext
    ) -> FindMissingBlobsResponse:
        LOGGER.info(
            f"FindMissingBlobs request from [{context.peer()}] "
            f"([{printable_request_metadata(context.invocation_metadata())}])"
        )

        try:
            instance = self.get_instance(request.instance_name)
            # No need to find the empty blob in the cas because the empty blob cannot be missing
            digests_to_find = [digest for digest in request.blob_digests if digest != EMPTY_BLOB_DIGEST]
            response = instance.find_missing_blobs(digests_to_find)
            return response

        except InvalidArgumentError as e:
            LOGGER.info(e)
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)

        except ConnectionError as e:
            LOGGER.exception(e)
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.UNAVAILABLE)

        # Attempt to catch postgres connection failures and instruct clients to retry
        except RetriableError as e:
            LOGGER.info(f"Retriable error, client should retry in: {e.retry_info.retry_delay}")
            context.abort_with_status(e.error_status)

        except Exception as e:
            LOGGER.exception(f"Unexpected error in FindMissingBlobs; request=[{request}]")
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)

        return FindMissingBlobsResponse()

    @authorize_unary_unary(lambda r: cast(str, r.instance_name))
    @context_module.metadatacontext()
    @track_request_id
    @DurationMetric(CAS_BATCH_UPDATE_BLOBS_TIME_METRIC_NAME)
    def BatchUpdateBlobs(
        self, request: BatchUpdateBlobsRequest, context: grpc.ServicerContext
    ) -> BatchUpdateBlobsResponse:
        LOGGER.info(
            f"BatchUpdateBlobs request from [{context.peer()}] "
            f"([{printable_request_metadata(context.invocation_metadata())}])"
        )

        try:
            instance = self.get_instance(request.instance_name)
            response = instance.batch_update_blobs(request.requests)

            return response

        except InvalidArgumentError as e:
            LOGGER.info(e)
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)

        except PermissionDeniedError as e:
            LOGGER.exception(e)
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)

        except ConnectionError as e:
            LOGGER.exception(e)
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.UNAVAILABLE)

        # Attempt to catch postgres connection failures and instruct clients to retry
        except RetriableError as e:
            LOGGER.info(f"Retriable error, client should retry in: {e.retry_info.retry_delay}")
            context.abort_with_status(e.error_status)

        except Exception as e:
            # Log the digests but not the data:
            printable_request = {
                "instance_name": request.instance_name,
                "digests": [r.digest for r in request.requests],
            }

            LOGGER.info(f"Unexpected error in BatchUpdateBlobs; request=[{printable_request}]")
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)

        return BatchUpdateBlobsResponse()

    @authorize_unary_unary(lambda r: cast(str, r.instance_name))
    @context_module.metadatacontext()
    @track_request_id
    @DurationMetric(CAS_BATCH_READ_BLOBS_TIME_METRIC_NAME)
    def BatchReadBlobs(self, request: BatchReadBlobsRequest, context: grpc.ServicerContext) -> BatchReadBlobsResponse:
        LOGGER.info(
            f"BatchReadBlobs request from [{context.peer()}] "
            f"([{printable_request_metadata(context.invocation_metadata())}])"
        )
        try:
            # No need to actually read the empty blob in the cas as it is always present
            digests_to_read = [digest for digest in request.digests if digest != EMPTY_BLOB_DIGEST]
            empty_digest_count = len(request.digests) - len(digests_to_read)

            instance = self.get_instance(request.instance_name)
            response = instance.batch_read_blobs(digests_to_read)

            # Append the empty blobs to the response
            for _ in range(empty_digest_count):
                response_proto = response.responses.add()
                response_proto.data = EMPTY_BLOB
                response_proto.digest.CopyFrom(EMPTY_BLOB_DIGEST)
                status_code = code_pb2.OK
                response_proto.status.CopyFrom(status_pb2.Status(code=status_code))

            return response

        except InvalidArgumentError as e:
            LOGGER.info(e)
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)

        except PermissionDeniedError as e:
            LOGGER.exception(e)
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)

        except ConnectionError as e:
            LOGGER.exception(e)
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.UNAVAILABLE)

        # Attempt to catch postgres connection failures and instruct clients to retry
        except RetriableError as e:
            LOGGER.info(f"Retriable error, client should retry in: {e.retry_info.retry_delay}")
            context.abort_with_status(e.error_status)

        except Exception as e:
            LOGGER.exception(f"Unexpected error in BatchReadBlobs; request=[{request}]")
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)

        return BatchReadBlobsResponse()

    @authorize_unary_stream(lambda r: cast(str, r.instance_name))
    @track_request_id_generator
    @DurationMetric(CAS_GET_TREE_TIME_METRIC_NAME)
    def GetTree(self, request: GetTreeRequest, context: grpc.ServicerContext) -> Iterator[GetTreeResponse]:
        LOGGER.info(
            f"GetTree request from [{context.peer()}] "
            f"([{printable_request_metadata(context.invocation_metadata())}])"
        )

        try:
            instance = self.get_instance(request.instance_name)
            yield from instance.get_tree(request)

        except InvalidArgumentError as e:
            LOGGER.info(e)
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)

        except NotFoundError as e:
            LOGGER.info(e)
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.NOT_FOUND)

        except ConnectionError as e:
            LOGGER.exception(e)
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.UNAVAILABLE)

        # Attempt to catch postgres connection failures and instruct clients to retry
        except RetriableError as e:
            LOGGER.info(f"Retriable error, client should retry in: {e.retry_info.retry_delay}")
            context.abort_with_status(e.error_status)

        except Exception as e:
            LOGGER.exception(f"Unexpected error in GetTree; request=[{request}]")
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)

        yield GetTreeResponse()


class ResourceNameRegex:
    # CAS read name format: "{instance_name}/blobs/{hash}/{size}"
    READ = "^(.*?)/?(blobs/.*/[0-9]*)$"

    # CAS write name format: "{instance_name}/uploads/{uuid}/blobs/{hash}/{size}[optional arbitrary extra content]"
    WRITE = "^(.*?)/?(uploads/.*/blobs/.*/[0-9]*)"


def _parse_resource_name(resource_name: str, regex: str) -> Tuple[str, str, "ByteStreamResourceType"]:
    cas_match = re.match(regex, resource_name)
    if cas_match:
        return cas_match[1], cas_match[2], ByteStreamResourceType.CAS
    else:
        raise InvalidArgumentError(f"Invalid resource name: [{resource_name}]")


class ByteStreamService(bytestream_pb2_grpc.ByteStreamServicer, InstancedServicer[ByteStreamInstance]):
    REGISTER_METHOD = bytestream_pb2_grpc.add_ByteStreamServicer_to_server
    FULL_NAME = bytestream_pb2.DESCRIPTOR.services_by_name["ByteStream"].full_name

    @authorize_unary_stream(lambda r: _parse_resource_name(r.resource_name, ResourceNameRegex.READ)[0])
    @context_module.metadatacontext()
    @track_request_id_generator
    @generator_method_duration_metric(CAS_BYTESTREAM_READ_TIME_METRIC_NAME)
    def Read(self, request: ReadRequest, context: grpc.ServicerContext) -> Iterator[ReadResponse]:
        LOGGER.info(
            f"Read request from [{context.peer()}] " f"([{printable_request_metadata(context.invocation_metadata())}])"
        )
        try:
            instance_name, resource_name, resource_type = _parse_resource_name(
                request.resource_name, ResourceNameRegex.READ
            )
            instance = self.get_instance(instance_name)
            if resource_type == ByteStreamResourceType.CAS:
                blob_details = resource_name.split("/")
                hash_, size_bytes = blob_details[1], blob_details[2]
                if size_bytes == "0":
                    if hash_ != EMPTY_BLOB_DIGEST.hash:
                        raise InvalidArgumentError(f"Invalid digest [{hash_}/{size_bytes}]")
                    yield bytestream_pb2.ReadResponse(data=EMPTY_BLOB)
                else:
                    yield from instance.read_cas_blob(hash_, size_bytes, request.read_offset, request.read_limit)

        except InvalidArgumentError as e:
            LOGGER.info(e)
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            yield bytestream_pb2.ReadResponse()

        except NotFoundError as e:
            LOGGER.info(f"{request.resource_name} not found", exc_info=True)
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.NOT_FOUND)
            yield bytestream_pb2.ReadResponse()

        except OutOfRangeError as e:
            LOGGER.exception(e)
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.OUT_OF_RANGE)
            yield bytestream_pb2.ReadResponse()

        except ConnectionError as e:
            LOGGER.exception(e)
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.UNAVAILABLE)
            yield bytestream_pb2.ReadResponse()

        except RetriableError as e:
            LOGGER.info(f"Retriable error, client should retry in: {e.retry_info.retry_delay}")
            context.abort_with_status(e.error_status)

        except Exception as e:
            LOGGER.exception(f"Unexpected error in ByteStreamRead; request=[{request}]")
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)

    @authorize_stream_unary(lambda r: _parse_resource_name(r.resource_name, ResourceNameRegex.WRITE)[0])
    @context_module.metadatacontext()
    @track_request_id
    @DurationMetric(CAS_BYTESTREAM_WRITE_TIME_METRIC_NAME)
    def Write(self, request_iterator: Iterator[WriteRequest], context: grpc.ServicerContext) -> WriteResponse:
        LOGGER.info(
            f"Write request from [{context.peer()}] "
            f"([{printable_request_metadata(context.invocation_metadata())}])"
        )
        try:
            request = next(request_iterator)
            instance_name, resource_name, resource_type = _parse_resource_name(
                request.resource_name,
                ResourceNameRegex.WRITE,
            )
            instance = self.get_instance(instance_name)
            if resource_type == ByteStreamResourceType.CAS:
                blob_details = resource_name.split("/")
                _, hash_, size_bytes = blob_details[1], blob_details[3], blob_details[4]
                return instance.write_cas_blob(hash_, size_bytes, itertools.chain([request], request_iterator))

        except NotImplementedError as e:
            LOGGER.info(e)
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.UNIMPLEMENTED)

        except InvalidArgumentError as e:
            LOGGER.info(e)
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)

        except NotFoundError as e:
            LOGGER.exception(e)
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.NOT_FOUND)

        except PermissionDeniedError as e:
            LOGGER.exception(e)
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)

        except StorageFullError as e:
            LOGGER.exception(e)
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.RESOURCE_EXHAUSTED)

        except ConnectionError as e:
            LOGGER.exception(e)
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.UNAVAILABLE)

        except RetriableError as e:
            LOGGER.info(f"Retriable error, client should retry in: {e.retry_info.retry_delay}")
            context.abort_with_status(e.error_status)

        except Exception as e:
            # Log all the fields except `data`:
            printable_request = {
                "resource_name": request.resource_name,
                "write_offset": request.write_offset,
                "finish_write": request.finish_write,
            }

            LOGGER.exception(f"Unexpected error in ByteStreamWrite; request=[{printable_request}]")
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)

        return bytestream_pb2.WriteResponse()

    @authorize_unary_unary(lambda r: _parse_resource_name(r.resource_name, ResourceNameRegex.WRITE)[0])
    @track_request_id
    def QueryWriteStatus(
        self, request: QueryWriteStatusRequest, context: grpc.ServicerContext
    ) -> QueryWriteStatusResponse:
        LOGGER.info(f"QueryWriteStatus request from [{context.peer()}]")
        context.abort(grpc.StatusCode.UNIMPLEMENTED, "Method not implemented!")
