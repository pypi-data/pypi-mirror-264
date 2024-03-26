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


"""
IndexABC
==================

The abstract base class for storage indices. An index is a special type of
Storage that facilitates storing blob metadata. It must wrap another Storage.

Derived classes must implement all methods of both this interface and the
StorageABC interface.
"""

import abc
from datetime import datetime
from typing import Iterator, List, Optional, Tuple

from buildgrid._protos.build.bazel.remote.execution.v2.remote_execution_pb2 import Digest

from ..storage_abc import StorageABC


class IndexABC(StorageABC):
    @abc.abstractmethod
    def __init__(self, *, fallback_on_get: bool = False) -> None:
        # If fallback is enabled, the index is required to fetch blobs from
        # storage on each get_blob and bulk_read_blobs request and update
        # itself accordingly.
        self._fallback_on_get = fallback_on_get

    @abc.abstractmethod
    def delete_blob(self, digest: Digest) -> None:
        """Delete a blob from the index. Return True if the blob was deleted,
        or False otherwise.

        TODO: This method will be promoted to StorageABC in a future commit."""
        raise NotImplementedError()

    @abc.abstractmethod
    def least_recent_digests(self) -> Iterator[Digest]:
        """Generator to iterate through the digests in LRU order"""
        raise NotImplementedError()

    @abc.abstractmethod
    def get_total_size(self, include_marked: bool = True) -> int:
        """
        Return the sum of the size of all blobs within the index.

        If include_marked is True, it will also include the size of blobs that have been marked deleted.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def mark_n_bytes_as_deleted(
        self,
        n_bytes: int,
        dry_run: bool = False,
        include_marked: bool = True,
        protect_blobs_after: Optional[datetime] = None,
        renew_windows: bool = True,
    ) -> Tuple[List[Digest], List[Digest]]:
        """Mark a given number of bytes' worth of index entries as deleted.

        The entries are marked as deleted in LRU order until the total size
        marked as deleted is at least the requested number of bytes. If any
        entries are already marked as deleted, they are used first when
        attempting to reach the required number of bytes.

        Args:
            n_bytes (int): The number of bytes of index entries to mark as
                deleted. When the sum of the ``size_bytes`` of index entries
                meets or exceeds this value, the affected digests will be
                returned.

            include_marked (bool): Consider items already marked for deletion.

        Returns:
            list: Two lists of digests that were marked as deleted. The first list
                contains items that are inlined, the other list contains larger blobs
                contained in a separate storage.

        """
        raise NotImplementedError()
