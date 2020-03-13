from transitions.extensions.diagrams import GraphMachine as Machine
from nwpc_workflow_model.node_status import NodeStatus

from .situation_type import FamilySituationType
from .node_situation import NodeSituation
from .node_status_change_data import NodeStatusChangeData
from .node_situation import TimePoint, TimePeriod, TimePeriodType


class FamilyStatusChangeDFA(object):
    states = [e for e in FamilySituationType]

    def __init__(self, name):
        self.name = name
        self.node_situation = NodeSituation()
        self.machine = Machine(
            model=self,
            states=FamilyStatusChangeDFA.states,
            initial=FamilySituationType.Initial,
            after_state_change=self.change_node_situation_type,
        )

        self._current_cycle = {
            NodeStatus.submitted: None,
            NodeStatus.active: None,
            NodeStatus.complete: None,
            NodeStatus.aborted: None,
        }

        self._initial_transitions()

    def change_node_situation_type(self, **kwargs):
        self.node_situation.situation = self.state

    def add_node_data(self, node_data: NodeStatusChangeData = None):
        if node_data is None:
            return
        self.node_situation.time_points.append(
            TimePoint(
                status=node_data.status,
                time=node_data.date_time,
            )
        )

    def enter_new_cycle(self, node_data: NodeStatusChangeData = None):
        if node_data is None:
            return
        self._current_cycle = {
            NodeStatus.submitted: None,
            NodeStatus.active: None,
            NodeStatus.complete: None,
            NodeStatus.aborted: None,
        }

    def set_cycle_time_point(self, node_data: NodeStatusChangeData = None):
        if node_data is None:
            return
        self._current_cycle[node_data.status] = node_data.date_time

    def calculate_time_period(self, **kwargs):
        begin_time = self._current_cycle[NodeStatus.submitted]
        if begin_time is None:
            begin_time = self._current_cycle[NodeStatus.active]

        in_all = TimePeriod(
            period_type=TimePeriodType.InAll,
            start_time=begin_time,
            end_time=self._current_cycle[NodeStatus.complete],
        )
        self.node_situation.time_periods.append(in_all)

    def _initial_transitions(self):
        self._initial_transitions_for_init()
        self._initial_transitions_for_last_complete()
        self._initial_transitions_for_current_queue()
        self._initial_transitions_for_current_run()
        self._initial_transitions_for_unknown()

    def _initial_transitions_for_init(self):
        source = FamilySituationType.Initial
        self.machine.add_transition(
            trigger=NodeStatus.complete.value,
            source=source,
            dest=FamilySituationType.LastComplete,
        )

        self.machine.add_transition(
            trigger=NodeStatus.queued.value,
            source=source,
            dest=FamilySituationType.CurrentQueue,
            before=self.add_node_data,
            after=self.enter_new_cycle,
        )

        self.machine.add_transition(
            trigger=NodeStatus.submitted.value,
            source=source,
            dest=FamilySituationType.CurrentRun,
            before=self.add_node_data,
            after=self.enter_new_cycle,
        )

        # all else is ignore.
        for t in (e.value for e in [
            NodeStatus.active,
            NodeStatus.complete,
            NodeStatus.aborted
        ]):
            self.machine.add_transition(
                trigger=t,
                source=source,
                dest="=",
            )

    def _initial_transitions_for_last_complete(self):
        source = FamilySituationType.LastComplete
        self.machine.add_transition(
            trigger=NodeStatus.queued.value,
            source=source,
            dest=FamilySituationType.CurrentQueue,
            before=self.add_node_data,
            after=self.enter_new_cycle,
        )

        # all else is unknown.
        for t in (e.value for e in [
            NodeStatus.submitted,
            NodeStatus.active,
            NodeStatus.complete,
            NodeStatus.aborted
        ]):
            self.machine.add_transition(
                trigger=t,
                source=source,
                dest=FamilySituationType.Unknown,
            )

    def _initial_transitions_for_current_queue(self):
        source = FamilySituationType.CurrentQueue
        self.machine.add_transition(
            trigger=NodeStatus.submitted.value,
            source=source,
            dest=FamilySituationType.CurrentRun,
            before=self.add_node_data,
            after=self.set_cycle_time_point,
        )

        self.machine.add_transition(
            trigger=NodeStatus.active.value,
            source=source,
            dest=FamilySituationType.CurrentRun,
            before=self.add_node_data,
            after=self.set_cycle_time_point,
        )

        # aborted enters Error
        self.machine.add_transition(
            trigger=NodeStatus.aborted.value,
            source=source,
            dest=FamilySituationType.Error,
            before=self.add_node_data,
            after=self.set_cycle_time_point,
        )

        # complete and queued enter Unknown
        for s in (NodeStatus.complete, NodeStatus.queued):
            self.machine.add_transition(
                trigger=s.value,
                source=source,
                dest=FamilySituationType.Unknown,
            )

    def _initial_transitions_for_current_run(self):
        source = FamilySituationType.CurrentRun
        self.machine.add_transition(
            trigger=NodeStatus.complete.value,
            source=source,
            dest=FamilySituationType.Complete,
            before=self.add_node_data,
            after=[
                self.set_cycle_time_point,
                self.calculate_time_period,
            ],
        )

        self.machine.add_transition(
            trigger=NodeStatus.aborted.value,
            source=source,
            dest=FamilySituationType.Error,
            before=self.add_node_data,
            after=[
                self.set_cycle_time_point,
            ],
        )

        # all else is ignore.
        for t in (e.value for e in [
            NodeStatus.queued,
            NodeStatus.submitted,
            NodeStatus.active,
        ]):
            self.machine.add_transition(
                trigger=t,
                source=source,
                dest="=",
            )

    def _initial_transitions_for_unknown(self):
        source = FamilySituationType.Unknown
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

