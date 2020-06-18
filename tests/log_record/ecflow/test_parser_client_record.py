from nwpc_workflow_log_model.log_record.ecflow import (
    EventType,
    EcflowLogParser,
    ClientLogRecord,
)
from tests.log_record.ecflow._util import _check_attrs_value


def test_kill():
    line = "MSG:[16:52:50 8.2.2020] --kill /meso_post/12/uploadAll/upload_togrib2/027/upload_togrib2_027  :nwp"
    parser = EcflowLogParser()
    record = parser.parse(line)
    assert record is not None
    assert isinstance(record, ClientLogRecord)

    attrs = {
        "event_type": EventType.Client,
        "node_path": "/meso_post/12/uploadAll/upload_togrib2/027/upload_togrib2_027",
        "command": "kill",
        "event": "kill",
    }

    _check_attrs_value(record, attrs)


def test_requeue():
    line = "MSG:[07:50:49 31.1.2020] --requeue force /grapes_reps_v3_2/00/control/model/fcst_monitor  :nwp_qu"
    parser = EcflowLogParser()
    record = parser.parse(line)
    assert record is not None
    assert isinstance(record, ClientLogRecord)

    attrs = {
        "event_type": EventType.Client,
        "node_path": "/grapes_reps_v3_2/00/control/model/fcst_monitor",
        "command": "requeue",
        "event": "requeue",
        "user": "nwp_qu"
    }

    _check_attrs_value(record, attrs)

    assert record.additional_attrs["option"] == "force"
