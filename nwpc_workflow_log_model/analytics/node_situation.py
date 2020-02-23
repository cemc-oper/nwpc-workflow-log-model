from enum import Enum
from typing import List
import datetime

from nwpc_workflow_model.node_status import NodeStatus


class SituationType(Enum):
    Initial = "initial"
    CurrentQueue = "current_queue"
    Submit = "submit"
    Active = "active"
    Complete = "complete"
    Error = "error"
    Unknown = "unknown"


class TimePeriodType(Enum):
    InSubmitted = "in_submitted"
    InActive = "in_active"
    InAll = "in_all"


class TimePoint(object):
    def __init__(
            self,
            status: NodeStatus = NodeStatus.unknown,
            time: datetime.datetime = None
    ):
        self.status = status
        self.time = time

    def __eq__(self, other):
        return self.status == other.status and self.time == self.time


class TimePeriod(object):
    def __init__(
            self,
            period_type: TimePeriodType = None,
            start_time: datetime.datetime = None,
            end_time: datetime.datetime = None,
    ):
        self.period_type = period_type
        self.start_time = start_time
        self.end_time = end_time


class NodeSituation(object):
    def __init__(
            self,
            situation: SituationType = SituationType.Initial,
            time_points: List[TimePoint] = None,
            time_periods: List[TimePeriod] = None,
    ):
        self.situation = situation

        if time_points is None:
            time_points = list()
        self.time_points = time_points

        if time_periods is None:
            time_periods = list()
        self.time_periods = time_periods
