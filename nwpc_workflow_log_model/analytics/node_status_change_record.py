import datetime
from abc import ABC, abstractmethod


from nwpc_workflow_model.node_status import NodeStatus


class NodeStatusChangeRecord(ABC):
    @property
    @abstractmethod
    def date_time(self) -> datetime.datetime:
        pass

    @property
    @abstractmethod
    def status(self) -> NodeStatus:
        pass
