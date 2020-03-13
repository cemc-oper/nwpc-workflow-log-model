from enum import Enum
from typing import List
import datetime

from nwpc_workflow_model.node_status import NodeStatus

from .situation_type import TaskSituationType


class TimePoint(object):
    """
    时间点，表示在某时间点（time）的状态（status）
    """
    def __init__(
            self,
            status: NodeStatus = NodeStatus.unknown,
            time: datetime.datetime = None
    ):
        self.status = status
        self.time = time

    def __eq__(self, other):
        return self.status == other.status and self.time == self.time


class TimePeriodType(Enum):
    """
    时间段类型
    """
    InSubmitted = "in_submitted"
    InActive = "in_active"
    InAll = "in_all"


class TimePeriod(object):
    """
    时间段
    """
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
    """
    节点运行状态，根据节点状态序列分析得到。
    """
    def __init__(
            self,
            situation: TaskSituationType = TaskSituationType.Initial,
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
