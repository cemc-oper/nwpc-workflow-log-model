from nwpc_workflow_log_model.analytics.node_situation import NodeSituation
from nwpc_workflow_log_model.analytics.node_situation_dfa import (
    NodeSituationDFA, NodeStatus, SituationType
)


def test_node_situation_dfa():
    dfa = NodeSituationDFA(name="test")
    dfa.trigger(NodeStatus.queued.value)
    assert dfa.node_situation.state == SituationType.CurrentQueue.value

    dfa.trigger(NodeStatus.submitted.value)
    assert dfa.node_situation.state == SituationType.Submit.value

    dfa.trigger(NodeStatus.active.value)
    assert dfa.node_situation.state == SituationType.Active.value

    dfa.trigger(NodeStatus.complete.value)
    assert dfa.node_situation.state == SituationType.Complete.value
