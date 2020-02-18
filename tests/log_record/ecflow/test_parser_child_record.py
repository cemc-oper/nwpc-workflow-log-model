from nwpc_workflow_log_model.log_record.ecflow import (
    EventType,
    EcflowLogParser,
    ChildLogRecord,
)


def test_init():
    line = "MSG:[13:33:57 8.1.2020] chd:init /grapes_reps_v3_2/06/members/mem09/pre_data/gmf_get/gmf_get_030"
    parser = EcflowLogParser()
    record = parser.parse(line)
    assert record is not None
    assert isinstance(record, ChildLogRecord)
    assert record.event_type == EventType.Child
    assert record.node_path == "/grapes_reps_v3_2/06/members/mem09/pre_data/gmf_get/gmf_get_030"
    assert record.command == "init"
    assert record.event == "init"


def test_complete():
    line = "MSG:[08:17:04 29.6.2018] chd:complete /gmf_grapes_025L60_v2.2_post/18/typhoon/post/tc_post"
    parser = EcflowLogParser()
    record = parser.parse(line)
    assert record is not None
    assert isinstance(record, ChildLogRecord)
    assert record.event_type == EventType.Child
    assert record.node_path == "/gmf_grapes_025L60_v2.2_post/18/typhoon/post/tc_post"
    assert record.command == "complete"
    assert record.event == "complete"
