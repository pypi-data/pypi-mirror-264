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


import logging
from typing import Union, cast

import grpc

from buildgrid._exceptions import InvalidArgumentError, RetriableError
from buildgrid._protos.build.bazel.remote.execution.v2.remote_execution_pb2 import DESCRIPTOR as RE_DESCRIPTOR
from buildgrid._protos.build.bazel.remote.execution.v2.remote_execution_pb2 import (
    GetCapabilitiesRequest,
    ServerCapabilities,
)
from buildgrid._protos.build.bazel.remote.execution.v2.remote_execution_pb2_grpc import (
    CapabilitiesServicer,
    add_CapabilitiesServicer_to_server,
)
from buildgrid.server.actioncache.caches.action_cache_abc import ActionCacheABC
from buildgrid.server.actioncache.instance import ActionCache
from buildgrid.server.auth.manager import authorize_unary_unary
from buildgrid.server.capabilities.instance import CapabilitiesInstance
from buildgrid.server.cas.instance import ContentAddressableStorageInstance
from buildgrid.server.execution.instance import ExecutionInstance
from buildgrid.server.request_metadata_utils import printable_request_metadata
from buildgrid.server.servicer import InstancedServicer
from buildgrid.server.utils.decorators import track_request_id

LOGGER = logging.getLogger(__name__)


class CapabilitiesService(CapabilitiesServicer, InstancedServicer[CapabilitiesInstance]):
    REGISTER_METHOD = add_CapabilitiesServicer_to_server
    FULL_NAME = RE_DESCRIPTOR.services_by_name["Capabilities"].full_name

    @property
    def enabled(self) -> bool:
        # We always want a capabilities service
        return True

    def add_cas_instance(self, name: str, instance: ContentAddressableStorageInstance) -> None:
        self.get_instance(name).add_cas_instance(instance)

    def add_action_cache_instance(self, name: str, instance: Union[ActionCache, ActionCacheABC]) -> None:
        self.get_instance(name).add_action_cache_instance(instance)

    def add_execution_instance(self, name: str, instance: ExecutionInstance) -> None:
        self.get_instance(name).add_execution_instance(instance)

    # --- Public API: Servicer ---

    @authorize_unary_unary(lambda r: cast(str, r.instance_name))
    @track_request_id
    def GetCapabilities(self, request: GetCapabilitiesRequest, context: grpc.ServicerContext) -> ServerCapabilities:
        """Handles GetCapabilitiesRequest messages.

        Args:
            request (GetCapabilitiesRequest): The incoming RPC request.
            context (grpc.ServicerContext): Context for the RPC call.
        """
        LOGGER.info(
            f"GetCapabilities request from [{context.peer()}] "
            f"([{printable_request_metadata(context.invocation_metadata())}])"
        )

        try:
            instance = self.get_instance(request.instance_name)

            return instance.get_capabilities()

        except InvalidArgumentError as e:
            LOGGER.info(e)
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)

        except RetriableError as e:
            LOGGER.info(f"Retriable error, client should retry in: {e.retry_info.retry_delay}")
            context.abort_with_status(e.error_status)

        except Exception as e:
            LOGGER.exception(f"Unexpected error in GetCapabilities; request=[{request}]")
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)

        return ServerCapabilities()
