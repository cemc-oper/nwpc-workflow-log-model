from nwpc_workflow_log_model.analytics.task_status_change_dfa import (
    TaskStatusChangeDFA, NodeStatus
)
from nwpc_workflow_log_model.analytics.situation_type import TaskSituationType


def test_node_situation_dfa():
    dfa = TaskStatusChangeDFA(name="test")
    dfa.trigger(NodeStatus.queued.value)
    assert dfa.state is TaskSituationType.CurrentQueue
    assert dfa.node_situation.situation is TaskSituationType.CurrentQueue

    dfa.trigger(NodeStatus.submitted.value)
    assert dfa.state is TaskSituationType.Submit
    assert dfa.node_situation.situation is TaskSituationType.Submit

    dfa.trigger(NodeStatus.active.value)
    assert dfa.state is TaskSituationType.Active
    assert dfa.node_situation.situation is TaskSituationType.Active

    dfa.trigger(NodeStatus.complete.value)
    assert dfa.state is TaskSituationType.Complete
    assert dfa.node_situation.situation is TaskSituationType.Complete


def test_node_situation_dfa_initial():
    dfa = TaskStatusChangeDFA(name="test")
    assert dfa.state is TaskSituationType.Initial

    dfa.trigger(NodeStatus.complete.value)
    assert dfa.state is TaskSituationType.Initial

    dfa.trigger(NodeStatus.queued.value)
    assert dfa.state is TaskSituationType.CurrentQueue


def test_node_situation_dfa_unknown():
    dfa = TaskStatusChangeDFA(name="test")
    dfa.machine.set_state(TaskSituationType.Unknown)

    assert dfa.state is TaskSituationType.Unknown

    dfa.trigger(NodeStatus.complete.value)
    assert dfa.state is TaskSituationType.Unknown

    dfa.trigger(NodeStatus.queued.value)
    assert dfa.state is TaskSituationType.Unknown

    dfa.trigger(NodeStatus.aborted.value)
    assert dfa.state is TaskSituationType.Unknown

    dfa.trigger(NodeStatus.submitted.value)
    assert dfa.state is TaskSituationType.Unknown

    dfa.trigger(NodeStatus.active.value)
    assert dfa.state is TaskSituationType.Unknown
