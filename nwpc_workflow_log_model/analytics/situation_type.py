from enum import Enum


class TaskSituationType(Enum):
    """
    Running situation of Task node

    Notes
    -----
    Different from node status ``NodeStatus``, task situation is computed from a sequence ``NodeStatus``.
    """
    Initial = "initial"  # initial situation
    CurrentQueue = "current_queue"  # start of current cycle
    Submit = "submit"
    Active = "active"
    Complete = "complete"  #
    Error = "error"  # There is some error.
    Unknown = "unknown"  # There is some unknown situation.


class FamilySituationType(Enum):
    """
    Running situation of Family node
    """
    Initial = "initial"  # initial situation, means nothing.
    LastComplete = "last_complete"  # complete situation of previous cycle, usually cycle run for last day.
    CurrentQueue = "current_queue"  # queue for current day's cycle.
    CurrentRun = "current_run"  # run for current day.
    Complete = "complete"  # first complete for current day
    Error = "error"
    Unknown = "unknown"
