from .node_situation import (
    NodeSituation,
    SituationType,
    TimePoint,
    TimePeriodType,
    TimePeriod,
)
from .node_status_change_data import NodeStatusChangeData
from nwpc_workflow_model.node_status import NodeStatus

from transitions.extensions.diagrams import GraphMachine as Machine


class NodeStatusChangeDFA(object):
    states = [e for e in SituationType]

    def __init__(self, name):
        self.name = name
        self.node_situation = NodeSituation()
        self.machine = Machine(
            model=self,
            states=NodeStatusChangeDFA.states,
            initial=SituationType.Initial,
            after_state_change=self.change_node_situation_type,
        )

        self._current_cycle = {
            NodeStatus.submitted: None,
            NodeStatus.active: None,
            NodeStatus.complete: None,
            NodeStatus.aborted: None,
        }

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
        in_active = TimePeriod(
            period_type=TimePeriodType.InActive,
            start_time=self._current_cycle[NodeStatus.active],
            end_time=self._current_cycle[NodeStatus.complete],
        )
        submitted_time = self._current_cycle[NodeStatus.submitted]
        if submitted_time is None:
            in_all = TimePeriod(
                period_type=TimePeriodType.InAll,
                start_time=self._current_cycle[NodeStatus.active],
                end_time=self._current_cycle[NodeStatus.complete],
            )
            self.node_situation.time_periods.extend([
                in_all,
                in_active,
            ])
        else:
            in_all = TimePeriod(
                period_type=TimePeriodType.InAll,
                start_time=self._current_cycle[NodeStatus.submitted],
                end_time=self._current_cycle[NodeStatus.complete]
            )
            in_submitted = TimePeriod(
                period_type=TimePeriodType.InSubmitted,
                start_time=self._current_cycle[NodeStatus.submitted],
                end_time=self._current_cycle[NodeStatus.active]
            )
            self.node_situation.time_periods.extend([
                in_all,
                in_submitted,
                in_active,
            ])

    def change_node_situation_type(self, **kwargs):
        self.node_situation.situation = self.state

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
            before=self.add_node_data,
            after=self.enter_new_cycle,
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
            before=self.add_node_data,
            after=self.set_cycle_time_point,
        )

        self.machine.add_transition(
            trigger=NodeStatus.active.value,
            source=source,
            dest=SituationType.Active,
            before=self.add_node_data,
            after=self.set_cycle_time_point,
        )

        # aborted enters Error
        self.machine.add_transition(
            trigger=NodeStatus.aborted.value,
            source=source,
            dest=SituationType.Error,
            before=self.add_node_data,
            after=self.set_cycle_time_point,
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
            before=self.add_node_data,
            after=self.set_cycle_time_point,
        )

        self.machine.add_transition(
            trigger=NodeStatus.aborted.value,
            source=source,
            dest=SituationType.Error,
            before=self.add_node_data,
            after=self.set_cycle_time_point,
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
            before=self.add_node_data,
            after=[
                self.set_cycle_time_point,
                self.calculate_time_period,
            ],
        )

        self.machine.add_transition(
            trigger=NodeStatus.aborted.value,
            source=source,
            dest=SituationType.Error,
            before=self.add_node_data,
            after=self.set_cycle_time_point,
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
