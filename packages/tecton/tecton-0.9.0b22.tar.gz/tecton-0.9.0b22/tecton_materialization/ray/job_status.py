import contextlib
import logging
import typing
from datetime import datetime
from typing import Optional

from tecton_core.query.executor_utils import QueryTreeMonitor
from tecton_materialization.common.job_metadata import JobMetadataClient
from tecton_proto.materialization.job_metadata_pb2 import JobMetadata
from tecton_proto.materialization.job_metadata_pb2 import TectonManagedStage


logger = logging.getLogger(__name__)

ProgressLogger = typing.Callable[[float], None]
SQLParam = typing.Optional[str]


class MonitoringContextProvider(typing.Protocol):
    def __call__(self, p: SQLParam = None) -> typing.ContextManager[ProgressLogger]: ...


class JobStatusClient(QueryTreeMonitor):
    def __init__(self, metadata_client: JobMetadataClient):
        self._metadata_client = metadata_client

    def create_stage(self, stage_type: TectonManagedStage.StageType, description: str) -> int:
        """
        Returns created stage index
        """

        def _update(job_metadata: JobMetadata) -> JobMetadata:
            new_proto = JobMetadata()
            new_proto.CopyFrom(job_metadata)

            new_stage = TectonManagedStage(
                description=description,
                stage_type=stage_type,
                state=TectonManagedStage.State.PENDING,
            )
            new_proto.tecton_managed_info.stages.append(new_stage)
            return new_proto

        return len(self._metadata_client.update(_update).tecton_managed_info.stages) - 1

    def set_query(self, stage_idx, sql: str):
        def _update(job_metadata: JobMetadata) -> JobMetadata:
            new_proto = JobMetadata()
            new_proto.CopyFrom(job_metadata)

            stage = new_proto.tecton_managed_info.stages[stage_idx]
            if not stage.compiled_sql_query:
                stage.compiled_sql_query = sql

            return new_proto

        self._metadata_client.update(_update)

    def update_progress(self, stage_idx: int, progress: float):
        def _update(job_metadata: JobMetadata) -> JobMetadata:
            new_proto = JobMetadata()
            new_proto.CopyFrom(job_metadata)

            stage = new_proto.tecton_managed_info.stages[stage_idx]

            if stage.state == TectonManagedStage.PENDING:
                stage.state = TectonManagedStage.State.RUNNING
                stage.start_time.GetCurrentTime()

            stage.progress = progress
            stage.duration.FromSeconds(int((datetime.now() - stage.start_time.ToDatetime()).total_seconds()))

            return new_proto

        self._metadata_client.update(_update)

    def set_completed(self, stage_idx: int):
        def _update(job_metadata: JobMetadata) -> JobMetadata:
            new_proto = JobMetadata()
            new_proto.CopyFrom(job_metadata)

            stage = new_proto.tecton_managed_info.stages[stage_idx]
            stage.state = TectonManagedStage.State.SUCCESS

            return new_proto

        self._metadata_client.update(_update)

    def set_failed(self, stage_idx: int, exc: Exception, user_error: bool):
        def _update(job_metadata: JobMetadata) -> JobMetadata:
            new_proto = JobMetadata()
            new_proto.CopyFrom(job_metadata)

            stage = new_proto.tecton_managed_info.stages[stage_idx]
            stage.error_type = (
                TectonManagedStage.ErrorType.USER_ERROR if user_error else TectonManagedStage.ErrorType.UNEXPECTED_ERROR
            )
            stage.error_detail = str(exc)
            stage.state = TectonManagedStage.State.ERROR

            return new_proto

        self._metadata_client.update(_update)

    def set_current_stage_failed(self, error_type: TectonManagedStage.ErrorType, error_detail: str):
        def _update(job_metadata: JobMetadata) -> JobMetadata:
            new_proto = JobMetadata()
            new_proto.CopyFrom(job_metadata)

            current_stage = None
            for stage in new_proto.tecton_managed_info.stages:
                if stage.state == TectonManagedStage.State.ERROR:
                    return new_proto

                # Select first RUNNING or PENDING stage
                # Or if all stages are complete - just the last one
                current_stage = stage
                if stage.state in (TectonManagedStage.State.RUNNING, TectonManagedStage.State.PENDING):
                    break

            if not current_stage:
                # if there are no stages - we will create a dummy one
                current_stage = TectonManagedStage(
                    description="Setting up materialization job",
                    state=TectonManagedStage.State.ERROR,
                )
                new_proto.tecton_managed_info.stages.append(current_stage)

            current_stage.error_type = error_type
            current_stage.error_detail = error_detail
            current_stage.state = TectonManagedStage.State.ERROR

            return new_proto

        self._metadata_client.update(_update)

    def create_stage_monitor(
        self,
        stage_type: TectonManagedStage.StageType,
        description: str,
    ) -> MonitoringContextProvider:
        stage_idx = self.create_stage(stage_type, description)

        @contextlib.contextmanager
        def monitor(sql: Optional[str] = None):
            if sql:
                self.set_query(stage_idx, sql)

            self.update_progress(stage_idx, 0)

            try:
                yield lambda p: self.update_progress(stage_idx, p)
            except Exception as err:
                self.set_failed(stage_idx, err, user_error=False)
                raise
            else:
                self.update_progress(stage_idx, 1)
                self.set_completed(stage_idx)

        return monitor
