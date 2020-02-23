import datetime
from abc import ABC, abstractmethod


from nwpc_workflow_model.node_status import NodeStatus


class NodeStatusChangeData(ABC):
    """
    节点状态变化数据的接口，指示某个时间点（date_time）节点变为新的状态（status）
    """
    @property
    @abstractmethod
    def date_time(self) -> datetime.datetime:
        pass

    @property
    @abstractmethod
    def status(self) -> NodeStatus:
        pass
