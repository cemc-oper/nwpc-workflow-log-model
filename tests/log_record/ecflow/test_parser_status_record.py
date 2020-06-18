import datetime

from nwpc_workflow_log_model.log_record.ecflow import (
    EventType,
    EcflowLogParser,
    StatusLogRecord,
)
from nwpc_workflow_log_model.log_record.ecflow.status_record import StatusChangeEntry

from nwpc_workflow_model.node_status import NodeStatus

from tests.log_record.ecflow._util import _check_attrs_value


def test_submit():
    line = "LOG:[13:28:29 8.1.2020]  submitted: /gmf_grapes_gfs_post/06"
    parser = EcflowLogParser()
    record = parser.parse(line)
    assert record is not None
    assert isinstance(record, StatusLogRecord)

    attrs = {
        "event_type": EventType.Status,
        "node_path": "/gmf_grapes_gfs_post/06",
        "status": NodeStatus.submitted,
        "event": "submitted",
    }
    _check_attrs_value(record, attrs)


def test_submit_with_job_size():
    line = "LOG:[17:38:08 28.1.2020]  submitted: /grapes_geps_v1_2/12/members/pair_06/mem02/geps2tigge/geps2tigge_054 job_size:31866"
    parser = EcflowLogParser()
    record = parser.parse(line)
    assert record is not None
    assert isinstance(record, StatusLogRecord)

    attrs = {
        "event_type": EventType.Status,
        "node_path": "/grapes_geps_v1_2/12/members/pair_06/mem02/geps2tigge/geps2tigge_054",
        "status": NodeStatus.submitted,
        "event": "submitted",
    }
    _check_attrs_value(record, attrs)

    assert record.additional_attrs["job_size"] == 31866


def test_aborted():
    line = "LOG:[05:20:57 19.5.2020]  aborted: /meso_post/03/uploadAll/upload_chartos/3h/prep_3hr/upload_prep_3hr_020 try-no: 1 reason: trap"
    parser = EcflowLogParser()
    record = parser.parse(line)
    assert record is not None
    assert isinstance(record, StatusLogRecord)

    attrs = {
        "event_type": EventType.Status,
        "node_path": "/meso_post/03/uploadAll/upload_chartos/3h/prep_3hr/upload_prep_3hr_020",
        "status": NodeStatus.aborted,
        "event": "aborted",
    }

    _check_attrs_value(record, attrs)

    assert record.additional_attrs["try_no"] == 1
    assert record.additional_attrs["reason"] == "trap"


def test_status_change_entry():
    line = "LOG:[13:28:29 8.1.2020]  submitted: /gmf_grapes_gfs_post/06"
    parser = EcflowLogParser()
    record = parser.parse(line)
    assert record is not None
    assert isinstance(record, StatusLogRecord)

    entry = StatusChangeEntry(record)

    assert entry.date_time == datetime.datetime(2020, 1, 8, 13, 28, 29)
    assert entry.status == NodeStatus.submitted
