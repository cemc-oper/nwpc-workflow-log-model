import datetime

from nwpc_workflow_log_model.analytics.node_situation import (
    NodeSituation,
    TimePoint,
    TimePeriodType,
    NodeStatus,
)
from nwpc_workflow_log_model.analytics.situation_type import FamilySituationType
from nwpc_workflow_log_model.analytics.node_status_change_data import NodeStatusChangeData
from nwpc_workflow_log_model.analytics.family_status_change_dfa import FamilyStatusChangeDFA


@NodeStatusChangeData.register
class StatusChange(object):
    def __init__(self, status: NodeStatus, date_time: datetime.datetime):
        self.status = status
        self.date_time = date_time


def test_family_situation_dfa_change():
    dfa = FamilyStatusChangeDFA(name="test")

    change_to_queue_data = StatusChange(
        status=NodeStatus.queued,
        date_time=datetime.datetime(2020, 2, 23, 10, 0),
    )

    dfa.trigger(
        change_to_queue_data.status.value,
        node_data=change_to_queue_data,
    )

    assert dfa.state is FamilySituationType.CurrentQueue
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
        change_to_submitted_data.status.value,
        node_data=change_to_submitted_data
    )
    assert dfa.state is FamilySituationType.CurrentRun
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
        change_to_active_data.status.value,
        node_data=change_to_active_data
    )
    assert dfa.state is FamilySituationType.CurrentRun
    assert len(dfa.node_situation.time_points) == 2
    assert dfa.node_situation.time_points[-1] == TimePoint(
        status=NodeStatus.submitted,
        time=change_to_submitted_data.date_time
    )

    change_to_complete_data = StatusChange(
        status=NodeStatus.complete,
        date_time=datetime.datetime(2020, 2, 23, 11, 30),
    )
    dfa.trigger(
        change_to_complete_data.status.value,
        node_data=change_to_complete_data
    )
    assert dfa.state is FamilySituationType.Complete
    assert len(dfa.node_situation.time_points) == 3
    assert dfa.node_situation.time_points[-1] == TimePoint(
        status=NodeStatus.complete,
        time=change_to_complete_data.date_time
    )

    node_situation = dfa.node_situation
    assert len(node_situation.time_periods) == 1

    in_all = list(filter(
        lambda x: x.period_type == TimePeriodType.InAll, node_situation.time_periods
    ))
    assert len(in_all) == 1
    in_all = in_all[0]
    assert in_all.start_time == change_to_submitted_data.date_time
    assert in_all.end_time == change_to_complete_data.date_time
