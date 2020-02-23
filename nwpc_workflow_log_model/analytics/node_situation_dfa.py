from .node_situation import (
    NodeSituation,
    SituationType,
    TimePoint,
)
from .node_status_change_data import NodeStatusChangeData
from nwpc_workflow_model.node_status import NodeStatus

from transitions.extensions.diagrams import GraphMachine as Machine


class NodeSituationDFA(object):
    states = [e for e in SituationType]

    def __init__(self, name):
        self.name = name
        self.node_situation = NodeSituation()
        self.machine = Machine(
            model=self,
            states=NodeSituationDFA.states,
            initial=SituationType.Initial,
        )

        self._initial_transitions()

    def add_node_data(self, node_data: NodeStatusChangeData = None):
        if node_data is None:
            return
        self.node_situation.time_points.append(
            TimePoint(
                status=node_data.status,
                time=node_data.date_time,
            )
        )

    def _initial_transitions(self):
        self._initial_transitions_for_init()
        self._initial_transitions_for_current_queue()
        self._initial_transitions_for_submit()
        self._initial_transitions_for_active()
        self._initial_transitions_for_unknown()

    def _initial_transitions_for_init(self):
        source = SituationType.Initial
        # queue enters CurrentQueue
        self.machine.add_transition(
            trigger=NodeStatus.queued.value,
            source=source,
            dest=SituationType.CurrentQueue,
            before="add_node_data",
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
            before="add_node_data",
        )
        self.machine.add_transition(
            trigger=NodeStatus.active.value,
            source=source,
            dest=SituationType.Active,
            before="add_node_data",
        )

        # aborted enters Error
        self.machine.add_transition(
            trigger=NodeStatus.aborted.value,
            source=source,
            dest=SituationType.Error,
            before="add_node_data",
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
            before="add_node_data",
        )

        self.machine.add_transition(
            trigger=NodeStatus.aborted.value,
            source=source,
            dest=SituationType.Error,
            before="add_node_data",
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
            before="add_node_data",
        )

        self.machine.add_transition(
            trigger=NodeStatus.aborted.value,
            source=source,
            dest=SituationType.Error,
            before="add_node_data",
        )

        for s in (NodeStatus.submitted, NodeStatus.queued, NodeStatus.active):
            self.machine.add_transition(
                trigger=s.value,
                source=source,
                dest=SituationType.Unknown,
            )

    def _initial_transitions_for_unknown(self):
        source = SituationType.Unknown
        for t in (e.name for e in [
            NodeStatus.queued,
            NodeStatus.submitted,
            NodeStatus.active,
            NodeStatus.complete,
            NodeStatus.aborted
        ]):
            self.machine.add_transition(
                trigger=t,
                source=source,
                dest=source,
            )
