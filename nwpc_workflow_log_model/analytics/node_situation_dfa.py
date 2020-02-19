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
        self._initial_transitions_for_init()
        self._initial_transitions_for_current_queue()
        self._initial_transitions_for_submit()
        self._initial_transitions_for_active()

    def _initial_transitions_for_init(self):
        source = SituationType.Initial.value
        self.machine.add_transition(
            trigger=NodeStatus.queued.value,
            source=source,
            dest=SituationType.CurrentQueue.value,
        )
        self.machine.add_transition(
            trigger=NodeStatus.complete.value,
            source=source,
            dest=source,
        )

    def _initial_transitions_for_current_queue(self):
        source = SituationType.CurrentQueue.value
        self.machine.add_transition(
            trigger=NodeStatus.submitted.value,
            source=source,
            dest=SituationType.Submit.value,
        )
        self.machine.add_transition(
            trigger=NodeStatus.aborted.value,
            source=source,
            dest=SituationType.Error.value,
        )
        self.machine.add_transition(
            trigger=NodeStatus.active.value,
            source=source,
            dest=SituationType.Active.value,
        )
        self.machine.add_transition(
            trigger=NodeStatus.complete.value,
            source=source,
            dest=SituationType.Unknown.value,
        )
        self.machine.add_transition(
            trigger=NodeStatus.queued.value,
            source=source,
            dest=SituationType.Unknown.value,
        )

    def _initial_transitions_for_submit(self):
        self.machine.add_transition(
            trigger=NodeStatus.active.value,
            source=SituationType.Submit.value,
            dest=SituationType.Active.value,
        )

    def _initial_transitions_for_active(self):
        self.machine.add_transition(
            trigger=NodeStatus.complete.value,
            source=SituationType.Active.value,
            dest=SituationType.Complete.value,
        )
