from typing import Dict, List, Literal, Optional, Union
from uuid import UUID

from nebula.client.schemas.responses import MinimalConcurrencyLimitResponse
from nebula.events import Event, RelatedResource, emit_event


def _emit_concurrency_event(
    phase: Union[Literal["acquired"], Literal["released"]],
    primary_limit: MinimalConcurrencyLimitResponse,
    related_limits: List[MinimalConcurrencyLimitResponse],
    slots: int,
    follows: Union[Event, None] = None,
) -> Union[Event, None]:
    resource = {
        "nebula.resource.id": f"nebula.concurrency-limit.{primary_limit.id}",
        "nebula.resource.name": primary_limit.name,
        "slots-acquired": slots,
        "limit": primary_limit.limit,
    }

    related = [
        RelatedResource(
            __root__={
                "nebula.resource.id": f"nebula.concurrency-limit.{limit.id}",
                "nebula.resource.role": "concurrency-limit",
            }
        )
        for limit in related_limits
        if limit.id != primary_limit.id
    ]

    return emit_event(
        f"nebula.concurrency-limit.{phase}",
        resource=resource,
        related=related,
        follows=follows,
    )


def _emit_concurrency_acquisition_events(
    limits: List[MinimalConcurrencyLimitResponse],
    occupy: int,
) -> Dict[UUID, Optional[Event]]:
    events = {}
    for limit in limits:
        event = _emit_concurrency_event("acquired", limit, limits, occupy)
        events[limit.id] = event

    return events


def _emit_concurrency_release_events(
    limits: List[MinimalConcurrencyLimitResponse],
    occupy: int,
    events: Dict[UUID, Optional[Event]],
):
    for limit in limits:
        _emit_concurrency_event("released", limit, limits, occupy, events[limit.id])
