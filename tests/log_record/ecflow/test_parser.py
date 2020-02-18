from nwpc_workflow_log_model.log_record.ecflow import EcflowLogParser


def test_ecflow_parser():
    line = "LOG:[13:28:29 8.1.2020]  submitted: /gmf_grapes_gfs_post/06"
    parser = EcflowLogParser()
    record = parser.parse(line)
    assert record is not None
