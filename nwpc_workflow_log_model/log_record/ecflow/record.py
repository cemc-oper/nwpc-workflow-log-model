from datetime import datetime

from loguru import logger

from nwpc_workflow_log_model.log_record.ecflow.util import EventType, convert_ecflow_log_type
from nwpc_workflow_log_model.log_record.log_record import LogRecord, LogType


class EcflowLogRecord(LogRecord):
    def __init__(
            self,
            log_type=LogType.Unknown,
            date=None,
            time=None,
            log_record=None):
        LogRecord.__init__(self)
        self.log_type = log_type
        self.log_record = log_record

        self.event_type: EventType = EventType.Unknown

    def parse(self, line: str):
        """
        NOTE
        ----
            ERR:[02:23:59 10.1.2020] Connection::handle_read_data, boost::archive::archive_exception unsupported version, in server
            ERR:[02:23:59 10.1.2020] 22 serialization::archive 17 0 0 0 1 2 8 CSyncCmd 1 0
            ERR:[02:23:59 10.1.2020] 0 0 0 0 0 4 root 2 0 0 0, in server
            ERR:[02:23:59 10.1.2020] Connection::handle_read_data archive version miss-match!, in server
        """
        self.log_record = line

        start_pos = 0
        end_pos = line.find(":")
        self._parse_log_type(line[start_pos:end_pos])

        start_pos = end_pos + 2
        end_pos = line.find("]", start_pos)
        if end_pos == -1:
            logger.warning("can't find date and time => ", line)
            return
        self._parse_datetime(line[start_pos:end_pos])

        start_pos = end_pos + 2
        if line[start_pos: start_pos + 1] == " ":
            self.event_type = EventType.Status
            start_pos += 1
            self._parse_status_record(line[start_pos:])
        elif line[start_pos: start_pos + 2] == "--":
            self.event_type = EventType.Client
            start_pos += 2
            self._parse_client_record(line[start_pos:])
        elif line[start_pos: start_pos + 4] == "chd:":
            # child event
            self.event_type = EventType.Child
            start_pos += 4
            self._parse_child_record(line[start_pos:])
        elif line[start_pos: start_pos + 4] == "svr:":
            # server
            # print("[server event]", line)
            self.event_type = EventType.Server
        elif len(line[start_pos:].strip()) > 0:
            # NOTE: line[start_pos].strip() will be empty but I haven't found example line.
            if line[start_pos:].strip()[0].isupper():
                # WAR:[09:00:08 6.8.2018] Job generation for task /grapes_emer_v1_1/00/plot/get_plot/get_plot_meso
                #  took 4593ms, Exceeds ECF_TASK_THRESHOLD(4000ms)
                pass
            else:
                pass
        else:
            # not supported
            # print("[not supported]", line)
            pass

        return self

    def _parse_log_type(self, token: str):
        self.log_type = convert_ecflow_log_type(token)

    def _parse_datetime(self, token: str):
        date_time = datetime.strptime(token, "%H:%M:%S %d.%m.%Y")
        self.date = date_time.date()
        self.time = date_time.time()

    def _parse_child_record(self, child_line: str):
        """
        Parse child line

        Example lines:
            MSG:[13:33:57 8.1.2020] chd:init /grapes_reps_v3_2/06/members/mem09/pre_data/gmf_get/gmf_get_030
            MSG:[14:02:38 8.1.2020] chd:meter fcstHours 0 /grapes_reps_v3_2/06/members/mem02/model/fcst_monitor

        Parameters
        ----------
        child_line: str

        Returns
        -------

        """
        start_pos = 0
        end_pos = child_line.find(" ", start_pos)
        if end_pos == -1:
            # print("[ERROR] child record: event not found =>", self.log_record)
            return
        event = child_line[start_pos:end_pos]
        self.event = event

        if event in ("init", "complete", "abort"):
            start_pos = end_pos + 2
            end_pos = child_line.find(" ", start_pos)
            if end_pos == -1:
                # MSG:[08:17:04 29.6.2018] chd:complete /gmf_grapes_025L60_v2.2_post/18/typhoon/post/tc_post
                self.node_path = child_line[start_pos:].strip()
            else:
                # MSG:[12:22:53 19.10.2018] chd:abort
                #  /3km_post/06/3km_togrib2/grib2WORK/030/after_data2grib2_030  trap
                self.node_path = child_line[start_pos:end_pos]
                self.additional_attrs["reason"] = child_line[end_pos + 1:]
        elif event in ("meter", "label", "event"):
            # MSG:[09:24:06 29.6.2018] chd:event transmissiondone
            #  /gmf_grapes_025L60_v2.2_post/00/tograph/base/015/AN_AEA/QFLXDIV_P700_AN_AEA_sep_015
            start_pos = end_pos + 1
            line = child_line[start_pos:]
            node_path_start_pos = line.rfind(" ")
            if node_path_start_pos != -1:
                self.node_path = line[node_path_start_pos + 1:]
                self.additional_attrs["event"] = line[:node_path_start_pos]
            else:
                # print("[ERROR] child record: parse error =>", self.log_record)
                pass
        else:
            logger.error("child record: event not supported =>", self.log_record)
