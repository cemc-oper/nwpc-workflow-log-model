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
