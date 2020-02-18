from nwpc_workflow_log_model.log_record.ecflow import (
    EventType,
    EcflowLogParser,
    StatusLogRecord,
)
from nwpc_workflow_model.node_status import NodeStatus


def test_submit():
    line = "LOG:[13:28:29 8.1.2020]  submitted: /gmf_grapes_gfs_post/06"
    parser = EcflowLogParser()
    record = parser.parse(line)
    assert record is not None
    assert isinstance(record, StatusLogRecord)
    assert record.event_type == EventType.Status
    assert record.status == NodeStatus.submitted
    assert record.node_path == "/gmf_grapes_gfs_post/06"


def test_submit_with_job_size():
    line = "LOG:[17:38:08 28.1.2020]  submitted: /grapes_geps_v1_2/12/members/pair_06/mem02/geps2tigge/geps2tigge_054 job_size:31866"
    parser = EcflowLogParser()
    record = parser.parse(line)
    assert record is not None
    assert isinstance(record, StatusLogRecord)
    assert record.event_type == EventType.Status
    assert record.status == NodeStatus.submitted
    assert record.node_path == "/grapes_geps_v1_2/12/members/pair_06/mem02/geps2tigge/geps2tigge_054"
    assert record.additional_attrs["job_size"] == 31866
