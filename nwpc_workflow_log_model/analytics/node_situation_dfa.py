from .node_situation import (
    NodeSituation,
    SituationType,
)
from nwpc_workflow_model.node_status import NodeStatus

from transitions.extensions.diagrams import GraphMachine as Machine


class NodeSituationDFA(object):
    states = [e for e in SituationType]

    def __init__(self, name):
        self.name = name
        self.node_situation = NodeSituation()
        self.machine = Machine(
            model=self.node_situation,
            states=NodeSituationDFA.states,
            initial=SituationType.Initial,
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
        source = SituationType.Initial
        # queue enters CurrentQueue
        self.machine.add_transition(
            trigger=NodeStatus.queued.value,
            source=source,
            dest=SituationType.CurrentQueue,
        )

        # complete is ignore.
        self.machine.add_transition(
            trigger=NodeStatus.complete.value,
            source=source,
            dest="=",
        )

    def _initial_transitions_for_current_queue(self):
        source = SituationType.CurrentQueue
        self.machine.add_transition(
            trigger=NodeStatus.submitted.value,
            source=source,
            dest=SituationType.Submit,
        )
        self.machine.add_transition(
            trigger=NodeStatus.active.value,
            source=source,
            dest=SituationType.Active,
        )

        # aborted enters Error
        self.machine.add_transition(
            trigger=NodeStatus.aborted.value,
            source=source,
            dest=SituationType.Error,
        )

        # complete and queued enter Unknown
        for s in (NodeStatus.complete, NodeStatus.queued):
            self.machine.add_transition(
                trigger=s.value,
                source=source,
                dest=SituationType.Unknown,
            )

    def _initial_transitions_for_submit(self):
        source = SituationType.Submit

        self.machine.add_transition(
            trigger=NodeStatus.active.value,
            source=source,
            dest=SituationType.Active,
        )

        self.machine.add_transition(
            trigger=NodeStatus.aborted.value,
            source=source,
            dest=SituationType.Error,
        )

        for s in (NodeStatus.complete, NodeStatus.queued, NodeStatus.submitted):
            self.machine.add_transition(
                trigger=s.value,
                source=source,
                dest=SituationType.Unknown,
            )

    def _initial_transitions_for_active(self):
        source = SituationType.Active

        self.machine.add_transition(
            trigger=NodeStatus.complete.value,
            source=source,
            dest=SituationType.Complete,
        )

        self.machine.add_transition(
            trigger=NodeStatus.aborted.value,
            source=source,
            dest=SituationType.Error,
        )

        for s in (NodeStatus.submitted, NodeStatus.queued, NodeStatus.active):
            self.machine.add_transition(
                trigger=s.value,
                source=source,
                dest=SituationType.Unknown,
            )
