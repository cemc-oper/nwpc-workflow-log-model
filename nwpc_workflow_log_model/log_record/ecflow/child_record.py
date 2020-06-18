import datetime

from loguru import logger

from .record import EcflowLogRecord, LogType, EventType


class ChildLogRecord(EcflowLogRecord):
    def __init__(
            self,
            log_type: LogType = LogType.Unknown,
            date: datetime.date = None,
            time: datetime.time = None,
            log_record: str = None,
    ):
        EcflowLogRecord.__init__(
            self,
            log_type=log_type,
            date=date,
            time=time,
            log_record=log_record
        )
        self.event_type: EventType = EventType.Child
        self.command: str or None = None

    def parse_record(
            self,
            line: str,
            debug: bool = False,
    ):
        """
        Parse child command log record.

        Example lines:
            MSG:[13:33:57 8.1.2020] chd:init /grapes_reps_v3_2/06/members/mem09/pre_data/gmf_get/gmf_get_030
            <- EcflowLogParser.parse -> <----------------   ChildLogRecord.parse_record   ----------------->
            MSG:[14:02:38 8.1.2020] chd:meter fcstHours 0 /grapes_reps_v3_2/06/members/mem02/model/fcst_monitor
            <- EcflowLogParser.parse -> <-----------------   ChildLogRecord.parse_record   ------------------->

        Parameters
        ----------
        line: str
            part of log line after 'chd:', such as
                "init /grapes_reps_v3_2/06/members/mem09/pre_data/gmf_get/gmf_get_030"

        debug: bool
            show debug information

        Examples
        --------

        >>> log_line = "MSG:[13:33:57 8.1.2020] chd:init /grapes_reps_v3_2/06/members/mem09/pre_data/gmf_get/gmf_get_030"
        >>> log_line[28:]
        'init /grapes_reps_v3_2/06/members/mem09/pre_data/gmf_get/gmf_get_030'
        >>> record = ChildLogRecord()
        >>> record.parse_record(log_line[28:])
        >>> record.event
        'init'
        >>> record.node_path
        '/grapes_reps_v3_2/06/members/mem09/pre_data/gmf_get/gmf_get_030'

        """
        start_pos = 0
        end_pos = line.find(" ", start_pos)
        if end_pos == -1:
            if debug:
                logger.error(f"[ERROR] child record: event not found => {self.log_record}")
            return
        event = line[start_pos:end_pos]
        self.event = event
        self.command = self.event

        if event in ("init", "complete", "abort"):
            start_pos = end_pos + 1
            end_pos = line.find(" ", start_pos)
            if end_pos == -1:
                # MSG:[08:17:04 29.6.2018] chd:complete /gmf_grapes_025L60_v2.2_post/18/typhoon/post/tc_post
                self.node_path = line[start_pos:].strip()
            else:
                # MSG:[12:22:53 19.10.2018] chd:abort /3km_post/06/3km_togrib2/grib2WORK/030/after_data2grib2_030  trap
                self.node_path = line[start_pos:end_pos]
                self.additional_attrs["reason"] = line[end_pos + 1:]
        elif event == "event":
            # MSG:[13:23:49 14.5.2020] chd:event unavailable /obs_rafs/09/pre_data/radar/SASB/9311/read
            start_pos = end_pos + 1
            line = line[start_pos:]
            tokens = line.split(" ")
            if len(tokens) == 2:
                self.node_path = tokens[1]
                self.additional_attrs["name"] = tokens[0]
            else:
                if debug:
                    logger.debug(f"[ERROR] child record: parse error => {self.log_record}")
                pass
        elif event == "meter":
            # MSG:[13:39:38 14.5.2020] chd:meter forecastHours 12 /grapes_tym/grapes_d01/06/model/grapes_monitor
            start_pos = end_pos + 1
            line = line[start_pos:]
            tokens = line.split(" ")
            if len(tokens) == 3:
                self.node_path = tokens[2]
                self.additional_attrs["name"] = tokens[0]
                self.additional_attrs["value"] = int(tokens[1])
            else:
                if debug:
                    logger.error(f"[ERROR] child record: parse error => {self.log_record}")
                pass
        elif event == "label":
            # MSG:[13:56:02 14.5.2020] chd:label info 'checking for 066...' /gmf_grapes_gfs_post/06/initial_togrib2
            start_pos = end_pos + 1
            line = line[start_pos:]
            line = line.rstrip()
            name_end_pos = line.find(" ")
            self.additional_attrs["name"] = line[:name_end_pos]
            node_start_pos = line.rfind(" ")
            self.node_path = line[node_start_pos+1:]
            self.additional_attrs["value"] = line[name_end_pos+2: node_start_pos-1]
        else:
            logger.error("child record: event not supported =>", self.log_record)
