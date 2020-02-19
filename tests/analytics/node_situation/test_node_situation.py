from nwpc_workflow_log_model.analytics.node_situation import NodeSituation
from nwpc_workflow_log_model.analytics.node_situation_dfa import (
    NodeSituationDFA, NodeStatus, SituationType
)


def test_node_situation_dfa():
    dfa = NodeSituationDFA(name="test")
    dfa.node_situation.trigger(NodeStatus.queued.value)
    assert dfa.node_situation.state == SituationType.CurrentQueue.value

    dfa.node_situation.trigger(NodeStatus.submitted.value)
    assert dfa.node_situation.state == SituationType.Submit.value
