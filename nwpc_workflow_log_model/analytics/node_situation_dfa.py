from .node_situation import (
    NodeSituation,
    SituationType,
)
from nwpc_workflow_model.node_status import NodeStatus

from transitions import Machine


class NodeSituationDFA(object):
    states = [e.value for e in SituationType]

    def __init__(self, name):
        self.name = name
        self.node_situation = NodeSituation()
        self.machine = Machine(
            model=self.node_situation,
            states=NodeSituationDFA.states,
            initial=SituationType.Initial.value,
        )

        self._initial_transitions()

    def trigger(self, name: str):
        self.node_situation.trigger(name)

    def _initial_transitions(self):
        self.machine.add_transition(
            trigger=NodeStatus.queued.value,
            source=SituationType.Initial.value,
            dest=SituationType.CurrentQueue.value,
        )

        self.machine.add_transition(
            trigger=NodeStatus.submitted.value,
            source=SituationType.CurrentQueue.value,
            dest=SituationType.Submit.value,
        )
