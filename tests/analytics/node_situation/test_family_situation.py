from nwpc_workflow_log_model.analytics.family_status_change_dfa import (
    FamilyStatusChangeDFA, NodeStatus
)
from nwpc_workflow_log_model.analytics.situation_type import FamilySituationType


def test_family_situation_dfa():
    dfa = FamilyStatusChangeDFA(name="test")
    dfa.trigger(NodeStatus.queued.value)
    assert dfa.state is FamilySituationType.CurrentQueue
    assert dfa.node_situation.situation is FamilySituationType.CurrentQueue

    dfa.trigger(NodeStatus.submitted.value)
    assert dfa.state is FamilySituationType.CurrentRun
    assert dfa.node_situation.situation is FamilySituationType.CurrentRun

    dfa.trigger(NodeStatus.active.value)
    assert dfa.state is FamilySituationType.CurrentRun
    assert dfa.node_situation.situation is FamilySituationType.CurrentRun

    dfa.trigger(NodeStatus.submitted.value)
    assert dfa.state is FamilySituationType.CurrentRun
    assert dfa.node_situation.situation is FamilySituationType.CurrentRun

    dfa.trigger(NodeStatus.queued.value)
    assert dfa.state is FamilySituationType.CurrentRun
    assert dfa.node_situation.situation is FamilySituationType.CurrentRun

    dfa.trigger(NodeStatus.complete.value)
    assert dfa.state is FamilySituationType.Complete
    assert dfa.node_situation.situation is FamilySituationType.Complete


def test_family_situation_dfa_initial():
    dfa = FamilyStatusChangeDFA(name="test")
    assert dfa.state is FamilySituationType.Initial

    dfa.trigger(NodeStatus.complete.value)
    assert dfa.state is FamilySituationType.LastComplete

    dfa.trigger(NodeStatus.queued.value)
    assert dfa.state is FamilySituationType.CurrentQueue


def test_node_situation_dfa_unknown():
    dfa = FamilyStatusChangeDFA(name="test")
    dfa.machine.set_state(FamilySituationType.Unknown)

    assert dfa.state is FamilySituationType.Unknown

    dfa.trigger(NodeStatus.complete.value)
    assert dfa.state is FamilySituationType.Unknown

    dfa.trigger(NodeStatus.queued.value)
    assert dfa.state is FamilySituationType.Unknown

    dfa.trigger(NodeStatus.aborted.value)
    assert dfa.state is FamilySituationType.Unknown

    dfa.trigger(NodeStatus.submitted.value)
    assert dfa.state is FamilySituationType.Unknown

    dfa.trigger(NodeStatus.active.value)
    assert dfa.state is FamilySituationType.Unknown
