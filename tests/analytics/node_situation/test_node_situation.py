from nwpc_workflow_log_model.analytics.node_situation_dfa import (
    NodeSituationDFA, NodeStatus, SituationType
)


def test_node_situation_dfa():
    dfa = NodeSituationDFA(name="test")
    dfa.trigger(NodeStatus.queued.value)
    assert dfa.state is SituationType.CurrentQueue

    dfa.trigger(NodeStatus.submitted.value)
    assert dfa.state is SituationType.Submit

    dfa.trigger(NodeStatus.active.value)
    assert dfa.state is SituationType.Active

    dfa.trigger(NodeStatus.complete.value)
    assert dfa.state is SituationType.Complete


def test_node_situation_dfa_initial():
    dfa = NodeSituationDFA(name="test")
    assert dfa.state is SituationType.Initial

    dfa.trigger(NodeStatus.complete.value)
    assert dfa.state is SituationType.Initial

    dfa.trigger(NodeStatus.queued.value)
    assert dfa.state is SituationType.CurrentQueue


def test_node_situation_dfa_unknown():
    dfa = NodeSituationDFA(name="test")
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
