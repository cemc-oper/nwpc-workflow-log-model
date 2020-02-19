from nwpc_workflow_log_model.analytics.node_situation_dfa import NodeSituationDFA

dfa = NodeSituationDFA("ecflow")

dfa.node_situation.get_graph().draw('my_state_diagram.png', prog='dot')
