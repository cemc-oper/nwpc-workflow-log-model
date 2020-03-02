# coding: utf-8
import logging

from sqlalchemy import Column, String
from nwpc_workflow_log_model.rmdb.base.model import Model
from nwpc_workflow_log_model.rmdb.base.record import RecordBase
from nwpc_workflow_log_model.log_record.ecflow import EcflowLogRecord, EcflowLogParser

logger = logging.getLogger()


class EcflowRecordBase(RecordBase):
    command_type = Column(String(10))

    def parse(self, line):
        parser = EcflowLogParser()
        record = parser.parse(line)

        attrs = [
            'log_type',
            'date',
            'time',
            'event',
            'node_path',
            # 'additional_information', # TODO: add information.
            'log_record',
            'event_type',
        ]
        for an_attr in attrs:
            setattr(self, an_attr, getattr(record, an_attr))


class EcflowRecord(EcflowRecordBase, Model):
    __tablename__ = "ecflow_record"

    def __init__(self):
        pass
