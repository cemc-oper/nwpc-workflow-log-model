from nwpc_workflow_log_model.analytics.node_status_change_dfa import (
    NodeStatusChangeDFA, NodeStatus, SituationType
)


def test_node_situation_dfa():
    dfa = NodeStatusChangeDFA(name="test")
    dfa.trigger(NodeStatus.queued.value)
    assert dfa.state is SituationType.CurrentQueue
    assert dfa.node_situation.situation is SituationType.CurrentQueue

    dfa.trigger(NodeStatus.submitted.value)
    assert dfa.state is SituationType.Submit
    assert dfa.node_situation.situation is SituationType.Submit

    dfa.trigger(NodeStatus.active.value)
    assert dfa.state is SituationType.Active
    assert dfa.node_situation.situation is SituationType.Active

    dfa.trigger(NodeStatus.complete.value)
    assert dfa.state is SituationType.Complete
    assert dfa.node_situation.situation is SituationType.Complete


def test_node_situation_dfa_initial():
    dfa = NodeStatusChangeDFA(name="test")
    assert dfa.state is SituationType.Initial

    dfa.trigger(NodeStatus.complete.value)
    assert dfa.state is SituationType.Initial

    dfa.trigger(NodeStatus.queued.value)
    assert dfa.state is SituationType.CurrentQueue


def test_node_situation_dfa_unknown():
    dfa = NodeStatusChangeDFA(name="test")
    dfa.machine.set_state(SituationType.Unknown)

    assert dfa.state is SituationType.Unknown

    dfa.trigger(NodeStatus.complete.value)
    assert dfa.state is SituationType.Unknown

    dfa.trigger(NodeStatus.queued.value)
    assert dfa.state is SituationType.Unknown

    dfa.trigger(NodeStatus.aborted.value)
    assert dfa.state is SituationType.Unknown

    dfa.trigger(NodeStatus.submitted.value)
    assert dfa.state is SituationType.Unknown

    dfa.trigger(NodeStatus.active.value)
    assert dfa.state is SituationType.Unknown
