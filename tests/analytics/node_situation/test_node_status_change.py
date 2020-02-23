import datetime

from nwpc_workflow_log_model.analytics.node_situation import (
    NodeSituation,
    TimePoint,
    SituationType,
    NodeStatus,
)
from nwpc_workflow_log_model.analytics.node_status_change_data import NodeStatusChangeData
from nwpc_workflow_log_model.analytics.node_situation_dfa import NodeSituationDFA


@NodeStatusChangeData.register
class StatusChange(object):
    def __init__(self, status: NodeStatus, date_time: datetime.datetime):
        self.status = status
        self.date_time = date_time


def test_node_situation_dfa_change():
    dfa = NodeSituationDFA(name="test")

    change_to_queue_data = StatusChange(
        status=NodeStatus.queued,
        date_time=datetime.datetime(2020, 2, 23, 10, 0),
    )

    dfa.trigger(
        NodeStatus.queued.value,
        node_data=change_to_queue_data,
    )

    assert dfa.state is SituationType.CurrentQueue
    assert len(dfa.node_situation.time_points) == 1
    assert dfa.node_situation.time_points[0] == TimePoint(
        status=NodeStatus.queued,
        time=change_to_queue_data.date_time
    )

    change_to_submitted_data = StatusChange(
        status=NodeStatus.submitted,
        date_time=datetime.datetime(2020, 2, 23, 11, 0),
    )
    dfa.trigger(
        NodeStatus.submitted.value,
        node_data=change_to_submitted_data
    )
    assert dfa.state is SituationType.Submit
    assert len(dfa.node_situation.time_points) == 2
    assert dfa.node_situation.time_points[-1] == TimePoint(
        status=NodeStatus.submitted,
        time=change_to_submitted_data.date_time
    )

    change_to_active_data = StatusChange(
        status=NodeStatus.active,
        date_time=datetime.datetime(2020, 2, 23, 11, 1),
    )
    dfa.trigger(
        NodeStatus.active.value,
        node_data=change_to_active_data
    )
    assert dfa.state is SituationType.Active
    assert len(dfa.node_situation.time_points) == 3
    assert dfa.node_situation.time_points[-1] == TimePoint(
        status=NodeStatus.active,
        time=change_to_active_data.date_time
    )

    change_to_complete_data = StatusChange(
        status=NodeStatus.complete,
        date_time=datetime.datetime(2020, 2, 23, 11, 30),
    )
    dfa.trigger(
        NodeStatus.complete.value,
        node_data=change_to_complete_data
    )
    assert dfa.state is SituationType.Complete
    assert len(dfa.node_situation.time_points) == 4
    assert dfa.node_situation.time_points[-1] == TimePoint(
        status=NodeStatus.complete,
        time=change_to_complete_data.date_time
    )


def test_node_status_change_unknown():
    dfa = NodeSituationDFA(name="test")
    dfa.machine.set_state(SituationType.Unknown)

    assert dfa.state is SituationType.Unknown

    change_to_complete_data = StatusChange(
        status=NodeStatus.complete,
        date_time=datetime.datetime(2020, 2, 23, 11, 30),
    )
    dfa.trigger(
        NodeStatus.complete.value,
        node_data=change_to_complete_data
    )
    assert dfa.state is SituationType.Unknown
    assert len(dfa.node_situation.time_points) == 0
