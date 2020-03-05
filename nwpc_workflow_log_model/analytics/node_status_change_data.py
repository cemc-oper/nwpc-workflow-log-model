import datetime
from abc import ABC, abstractmethod


from nwpc_workflow_model.node_status import NodeStatus


class NodeStatusChangeData(ABC):
    """
    节点状态变化数据的接口，表示节点在某个时间点（date_time）变为新的状态（status: NodeStatus）
    """
    @property
    @abstractmethod
    def date_time(self) -> datetime.datetime:
        pass

    @property
    @abstractmethod
    def status(self) -> NodeStatus:
        pass
