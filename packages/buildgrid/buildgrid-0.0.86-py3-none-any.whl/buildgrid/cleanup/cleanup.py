# Copyright (C) 2020 Bloomberg LP
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
import threading
import time
from contextlib import ExitStack
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from buildgrid._protos.build.bazel.remote.execution.v2.remote_execution_pb2 import Digest
from buildgrid.server.cas.storage.index.index_abc import IndexABC
from buildgrid.server.cas.storage.storage_abc import StorageABC
from buildgrid.server.cas.storage.with_cache import WithCacheStorage
from buildgrid.server.metrics_names import (
    CLEANUP_BLOBS_DELETION_RATE_METRIC_NAME,
    CLEANUP_BYTES_DELETION_RATE_METRIC_NAME,
    CLEANUP_INDEX_BULK_DELETE_METRIC_NAME,
    CLEANUP_INDEX_MARK_DELETED_METRIC_NAME,
    CLEANUP_RUNTIME_METRIC_NAME,
    CLEANUP_STORAGE_BULK_DELETE_METRIC_NAME,
    CLEANUP_STORAGE_DELETION_FAILURES_METRIC_NAME,
)
from buildgrid.server.metrics_utils import DurationMetric, publish_counter_metric, publish_gauge_metric
from buildgrid.server.monitoring import (
    MonitoringBus,
    MonitoringOutputFormat,
    MonitoringOutputType,
    get_monitoring_bus,
    set_monitoring_bus,
)
from buildgrid.server.threading import ContextThreadPoolExecutor, ContextWorker

LOGGER = logging.getLogger(__name__)


def _digests_str(digests: List[Digest]) -> str:
    return f"{len(digests)} digests ({sum(d.size_bytes for d in digests)} bytes)"


class CASCleanUp:
    """Creates a LRU CAS cleanup service."""

    def __init__(
        self,
        dry_run: bool,
        high_watermark: int,
        low_watermark: int,
        sleep_interval: int,
        batch_size: int,
        only_if_unused_for: timedelta,
        storages: Dict[str, StorageABC],
        indexes: Dict[str, IndexABC],
        monitor: bool,
        mon_endpoint_type: Optional[MonitoringOutputType] = None,
        mon_endpoint_location: Optional[str] = None,
        mon_serialisation_format: Optional[MonitoringOutputFormat] = None,
        mon_metric_prefix: Optional[str] = None,
    ) -> None:
        self._stack = ExitStack()
        self._dry_run = dry_run

        self._high_watermark = high_watermark
        self._low_watermark = low_watermark
        self._batch_size = batch_size
        self._only_if_unused_for = only_if_unused_for

        self._storages = storages
        self._indexes = indexes

        self._is_instrumented = monitor

        self._sleep_interval = sleep_interval

        if self._is_instrumented:
            set_monitoring_bus(
                MonitoringBus(
                    endpoint_type=mon_endpoint_type or MonitoringOutputType.SOCKET,
                    endpoint_location=mon_endpoint_location,
                    metric_prefix=mon_metric_prefix or "",
                    serialisation_format=mon_serialisation_format or MonitoringOutputFormat.STATSD,
                )
            )

    # --- Public API ---

    def start(self, timeout: Optional[float] = None) -> None:
        """Start cleanup service"""
        if self._is_instrumented:
            self._stack.enter_context(get_monitoring_bus())
        worker = self._stack.enter_context(ContextWorker(self._begin_cleanup, "CleanUpLauncher"))
        worker.wait(timeout=timeout)

    def stop(self, *args: Any, **kwargs: Any) -> None:
        """Stops the cleanup service"""
        LOGGER.info("Stopping Cleanup Service")
        self._stack.close()

    def _begin_cleanup(self, stop_requested: threading.Event) -> None:
        if self._dry_run:
            for instance_name, storage in self._storages.items():
                if storage.is_cleanup_enabled():
                    self._calculate_cleanup(instance_name)
            return

        attempts = 0
        with ContextThreadPoolExecutor(max_workers=len(self._storages)) as ex:
            while True:
                futures = {
                    instance_name: ex.submit(self._cleanup_worker, instance_name, stop_requested)
                    for instance_name, storage in self._storages.items()
                    if storage.is_cleanup_enabled()
                }

                failed = False
                for instance_name, future in futures.items():
                    try:
                        future.result()
                        LOGGER.info(f"CleanUp for {instance_name} completed")
                    except Exception:
                        LOGGER.exception(f"CleanUp for {instance_name} failed")
                        failed = True

                if not failed:
                    break

                # Exponential backoff before retrying
                sleep_time = 1.6**attempts
                LOGGER.info(f"Retrying Cleanup in {sleep_time} seconds")
                stop_requested.wait(timeout=sleep_time)
                attempts += 1
                continue

    def _calculate_cleanup(self, instance_name: str) -> None:
        """Work out which blobs will be deleted by the cleanup command."""

        LOGGER.info(f"Cleanup dry run for instance '{instance_name}'")
        index = self._indexes[instance_name]
        only_delete_before = self._get_last_accessed_threshold()
        total_size = index.get_total_size()
        LOGGER.info(
            f"CAS size is {total_size} bytes, compared with a high water mark of "
            f"{self._high_watermark} bytes and a low water mark of {self._low_watermark} bytes."
        )
        if total_size >= self._high_watermark:
            required_space = total_size - self._low_watermark
            inlined_digests, digests = index.mark_n_bytes_as_deleted(
                required_space, self._dry_run, protect_blobs_after=only_delete_before
            )
            digests += inlined_digests
            cleared_space = sum(digest.size_bytes for digest in digests)
            LOGGER.info(f"{len(digests)} digests will be deleted, freeing up {cleared_space} bytes.")
        else:
            LOGGER.info(f"Total size {total_size} is less than the high water mark, " f"nothing will be deleted.")

    def _do_cleanup_batch(
        self,
        instance_name: str,
        index: IndexABC,
        storage: StorageABC,
        only_delete_before: datetime,
        total_size: int,
        is_first_run: bool,
        stop_requested: threading.Event,
    ) -> None:
        """
        When using a SQL Index, entries with a delete marker are "in the process of being deleted".
        This is required because storage operations can't be safely tied to the SQL index transaction
        (one may fail independently of the other, and you end up inconsistent).

        The workflow is roughly as follows:
        - Start a SQL transaction.
        - Lock and mark the indexed items you want to delete.
        - Close the SQL transaction.
        - Perform the storage deletes
        - Start a SQL transaction.
        - Actually delete the index entries.
        - Close the SQL transaction.

        This means anything with deleted=False will always be present in S3. If it is marked
        deleted=True, and the process gets killed during the "Perform the storage deletes", only
        some of the items might actually be gone.

        The next time the cleaner starts up, it can try to do that delete again (ignoring 404s).
        Eventually that will succeed and the item will actually be removed from the DB. Only during
        the first run of batches do we consider already marked items. This avoids multiple cleanup
        daemons from competing with each other on every batch.
        """
        batch_start_time = time.time()

        LOGGER.info(f"Starting mark of {self._batch_size} from index")

        # Mark a batch of index entries for deletion
        with DurationMetric(CLEANUP_INDEX_MARK_DELETED_METRIC_NAME, instance_name, instanced=True):
            # If is_first_run==True, then set renew_windows=True, an expensive SQL will run to construct
            # LRU windows. Otherwise, the previously constructed LRU windows will be used for speed up.
            #
            # If is_first_run==True, then set include_marked=True, we will count already
            # deleted blobs to the total we are deleting.
            inlined_digests, storage_digests_to_delete = index.mark_n_bytes_as_deleted(
                self._batch_size,
                protect_blobs_after=only_delete_before,
                include_marked=is_first_run,
                renew_windows=is_first_run,
            )

        if not inlined_digests and not storage_digests_to_delete:
            err = (
                "Marked 0 digests for deletion, even though cleanup was triggered. "
                "This may be because the remaining digests have been accessed within "
                f"{only_delete_before}."
            )
            if total_size >= self._high_watermark:
                LOGGER.error(f"{err} Total size still remains greater than high watermark!")
            else:
                LOGGER.warning(err)
            stop_requested.wait(timeout=self._sleep_interval)  # Avoid a busy loop when we can't make progress
            return

        LOGGER.info(f"Marked records in index: {_digests_str(inlined_digests + storage_digests_to_delete)}")

        if inlined_digests:
            # Bulk delete the entries for the successfully deleted (and already missing)
            # blobs from the storage
            with DurationMetric(CLEANUP_INDEX_BULK_DELETE_METRIC_NAME, instance_name, instanced=True):
                index_failed_deletions = index.bulk_delete(inlined_digests)

            # TODO this should not be possible from type-hint. Fix the code...
            if index_failed_deletions is None:
                LOGGER.error("Calling bulk_delete on the index returned 'None' instead of a list")
                index_failed_deletions = []
            if index_failed_deletions:
                LOGGER.info(f"Failed to delete {len(index_failed_deletions)} records from index")

            deleted_digests = [d for d in inlined_digests if d.hash not in index_failed_deletions]
            LOGGER.info(f"Bulk deleted records from index: {_digests_str(deleted_digests)}")

        if storage_digests_to_delete:
            # Bulk delete the marked blobs from the actual storage backend
            with DurationMetric(CLEANUP_STORAGE_BULK_DELETE_METRIC_NAME, instance_name, instanced=True):
                failed_delete_hashes = storage.bulk_delete(storage_digests_to_delete)

            if failed_delete_hashes:
                # Separately handle blobs which failed to be deleted and blobs that
                # were already missing from the storage
                if self._is_instrumented:
                    publish_counter_metric(
                        CLEANUP_STORAGE_DELETION_FAILURES_METRIC_NAME,
                        len(failed_delete_hashes),
                        {"instance-name": instance_name},
                    )

                LOGGER.info(f"Failed to delete {len(failed_delete_hashes)} blobs.")
                for failure in failed_delete_hashes:
                    LOGGER.debug(f"Failed to delete {failure}.")

                index_digests_to_delete = [
                    digest for digest in storage_digests_to_delete if digest.hash not in failed_delete_hashes
                ]
            else:
                # TODO this should not be possible from type-hint. Fix the code...
                if failed_delete_hashes is None:
                    LOGGER.error("Calling bulk_delete on storage returned 'None' instead of a list")
                index_digests_to_delete = storage_digests_to_delete

            LOGGER.info(f"Bulk deleted blobs from storage: {_digests_str(storage_digests_to_delete)}")

            # Bulk delete the entries for the successfully deleted (and already missing)
            # blobs from the storage
            with DurationMetric(CLEANUP_INDEX_BULK_DELETE_METRIC_NAME, instance_name, instanced=True):
                index_failed_deletions = index.bulk_delete(index_digests_to_delete)

            # TODO this should not be possible from type-hint. Fix the code...
            if index_failed_deletions is None:
                LOGGER.error("Calling bulk_delete on the index returned 'None' instead of a list")
                index_failed_deletions = []
            if index_failed_deletions:
                LOGGER.info(f"Failed to delete {len(index_failed_deletions)} records from index")

            deleted_digests = [d for d in index_digests_to_delete if d.hash not in index_failed_deletions]
            LOGGER.info(f"Bulk deleted records from index: {_digests_str(deleted_digests)}")

        if self._is_instrumented:
            deleted_digests = inlined_digests + storage_digests_to_delete
            batch_duration = time.time() - batch_start_time
            blobs_deleted_per_second = len(deleted_digests) / batch_duration
            publish_gauge_metric(
                CLEANUP_BLOBS_DELETION_RATE_METRIC_NAME, blobs_deleted_per_second, {"instance-name": instance_name}
            )

            bytes_deleted = sum(digest.size_bytes for digest in deleted_digests)
            bytes_deleted_per_second = bytes_deleted / batch_duration
            publish_gauge_metric(
                CLEANUP_BYTES_DELETION_RATE_METRIC_NAME, bytes_deleted_per_second, {"instance-name": instance_name}
            )

    def _cleanup_worker(self, instance_name: str, stop_requested: threading.Event) -> None:
        """Cleanup when full"""
        storage = self._storages[instance_name]
        if isinstance(storage, WithCacheStorage):
            LOGGER.warning(
                "Cleaning up a WithCache storage will not cleanup local cache entries "
                "running with a total cache size larger than the configured low watermark "
                "may result in inconsistent cache state."
            )
        index = self._indexes[instance_name]
        index.set_instance_name(instance_name)
        storage.set_instance_name(instance_name)
        LOGGER.info(f"Cleanup for instance '{instance_name}' started.")

        while not stop_requested.is_set():
            # When first starting a loop, we will also include any remaining delete markers as part of
            # the total size.
            total_size = index.get_total_size(include_marked=True)
            if total_size >= self._high_watermark:
                to_delete = total_size - self._low_watermark
                LOGGER.info(
                    f"CAS size for instance '{instance_name}' is {total_size} bytes, at least "
                    f"{to_delete} bytes will be cleared."
                )
                LOGGER.info(f"Deleting items from storage/index for instance '{instance_name}'.")

                with DurationMetric(CLEANUP_RUNTIME_METRIC_NAME, instance_name, instanced=True):
                    is_first_run = True
                    while not stop_requested.is_set() and total_size > self._low_watermark:
                        only_delete_before = self._get_last_accessed_threshold()
                        self._do_cleanup_batch(
                            instance_name=instance_name,
                            index=index,
                            storage=storage,
                            only_delete_before=only_delete_before,
                            total_size=total_size,
                            is_first_run=is_first_run,
                            stop_requested=stop_requested,
                        )
                        is_first_run = False
                        # Here we should have already deleted any remaining delete markers,
                        # Our cleanup target should be based on finding new entries.
                        total_size = index.get_total_size(include_marked=False)
                        LOGGER.info(f"After batch, the non-stale total size is {total_size} bytes.")

                # Report the final size including the marked deleted items.
                total_size = index.get_total_size(include_marked=True)
                LOGGER.info(f"Finished cleanup. CAS size is now {total_size} bytes.")

            stop_requested.wait(timeout=self._sleep_interval)

    def _get_last_accessed_threshold(self) -> datetime:
        return datetime.utcnow() - self._only_if_unused_for
