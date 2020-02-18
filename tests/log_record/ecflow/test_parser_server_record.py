from nwpc_workflow_log_model.log_record.ecflow import (
    EventType,
    EcflowLogParser,
    ServerLogRecord,
)


def test_check_pt():
    line = "MSG:[05:41:25 2.2.2020] svr:check_pt in 0 seconds"
    parser = EcflowLogParser()
    record = parser.parse(line)
    assert record is not None
    assert isinstance(record, ServerLogRecord)
    assert record.event_type == EventType.Server
    assert record.command == "check_pt"
    assert record.event == "check_pt"
