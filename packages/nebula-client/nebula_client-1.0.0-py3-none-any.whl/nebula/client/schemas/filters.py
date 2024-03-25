"""
Schemas that define Nebula REST API filtering operations.
"""

from typing import List, Optional
from uuid import UUID

from nebula._internal.pydantic import HAS_PYDANTIC_V2

if HAS_PYDANTIC_V2:
    from pydantic.v1 import Field
else:
    from pydantic import Field

from nebula._internal.schemas.bases import NebulaBaseModel
from nebula._internal.schemas.fields import DateTimeTZ
from nebula.client.schemas.objects import StateType
from nebula.utilities.collections import AutoEnum


class Operator(AutoEnum):
    """Operators for combining filter criteria."""

    and_ = AutoEnum.auto()
    or_ = AutoEnum.auto()


class OperatorMixin:
    """Base model for Nebula filters that combines criteria with a user-provided operator"""

    operator: Operator = Field(
        default=Operator.and_,
        description="Operator for combining filter criteria. Defaults to 'and_'.",
    )


class FlowFilterId(NebulaBaseModel):
    """Filter by `Flow.id`."""

    any_: Optional[List[UUID]] = Field(
        default=None, description="A list of flow ids to include"
    )


class FlowFilterName(NebulaBaseModel):
    """Filter by `Flow.name`."""

    any_: Optional[List[str]] = Field(
        default=None,
        description="A list of flow names to include",
        example=["my-flow-1", "my-flow-2"],
    )

    like_: Optional[str] = Field(
        default=None,
        description=(
            "A case-insensitive partial match. For example, "
            " passing 'astro' will match "
            "'astro', 'sad-Astro', and 'astro-robot'."
        ),
        example="astro",
    )


class FlowFilterTags(NebulaBaseModel, OperatorMixin):
    """Filter by `Flow.tags`."""

    all_: Optional[List[str]] = Field(
        default=None,
        example=["tag-1", "tag-2"],
        description=(
            "A list of tags. Flows will be returned only if their tags are a superset"
            " of the list"
        ),
    )
    is_null_: Optional[bool] = Field(
        default=None, description="If true, only include flows without tags"
    )


class FlowFilter(NebulaBaseModel, OperatorMixin):
    """Filter for flows. Only flows matching all criteria will be returned."""

    id: Optional[FlowFilterId] = Field(
        default=None, description="Filter criteria for `Flow.id`"
    )
    name: Optional[FlowFilterName] = Field(
        default=None, description="Filter criteria for `Flow.name`"
    )
    tags: Optional[FlowFilterTags] = Field(
        default=None, description="Filter criteria for `Flow.tags`"
    )


class FlowRunFilterId(NebulaBaseModel):
    """Filter by FlowRun.id."""

    any_: Optional[List[UUID]] = Field(
        default=None, description="A list of flow run ids to include"
    )
    not_any_: Optional[List[UUID]] = Field(
        default=None, description="A list of flow run ids to exclude"
    )


class FlowRunFilterName(NebulaBaseModel):
    """Filter by `FlowRun.name`."""

    any_: Optional[List[str]] = Field(
        default=None,
        description="A list of flow run names to include",
        example=["my-flow-run-1", "my-flow-run-2"],
    )

    like_: Optional[str] = Field(
        default=None,
        description=(
            "A case-insensitive partial match. For example, "
            " passing 'astro' will match "
            "'astro', 'sad-Astro', and 'astro-robot'."
        ),
        example="astro",
    )


class FlowRunFilterTags(NebulaBaseModel, OperatorMixin):
    """Filter by `FlowRun.tags`."""

    all_: Optional[List[str]] = Field(
        default=None,
        example=["tag-1", "tag-2"],
        description=(
            "A list of tags. Flow runs will be returned only if their tags are a"
            " superset of the list"
        ),
    )
    is_null_: Optional[bool] = Field(
        default=None, description="If true, only include flow runs without tags"
    )


class FlowRunFilterDeploymentId(NebulaBaseModel, OperatorMixin):
    """Filter by `FlowRun.deployment_id`."""

    any_: Optional[List[UUID]] = Field(
        default=None, description="A list of flow run deployment ids to include"
    )
    is_null_: Optional[bool] = Field(
        default=None,
        description="If true, only include flow runs without deployment ids",
    )


class FlowRunFilterWorkQueueName(NebulaBaseModel, OperatorMixin):
    """Filter by `FlowRun.work_queue_name`."""

    any_: Optional[List[str]] = Field(
        default=None,
        description="A list of work queue names to include",
        example=["work_queue_1", "work_queue_2"],
    )
    is_null_: Optional[bool] = Field(
        default=None,
        description="If true, only include flow runs without work queue names",
    )


class FlowRunFilterStateType(NebulaBaseModel):
    """Filter by `FlowRun.state_type`."""

    any_: Optional[List[StateType]] = Field(
        default=None, description="A list of flow run state types to include"
    )


class FlowRunFilterStateName(NebulaBaseModel):
    any_: Optional[List[str]] = Field(
        default=None, description="A list of flow run state names to include"
    )


class FlowRunFilterState(NebulaBaseModel, OperatorMixin):
    type: Optional[FlowRunFilterStateType]
    name: Optional[FlowRunFilterStateName]


class FlowRunFilterFlowVersion(NebulaBaseModel):
    """Filter by `FlowRun.flow_version`."""

    any_: Optional[List[str]] = Field(
        default=None, description="A list of flow run flow_versions to include"
    )


class FlowRunFilterStartTime(NebulaBaseModel):
    """Filter by `FlowRun.start_time`."""

    before_: Optional[DateTimeTZ] = Field(
        default=None,
        description="Only include flow runs starting at or before this time",
    )
    after_: Optional[DateTimeTZ] = Field(
        default=None,
        description="Only include flow runs starting at or after this time",
    )
    is_null_: Optional[bool] = Field(
        default=None, description="If true, only return flow runs without a start time"
    )


class FlowRunFilterExpectedStartTime(NebulaBaseModel):
    """Filter by `FlowRun.expected_start_time`."""

    before_: Optional[DateTimeTZ] = Field(
        default=None,
        description="Only include flow runs scheduled to start at or before this time",
    )
    after_: Optional[DateTimeTZ] = Field(
        default=None,
        description="Only include flow runs scheduled to start at or after this time",
    )


class FlowRunFilterNextScheduledStartTime(NebulaBaseModel):
    """Filter by `FlowRun.next_scheduled_start_time`."""

    before_: Optional[DateTimeTZ] = Field(
        default=None,
        description=(
            "Only include flow runs with a next_scheduled_start_time or before this"
            " time"
        ),
    )
    after_: Optional[DateTimeTZ] = Field(
        default=None,
        description=(
            "Only include flow runs with a next_scheduled_start_time at or after this"
            " time"
        ),
    )


class FlowRunFilterParentFlowRunId(NebulaBaseModel, OperatorMixin):
    """Filter for subflows of the given flow runs"""

    any_: Optional[List[UUID]] = Field(
        default=None, description="A list of flow run parents to include"
    )


class FlowRunFilterParentTaskRunId(NebulaBaseModel, OperatorMixin):
    """Filter by `FlowRun.parent_task_run_id`."""

    any_: Optional[List[UUID]] = Field(
        default=None, description="A list of flow run parent_task_run_ids to include"
    )
    is_null_: Optional[bool] = Field(
        default=None,
        description="If true, only include flow runs without parent_task_run_id",
    )


class FlowRunFilterIdempotencyKey(NebulaBaseModel):
    """Filter by FlowRun.idempotency_key."""

    any_: Optional[List[str]] = Field(
        default=None, description="A list of flow run idempotency keys to include"
    )
    not_any_: Optional[List[str]] = Field(
        default=None, description="A list of flow run idempotency keys to exclude"
    )


class FlowRunFilter(NebulaBaseModel, OperatorMixin):
    """Filter flow runs. Only flow runs matching all criteria will be returned"""

    id: Optional[FlowRunFilterId] = Field(
        default=None, description="Filter criteria for `FlowRun.id`"
    )
    name: Optional[FlowRunFilterName] = Field(
        default=None, description="Filter criteria for `FlowRun.name`"
    )
    tags: Optional[FlowRunFilterTags] = Field(
        default=None, description="Filter criteria for `FlowRun.tags`"
    )
    deployment_id: Optional[FlowRunFilterDeploymentId] = Field(
        default=None, description="Filter criteria for `FlowRun.deployment_id`"
    )
    work_queue_name: Optional[FlowRunFilterWorkQueueName] = Field(
        default=None, description="Filter criteria for `FlowRun.work_queue_name"
    )
    state: Optional[FlowRunFilterState] = Field(
        default=None, description="Filter criteria for `FlowRun.state`"
    )
    flow_version: Optional[FlowRunFilterFlowVersion] = Field(
        default=None, description="Filter criteria for `FlowRun.flow_version`"
    )
    start_time: Optional[FlowRunFilterStartTime] = Field(
        default=None, description="Filter criteria for `FlowRun.start_time`"
    )
    expected_start_time: Optional[FlowRunFilterExpectedStartTime] = Field(
        default=None, description="Filter criteria for `FlowRun.expected_start_time`"
    )
    next_scheduled_start_time: Optional[FlowRunFilterNextScheduledStartTime] = Field(
        default=None,
        description="Filter criteria for `FlowRun.next_scheduled_start_time`",
    )
    parent_flow_run_id: Optional[FlowRunFilterParentFlowRunId] = Field(
        default=None, description="Filter criteria for subflows of the given flow runs"
    )
    parent_task_run_id: Optional[FlowRunFilterParentTaskRunId] = Field(
        default=None, description="Filter criteria for `FlowRun.parent_task_run_id`"
    )
    idempotency_key: Optional[FlowRunFilterIdempotencyKey] = Field(
        default=None, description="Filter criteria for `FlowRun.idempotency_key`"
    )


class TaskRunFilterFlowRunId(NebulaBaseModel):
    """Filter by `TaskRun.flow_run_id`."""

    any_: Optional[List[UUID]] = Field(
        default=None, description="A list of flow run ids to include"
    )

    is_null_: bool = Field(
        default=False,
        description="If true, only include task runs without a flow run id",
    )


class TaskRunFilterId(NebulaBaseModel):
    """Filter by `TaskRun.id`."""

    any_: Optional[List[UUID]] = Field(
        default=None, description="A list of task run ids to include"
    )


class TaskRunFilterName(NebulaBaseModel):
    """Filter by `TaskRun.name`."""

    any_: Optional[List[str]] = Field(
        default=None,
        description="A list of task run names to include",
        example=["my-task-run-1", "my-task-run-2"],
    )

    like_: Optional[str] = Field(
        default=None,
        description=(
            "A case-insensitive partial match. For example, "
            " passing 'astro' will match "
            "'astro', 'sad-Astro', and 'astro-robot'."
        ),
        example="astro",
    )


class TaskRunFilterTags(NebulaBaseModel, OperatorMixin):
    """Filter by `TaskRun.tags`."""

    all_: Optional[List[str]] = Field(
        default=None,
        example=["tag-1", "tag-2"],
        description=(
            "A list of tags. Task runs will be returned only if their tags are a"
            " superset of the list"
        ),
    )
    is_null_: Optional[bool] = Field(
        default=None, description="If true, only include task runs without tags"
    )


class TaskRunFilterStateType(NebulaBaseModel):
    """Filter by `TaskRun.state_type`."""

    any_: Optional[List[StateType]] = Field(
        default=None, description="A list of task run state types to include"
    )


class TaskRunFilterStateName(NebulaBaseModel):
    any_: Optional[List[str]] = Field(
        default=None, description="A list of task run state names to include"
    )


class TaskRunFilterState(NebulaBaseModel, OperatorMixin):
    type: Optional[TaskRunFilterStateType]
    name: Optional[TaskRunFilterStateName]


class TaskRunFilterSubFlowRuns(NebulaBaseModel):
    """Filter by `TaskRun.subflow_run`."""

    exists_: Optional[bool] = Field(
        default=None,
        description=(
            "If true, only include task runs that are subflow run parents; if false,"
            " exclude parent task runs"
        ),
    )


class TaskRunFilterStartTime(NebulaBaseModel):
    """Filter by `TaskRun.start_time`."""

    before_: Optional[DateTimeTZ] = Field(
        default=None,
        description="Only include task runs starting at or before this time",
    )
    after_: Optional[DateTimeTZ] = Field(
        default=None,
        description="Only include task runs starting at or after this time",
    )
    is_null_: Optional[bool] = Field(
        default=None, description="If true, only return task runs without a start time"
    )


class TaskRunFilter(NebulaBaseModel, OperatorMixin):
    """Filter task runs. Only task runs matching all criteria will be returned"""

    id: Optional[TaskRunFilterId] = Field(
        default=None, description="Filter criteria for `TaskRun.id`"
    )
    name: Optional[TaskRunFilterName] = Field(
        default=None, description="Filter criteria for `TaskRun.name`"
    )
    tags: Optional[TaskRunFilterTags] = Field(
        default=None, description="Filter criteria for `TaskRun.tags`"
    )
    state: Optional[TaskRunFilterState] = Field(
        default=None, description="Filter criteria for `TaskRun.state`"
    )
    start_time: Optional[TaskRunFilterStartTime] = Field(
        default=None, description="Filter criteria for `TaskRun.start_time`"
    )
    subflow_runs: Optional[TaskRunFilterSubFlowRuns] = Field(
        default=None, description="Filter criteria for `TaskRun.subflow_run`"
    )
    flow_run_id: Optional[TaskRunFilterFlowRunId] = Field(
        default=None, description="Filter criteria for `TaskRun.flow_run_id`"
    )


class DeploymentFilterId(NebulaBaseModel):
    """Filter by `Deployment.id`."""

    any_: Optional[List[UUID]] = Field(
        default=None, description="A list of deployment ids to include"
    )


class DeploymentFilterName(NebulaBaseModel):
    """Filter by `Deployment.name`."""

    any_: Optional[List[str]] = Field(
        default=None,
        description="A list of deployment names to include",
        example=["my-deployment-1", "my-deployment-2"],
    )

    like_: Optional[str] = Field(
        default=None,
        description=(
            "A case-insensitive partial match. For example, "
            " passing 'astro' will match "
            "'astro', 'sad-Astro', and 'astro-robot'."
        ),
        example="astro",
    )


class DeploymentFilterWorkQueueName(NebulaBaseModel):
    """Filter by `Deployment.work_queue_name`."""

    any_: Optional[List[str]] = Field(
        default=None,
        description="A list of work queue names to include",
        example=["work_queue_1", "work_queue_2"],
    )


class DeploymentFilterIsScheduleActive(NebulaBaseModel):
    """Filter by `Deployment.is_schedule_active`."""

    eq_: Optional[bool] = Field(
        default=None,
        description="Only returns where deployment schedule is/is not active",
    )


class DeploymentFilterTags(NebulaBaseModel, OperatorMixin):
    """Filter by `Deployment.tags`."""

    all_: Optional[List[str]] = Field(
        default=None,
        example=["tag-1", "tag-2"],
        description=(
            "A list of tags. Deployments will be returned only if their tags are a"
            " superset of the list"
        ),
    )
    is_null_: Optional[bool] = Field(
        default=None, description="If true, only include deployments without tags"
    )


class DeploymentFilter(NebulaBaseModel, OperatorMixin):
    """Filter for deployments. Only deployments matching all criteria will be returned."""

    id: Optional[DeploymentFilterId] = Field(
        default=None, description="Filter criteria for `Deployment.id`"
    )
    name: Optional[DeploymentFilterName] = Field(
        default=None, description="Filter criteria for `Deployment.name`"
    )
    is_schedule_active: Optional[DeploymentFilterIsScheduleActive] = Field(
        default=None, description="Filter criteria for `Deployment.is_schedule_active`"
    )
    tags: Optional[DeploymentFilterTags] = Field(
        default=None, description="Filter criteria for `Deployment.tags`"
    )
    work_queue_name: Optional[DeploymentFilterWorkQueueName] = Field(
        default=None, description="Filter criteria for `Deployment.work_queue_name`"
    )


class LogFilterName(NebulaBaseModel):
    """Filter by `Log.name`."""

    any_: Optional[List[str]] = Field(
        default=None,
        description="A list of log names to include",
        example=["nebula.logger.flow_runs", "nebula.logger.task_runs"],
    )


class LogFilterLevel(NebulaBaseModel):
    """Filter by `Log.level`."""

    ge_: Optional[int] = Field(
        default=None,
        description="Include logs with a level greater than or equal to this level",
        example=20,
    )

    le_: Optional[int] = Field(
        default=None,
        description="Include logs with a level less than or equal to this level",
        example=50,
    )


class LogFilterTimestamp(NebulaBaseModel):
    """Filter by `Log.timestamp`."""

    before_: Optional[DateTimeTZ] = Field(
        default=None,
        description="Only include logs with a timestamp at or before this time",
    )
    after_: Optional[DateTimeTZ] = Field(
        default=None,
        description="Only include logs with a timestamp at or after this time",
    )


class LogFilterFlowRunId(NebulaBaseModel):
    """Filter by `Log.flow_run_id`."""

    any_: Optional[List[UUID]] = Field(
        default=None, description="A list of flow run IDs to include"
    )


class LogFilterTaskRunId(NebulaBaseModel):
    """Filter by `Log.task_run_id`."""

    any_: Optional[List[UUID]] = Field(
        default=None, description="A list of task run IDs to include"
    )


class LogFilter(NebulaBaseModel, OperatorMixin):
    """Filter logs. Only logs matching all criteria will be returned"""

    level: Optional[LogFilterLevel] = Field(
        default=None, description="Filter criteria for `Log.level`"
    )
    timestamp: Optional[LogFilterTimestamp] = Field(
        default=None, description="Filter criteria for `Log.timestamp`"
    )
    flow_run_id: Optional[LogFilterFlowRunId] = Field(
        default=None, description="Filter criteria for `Log.flow_run_id`"
    )
    task_run_id: Optional[LogFilterTaskRunId] = Field(
        default=None, description="Filter criteria for `Log.task_run_id`"
    )


class FilterSet(NebulaBaseModel):
    """A collection of filters for common objects"""

    flows: FlowFilter = Field(
        default_factory=FlowFilter, description="Filters that apply to flows"
    )
    flow_runs: FlowRunFilter = Field(
        default_factory=FlowRunFilter, description="Filters that apply to flow runs"
    )
    task_runs: TaskRunFilter = Field(
        default_factory=TaskRunFilter, description="Filters that apply to task runs"
    )
    deployments: DeploymentFilter = Field(
        default_factory=DeploymentFilter,
        description="Filters that apply to deployments",
    )


class BlockTypeFilterName(NebulaBaseModel):
    """Filter by `BlockType.name`"""

    like_: Optional[str] = Field(
        default=None,
        description=(
            "A case-insensitive partial match. For example, "
            " passing 'astro' will match "
            "'astro', 'sad-Astro', and 'astro-robot'."
        ),
        example="astro",
    )


class BlockTypeFilterSlug(NebulaBaseModel):
    """Filter by `BlockType.slug`"""

    any_: Optional[List[str]] = Field(
        default=None, description="A list of slugs to match"
    )


class BlockTypeFilter(NebulaBaseModel):
    """Filter BlockTypes"""

    name: Optional[BlockTypeFilterName] = Field(
        default=None, description="Filter criteria for `BlockType.name`"
    )

    slug: Optional[BlockTypeFilterSlug] = Field(
        default=None, description="Filter criteria for `BlockType.slug`"
    )


class BlockSchemaFilterBlockTypeId(NebulaBaseModel):
    """Filter by `BlockSchema.block_type_id`."""

    any_: Optional[List[UUID]] = Field(
        default=None, description="A list of block type ids to include"
    )


class BlockSchemaFilterId(NebulaBaseModel):
    """Filter by BlockSchema.id"""

    any_: Optional[List[UUID]] = Field(
        default=None, description="A list of IDs to include"
    )


class BlockSchemaFilterCapabilities(NebulaBaseModel):
    """Filter by `BlockSchema.capabilities`"""

    all_: Optional[List[str]] = Field(
        default=None,
        example=["write-storage", "read-storage"],
        description=(
            "A list of block capabilities. Block entities will be returned only if an"
            " associated block schema has a superset of the defined capabilities."
        ),
    )


class BlockSchemaFilterVersion(NebulaBaseModel):
    """Filter by `BlockSchema.capabilities`"""

    any_: Optional[List[str]] = Field(
        default=None,
        example=["2.0.0", "2.1.0"],
        description="A list of block schema versions.",
    )


class BlockSchemaFilter(NebulaBaseModel, OperatorMixin):
    """Filter BlockSchemas"""

    block_type_id: Optional[BlockSchemaFilterBlockTypeId] = Field(
        default=None, description="Filter criteria for `BlockSchema.block_type_id`"
    )
    block_capabilities: Optional[BlockSchemaFilterCapabilities] = Field(
        default=None, description="Filter criteria for `BlockSchema.capabilities`"
    )
    id: Optional[BlockSchemaFilterId] = Field(
        default=None, description="Filter criteria for `BlockSchema.id`"
    )
    version: Optional[BlockSchemaFilterVersion] = Field(
        default=None, description="Filter criteria for `BlockSchema.version`"
    )


class BlockDocumentFilterIsAnonymous(NebulaBaseModel):
    """Filter by `BlockDocument.is_anonymous`."""

    eq_: Optional[bool] = Field(
        default=None,
        description=(
            "Filter block documents for only those that are or are not anonymous."
        ),
    )


class BlockDocumentFilterBlockTypeId(NebulaBaseModel):
    """Filter by `BlockDocument.block_type_id`."""

    any_: Optional[List[UUID]] = Field(
        default=None, description="A list of block type ids to include"
    )


class BlockDocumentFilterId(NebulaBaseModel):
    """Filter by `BlockDocument.id`."""

    any_: Optional[List[UUID]] = Field(
        default=None, description="A list of block ids to include"
    )


class BlockDocumentFilterName(NebulaBaseModel):
    """Filter by `BlockDocument.name`."""

    any_: Optional[List[str]] = Field(
        default=None, description="A list of block names to include"
    )
    like_: Optional[str] = Field(
        default=None,
        description=(
            "A string to match block names against. This can include "
            "SQL wildcard characters like `%` and `_`."
        ),
        example="my-block%",
    )


class BlockDocumentFilter(NebulaBaseModel, OperatorMixin):
    """Filter BlockDocuments. Only BlockDocuments matching all criteria will be returned"""

    id: Optional[BlockDocumentFilterId] = Field(
        default=None, description="Filter criteria for `BlockDocument.id`"
    )
    is_anonymous: Optional[BlockDocumentFilterIsAnonymous] = Field(
        # default is to exclude anonymous blocks
        BlockDocumentFilterIsAnonymous(eq_=False),
        description=(
            "Filter criteria for `BlockDocument.is_anonymous`. "
            "Defaults to excluding anonymous blocks."
        ),
    )
    block_type_id: Optional[BlockDocumentFilterBlockTypeId] = Field(
        default=None, description="Filter criteria for `BlockDocument.block_type_id`"
    )
    name: Optional[BlockDocumentFilterName] = Field(
        default=None, description="Filter criteria for `BlockDocument.name`"
    )


class FlowRunNotificationPolicyFilterIsActive(NebulaBaseModel):
    """Filter by `FlowRunNotificationPolicy.is_active`."""

    eq_: Optional[bool] = Field(
        default=None,
        description=(
            "Filter notification policies for only those that are or are not active."
        ),
    )


class FlowRunNotificationPolicyFilter(NebulaBaseModel):
    """Filter FlowRunNotificationPolicies."""

    is_active: Optional[FlowRunNotificationPolicyFilterIsActive] = Field(
        default=FlowRunNotificationPolicyFilterIsActive(eq_=False),
        description="Filter criteria for `FlowRunNotificationPolicy.is_active`. ",
    )


class WorkQueueFilterId(NebulaBaseModel):
    """Filter by `WorkQueue.id`."""

    any_: Optional[List[UUID]] = Field(
        default=None,
        description="A list of work queue ids to include",
    )


class WorkQueueFilterName(NebulaBaseModel):
    """Filter by `WorkQueue.name`."""

    any_: Optional[List[str]] = Field(
        default=None,
        description="A list of work queue names to include",
        example=["wq-1", "wq-2"],
    )

    startswith_: Optional[List[str]] = Field(
        default=None,
        description=(
            "A list of case-insensitive starts-with matches. For example, "
            " passing 'astro' will match "
            "'astro', and 'Astro-robot', but not 'sad-astro'."
        ),
        example=["astro", "Astro-robot"],
    )


class WorkQueueFilter(NebulaBaseModel, OperatorMixin):
    """Filter work queues. Only work queues matching all criteria will be
    returned"""

    id: Optional[WorkQueueFilterId] = Field(
        default=None, description="Filter criteria for `WorkQueue.id`"
    )

    name: Optional[WorkQueueFilterName] = Field(
        default=None, description="Filter criteria for `WorkQueue.name`"
    )


class WorkPoolFilterId(NebulaBaseModel):
    """Filter by `WorkPool.id`."""

    any_: Optional[List[UUID]] = Field(
        default=None, description="A list of work pool ids to include"
    )


class WorkPoolFilterName(NebulaBaseModel):
    """Filter by `WorkPool.name`."""

    any_: Optional[List[str]] = Field(
        default=None, description="A list of work pool names to include"
    )


class WorkPoolFilterType(NebulaBaseModel):
    """Filter by `WorkPool.type`."""

    any_: Optional[List[str]] = Field(
        default=None, description="A list of work pool types to include"
    )


class WorkPoolFilter(NebulaBaseModel, OperatorMixin):
    id: Optional[WorkPoolFilterId] = Field(
        default=None, description="Filter criteria for `WorkPool.id`"
    )
    name: Optional[WorkPoolFilterName] = Field(
        default=None, description="Filter criteria for `WorkPool.name`"
    )
    type: Optional[WorkPoolFilterType] = Field(
        default=None, description="Filter criteria for `WorkPool.type`"
    )


class WorkerFilterWorkPoolId(NebulaBaseModel):
    """Filter by `Worker.worker_config_id`."""

    any_: Optional[List[UUID]] = Field(
        default=None, description="A list of work pool ids to include"
    )


class WorkerFilterLastHeartbeatTime(NebulaBaseModel):
    """Filter by `Worker.last_heartbeat_time`."""

    before_: Optional[DateTimeTZ] = Field(
        default=None,
        description=(
            "Only include processes whose last heartbeat was at or before this time"
        ),
    )
    after_: Optional[DateTimeTZ] = Field(
        default=None,
        description=(
            "Only include processes whose last heartbeat was at or after this time"
        ),
    )


class WorkerFilter(NebulaBaseModel, OperatorMixin):
    # worker_config_id: Optional[WorkerFilterWorkPoolId] = Field(
    #     default=None, description="Filter criteria for `Worker.worker_config_id`"
    # )

    last_heartbeat_time: Optional[WorkerFilterLastHeartbeatTime] = Field(
        default=None,
        description="Filter criteria for `Worker.last_heartbeat_time`",
    )


class ArtifactFilterId(NebulaBaseModel):
    """Filter by `Artifact.id`."""

    any_: Optional[List[UUID]] = Field(
        default=None, description="A list of artifact ids to include"
    )


class ArtifactFilterKey(NebulaBaseModel):
    """Filter by `Artifact.key`."""

    any_: Optional[List[str]] = Field(
        default=None, description="A list of artifact keys to include"
    )

    like_: Optional[str] = Field(
        default=None,
        description=(
            "A string to match artifact keys against. This can include "
            "SQL wildcard characters like `%` and `_`."
        ),
        example="my-artifact-%",
    )

    exists_: Optional[bool] = Field(
        default=None,
        description=(
            "If `true`, only include artifacts with a non-null key. If `false`, "
            "only include artifacts with a null key."
        ),
    )


class ArtifactFilterFlowRunId(NebulaBaseModel):
    """Filter by `Artifact.flow_run_id`."""

    any_: Optional[List[UUID]] = Field(
        default=None, description="A list of flow run IDs to include"
    )


class ArtifactFilterTaskRunId(NebulaBaseModel):
    """Filter by `Artifact.task_run_id`."""

    any_: Optional[List[UUID]] = Field(
        default=None, description="A list of task run IDs to include"
    )


class ArtifactFilterType(NebulaBaseModel):
    """Filter by `Artifact.type`."""

    any_: Optional[List[str]] = Field(
        default=None, description="A list of artifact types to include"
    )
    not_any_: Optional[List[str]] = Field(
        default=None, description="A list of artifact types to exclude"
    )


class ArtifactFilter(NebulaBaseModel, OperatorMixin):
    """Filter artifacts. Only artifacts matching all criteria will be returned"""

    id: Optional[ArtifactFilterId] = Field(
        default=None, description="Filter criteria for `Artifact.id`"
    )
    key: Optional[ArtifactFilterKey] = Field(
        default=None, description="Filter criteria for `Artifact.key`"
    )
    flow_run_id: Optional[ArtifactFilterFlowRunId] = Field(
        default=None, description="Filter criteria for `Artifact.flow_run_id`"
    )
    task_run_id: Optional[ArtifactFilterTaskRunId] = Field(
        default=None, description="Filter criteria for `Artifact.task_run_id`"
    )
    type: Optional[ArtifactFilterType] = Field(
        default=None, description="Filter criteria for `Artifact.type`"
    )


class ArtifactCollectionFilterLatestId(NebulaBaseModel):
    """Filter by `ArtifactCollection.latest_id`."""

    any_: Optional[List[UUID]] = Field(
        default=None, description="A list of artifact ids to include"
    )


class ArtifactCollectionFilterKey(NebulaBaseModel):
    """Filter by `ArtifactCollection.key`."""

    any_: Optional[List[str]] = Field(
        default=None, description="A list of artifact keys to include"
    )

    like_: Optional[str] = Field(
        default=None,
        description=(
            "A string to match artifact keys against. This can include "
            "SQL wildcard characters like `%` and `_`."
        ),
        example="my-artifact-%",
    )

    exists_: Optional[bool] = Field(
        default=None,
        description=(
            "If `true`, only include artifacts with a non-null key. If `false`, "
            "only include artifacts with a null key. Should return all rows in "
            "the ArtifactCollection table if specified."
        ),
    )


class ArtifactCollectionFilterFlowRunId(NebulaBaseModel):
    """Filter by `ArtifactCollection.flow_run_id`."""

    any_: Optional[List[UUID]] = Field(
        default=None, description="A list of flow run IDs to include"
    )


class ArtifactCollectionFilterTaskRunId(NebulaBaseModel):
    """Filter by `ArtifactCollection.task_run_id`."""

    any_: Optional[List[UUID]] = Field(
        default=None, description="A list of task run IDs to include"
    )


class ArtifactCollectionFilterType(NebulaBaseModel):
    """Filter by `ArtifactCollection.type`."""

    any_: Optional[List[str]] = Field(
        default=None, description="A list of artifact types to include"
    )
    not_any_: Optional[List[str]] = Field(
        default=None, description="A list of artifact types to exclude"
    )


class ArtifactCollectionFilter(NebulaBaseModel, OperatorMixin):
    """Filter artifact collections. Only artifact collections matching all criteria will be returned"""

    latest_id: Optional[ArtifactCollectionFilterLatestId] = Field(
        default=None, description="Filter criteria for `Artifact.id`"
    )
    key: Optional[ArtifactCollectionFilterKey] = Field(
        default=None, description="Filter criteria for `Artifact.key`"
    )
    flow_run_id: Optional[ArtifactCollectionFilterFlowRunId] = Field(
        default=None, description="Filter criteria for `Artifact.flow_run_id`"
    )
    task_run_id: Optional[ArtifactCollectionFilterTaskRunId] = Field(
        default=None, description="Filter criteria for `Artifact.task_run_id`"
    )
    type: Optional[ArtifactCollectionFilterType] = Field(
        default=None, description="Filter criteria for `Artifact.type`"
    )


class VariableFilterId(NebulaBaseModel):
    """Filter by `Variable.id`."""

    any_: Optional[List[UUID]] = Field(
        default=None, description="A list of variable ids to include"
    )


class VariableFilterName(NebulaBaseModel):
    """Filter by `Variable.name`."""

    any_: Optional[List[str]] = Field(
        default=None, description="A list of variables names to include"
    )
    like_: Optional[str] = Field(
        default=None,
        description=(
            "A string to match variable names against. This can include "
            "SQL wildcard characters like `%` and `_`."
        ),
        example="my_variable_%",
    )


class VariableFilterValue(NebulaBaseModel):
    """Filter by `Variable.value`."""

    any_: Optional[List[str]] = Field(
        default=None, description="A list of variables value to include"
    )
    like_: Optional[str] = Field(
        default=None,
        description=(
            "A string to match variable value against. This can include "
            "SQL wildcard characters like `%` and `_`."
        ),
        example="my-value-%",
    )


class VariableFilterTags(NebulaBaseModel, OperatorMixin):
    """Filter by `Variable.tags`."""

    all_: Optional[List[str]] = Field(
        default=None,
        example=["tag-1", "tag-2"],
        description=(
            "A list of tags. Variables will be returned only if their tags are a"
            " superset of the list"
        ),
    )
    is_null_: Optional[bool] = Field(
        default=None, description="If true, only include Variables without tags"
    )


class VariableFilter(NebulaBaseModel, OperatorMixin):
    """Filter variables. Only variables matching all criteria will be returned"""

    id: Optional[VariableFilterId] = Field(
        default=None, description="Filter criteria for `Variable.id`"
    )
    name: Optional[VariableFilterName] = Field(
        default=None, description="Filter criteria for `Variable.name`"
    )
    value: Optional[VariableFilterValue] = Field(
        default=None, description="Filter criteria for `Variable.value`"
    )
    tags: Optional[VariableFilterTags] = Field(
        default=None, description="Filter criteria for `Variable.tags`"
    )
