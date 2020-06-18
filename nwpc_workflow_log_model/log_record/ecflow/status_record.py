import datetime

from loguru import logger

from nwpc_workflow_model.node_status import NodeStatus

from nwpc_workflow_log_model.analytics.node_status_change_data import NodeStatusChangeData
from .record import EcflowLogRecord, LogType, EventType


class StatusLogRecord(EcflowLogRecord):
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
        self.event_type: EventType = EventType.Status
        self.status: NodeStatus = NodeStatus.unknown

    def parse_record(
            self,
            status_line: str,
            debug: bool = False,
    ):
        """
        Parse status record

        Example:
            LOG:[13:34:07 8.1.2020]  complete: /grapes_reps_v3_2/06/control/pre_data/psi
            <EcflowLogParser.parse>  <-------   StatusLogRecord.parse_record   -------->

            LOG:[13:34:07 8.1.2020]  complete: /grapes_reps_v3_2/06/control/pre_data
            <EcflowLogParser.parse>  <-----   StatusLogRecord.parse_record   ------>

            LOG:[13:34:07 8.1.2020]  queued: /grapes_reps_v3_2/06/control
            <EcflowLogParser.parse>  <---StatusLogRecord.parse_record--->

            LOG:[17:38:08 28.1.2020]  submitted: /grapes_geps_v1_2/12/members/pair_06/mem02/geps2tigge/geps2tigge_054 job_size:31866
            < EcflowLogParser.parse > <--------------------------   StatusLogRecord.parse_record   -------------------------------->

        Parameters
        ----------
        status_line: str
            subset of log record line without log type and datetime, such as:
                complete: /grapes_reps_v3_2/06/control/pre_data/psi
                submitted: /grapes_geps_v1_2/12/members/pair_06/mem02/geps2tigge/geps2tigge_054 job_size:31866
        debug: bool
            show debug information
        """
        start_pos = 0
        end_pos = status_line.find(":", start_pos)
        if end_pos == -1:
            if status_line.strip()[0].isupper():
                if debug:
                    logger.warning(f"[WARNING] status record: event is ignored => {self.log_record}")
                pass
            else:
                if debug:
                    logger.error(f"[ERROR] status record: event not found => {self.log_record}")
                pass
            return
        event = status_line[start_pos:end_pos]

        if event in ("active", "queued", "complete"):
            self.event = event
            self.status = NodeStatus[event]
            start_pos = end_pos + 2
            end_pos = status_line.find(" ", start_pos)
            # assert end_pos == -1
            self.node_path = status_line[start_pos:end_pos].strip()
        elif event == "aborted":
            self.event = event
            self.status = NodeStatus[event]
            start_pos = end_pos + 2
            end_pos = status_line.find(" ", start_pos)
            if end_pos == -1:
                # LOG:[05:20:57 19.5.2020]  aborted: /meso_post/03/uploadAll
                self.node_path = status_line[start_pos:].strip()
            else:
                # LOG:[05:20:57 19.5.2020]  aborted: /meso_post/03/uploadAll/upload_chartos/3h/prep_3hr/upload_prep_3hr_020 try-no: 1 reason: trap
                # LOG:[04:35:14 9.2.2020]  aborted: /gmf_grapes_gfs_post/00/upload/ftp_togrib2/upload_togrib2_global/upload_togrib2_069 try-no: 2 reason: trap
                self.node_path = status_line[start_pos:end_pos]
                start_pos = end_pos + 1
                info = status_line[start_pos:].strip()
                try_no_start = info.find("try_no: ")
                reason_start = info.find("reason: ")
                try_no = int(info[try_no_start + 8:reason_start].strip())
                reason = info[reason_start + 8:].strip()
                self.additional_attrs["reason"] = reason
                self.additional_attrs["try_no"] = try_no
        elif event == "submitted":
            # LOG:[17:38:08 28.1.2020]  submitted: /grapes_geps_v1_2/12/members/pair_06/mem02/geps2tigge/geps2tigge_054 job_size:31866
            # LOG:[13:28:29 8.1.2020]  submitted: /gmf_grapes_gfs_post/06
            self.event = event
            self.status = NodeStatus[event]
            start_pos = end_pos + 2
            end_pos = status_line.find(" ", start_pos)
            if end_pos == -1:
                self.node_path = status_line[start_pos:]
            else:
                self.node_path = status_line[start_pos:end_pos]
                start_pos = end_pos + 1
                end_pos = status_line.find(":", start_pos)
                try:
                    self.additional_attrs["job_size"] = int(status_line[end_pos + 1:])
                except ValueError:
                    # LOG:[00:23:58 15.5.2020]  complete: /gmf_grapes_gfs_post/12/upload/ftp_togrib2/upload_togrib2_global/upload_togrib2_006
                    # LOG:[00:23:58 15.5.2020]  submitted: /gmf_grapes_gfs_post/12/upload/ftp_togrib2/upload_togrib2_global/upload_togrib2_054 job_size:9824MSG:[03:58:52 15.5.2020] Ecflow version(4.11.1) boost(1.53.0) compiler(gcc 4.8.5) protocol(TEXT_ARCHIVE) Compiled on Dec 25 2018 06:53:21
                    # MSG:[03:58:52 15.5.2020] Started at 2020-May-15 03:58:52 universal time
                    pass
        elif event in ("unknown",):
            self.status = NodeStatus[event]
            # just ignore
            pass
        elif event == "":
            # MSG:[04:39:45 18.7.2019]  :nwp
            pass
        elif event.strip()[0].isupper():
            pass
        elif event[0] == "[":
            # WAR:[09:16:14 8.8.2018]  [ overloaded || --abort*2 ] (pid & password match) : chd:abort
            #  : /grapes_emer_v1_1/12/plot/plot_wind : already aborted : action(fob)
            pass
        else:
            self.event = event
            if debug:
                logger.error(f"[ERROR] status record: event not supported =>  {self.log_record}")


@NodeStatusChangeData.register
class StatusChangeEntry(object):
    def __init__(self, record: StatusLogRecord):
        self._record = record

    @property
    def status(self) -> NodeStatus:
        return self._record.status

    @property
    def date_time(self) -> datetime.datetime:
        return datetime.datetime.combine(self._record.date, self._record.time)
