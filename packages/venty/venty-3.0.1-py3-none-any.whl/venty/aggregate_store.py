from typing import Type

from venty import EventStore
from venty.event_store import append_events, read_stream_no_metadata
from venty.aggregate_root import AggregateRoot, AggregateUUID, AggregateRootT
from venty.strong_types import StreamName


def _entity_stream(
    entity_cls: Type[AggregateRoot], entity_id: AggregateUUID
) -> StreamName:
    return StreamName("{}-{}".format(entity_cls.entity_type(), entity_id))


class AggregateStore:
    def __init__(self, event_store: EventStore):
        self._event_store = event_store

    def store(self, entity: AggregateRoot):
        append_events(
            self._event_store,
            _entity_stream(type(entity), entity.aggregate_uuid),
            expected_version=entity.aggregate_version,
            events=entity.uncommitted_changes,
        )
        entity.mark_changes_as_committed()

    def load(
        self, entity_cls: Type[AggregateRootT], entity_id: AggregateUUID
    ) -> AggregateRootT:
        result: AggregateRoot = entity_cls()
        result.load_from_history(
            read_stream_no_metadata(
                self._event_store,
                _entity_stream(entity_cls, entity_id),
                stream_position=None,
            )
        )
        return result

    def fetch(self, entity: AggregateRootT) -> AggregateRootT:
        entity.load_from_history(
            read_stream_no_metadata(
                self._event_store,
                _entity_stream(type(entity), entity.aggregate_uuid),
                stream_position=entity.aggregate_version,
            )
        )
        return entity
