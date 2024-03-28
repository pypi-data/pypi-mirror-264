# Copyright (C) 2023 Bloomberg LP
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


import uuid
from functools import wraps
from typing import Any, Callable, Iterator, TypeVar

from buildgrid.server.context import ctx_grpc_request_id

_Res = TypeVar("_Res")
_Self = TypeVar("_Self")
_Req = TypeVar("_Req")
_Ctx = TypeVar("_Ctx")


def track_request_id(f: Callable[[_Self, _Req, _Ctx], _Res]) -> Callable[[_Self, _Req, _Ctx], _Res]:
    """Decorator to set the request ID ContextVar.

    This decorator sets the ``ctx_grpc_request_id`` ContextVar to a UUID
    for the duration of the decorated function. This ContextVar is used
    in logging output to allow log lines for the same request to be
    identified.

    """

    @wraps(f)
    def wrapper(*args: Any, **kwargs: Any) -> _Res:
        ctx_grpc_request_id.set(str(uuid.uuid4()))
        try:
            return f(*args, **kwargs)
        finally:
            ctx_grpc_request_id.set(None)

    return wrapper


def track_request_id_generator(
    f: Callable[[_Self, _Req, _Ctx], Iterator[_Res]]
) -> Callable[[_Self, _Req, _Ctx], Iterator[_Res]]:
    """Decorator to set the request ID ContextVar.

    This is similar to ``track_request_id``, except aimed at wrapping
    generator functions.

    """

    @wraps(f)
    def wrapper(*args: Any, **kwargs: Any) -> Iterator[_Res]:
        ctx_grpc_request_id.set(str(uuid.uuid4()))
        try:
            yield from f(*args, **kwargs)
        finally:
            ctx_grpc_request_id.set(None)

    return wrapper
