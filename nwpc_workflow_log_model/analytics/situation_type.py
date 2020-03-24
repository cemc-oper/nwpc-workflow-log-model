from enum import Enum


class TaskSituationType(Enum):
    """
    Task节点的运行状态

    Notes
    -----
    与节点状态``NodeStatus``不同，来自于对节点状态``NodeStatus``序列的分析
    """
    Initial = "initial"  # 初始状态
    CurrentQueue = "current_queue"  # 每次循环的开始
    Submit = "submit"  # 提交
    Active = "active"  # 运行
    Complete = "complete"  # 正常结束
    Error = "error"  # 运行出错
    Unknown = "unknown"  # 未知状态


class FamilySituationType(Enum):
    """
    Family节点的运行状态
    """
    Initial = "initial"  # initial situation, means nothing.
    LastComplete = "last_complete"  # complete situation of previous cycle, usually cycle run for last day.
    CurrentQueue = "current_queue"  # queue for current day's cycle.
    CurrentRun = "current_run"  # run for current day.
    Complete = "complete"  # first complete for current day
    Error = "error"
    Unknown = "unknown"
