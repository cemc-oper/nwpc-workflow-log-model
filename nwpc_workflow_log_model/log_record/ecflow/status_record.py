from .record import EcflowLogRecord, LogType, EventType
from nwpc_workflow_model.node_status import NodeStatus


class StatusLogRecord(EcflowLogRecord):
    def __init__(
            self,
            log_type=LogType.Unknown,
            date=None,
            time=None,
            log_record=None
    ):
        EcflowLogRecord.__init__(
            self,
            log_type=log_type,
            date=date,
            time=time,
            log_record=log_record
        )
        self.event_type = EventType.Status
        self.status = NodeStatus.unknown

    def parse_record(self, status_line: str):
        """
        Parse status record

        Example:
            LOG:[13:34:07 8.1.2020]  complete: /grapes_reps_v3_2/06/control/pre_data/psi
            LOG:[13:34:07 8.1.2020]  complete: /grapes_reps_v3_2/06/control/pre_data
            LOG:[13:34:07 8.1.2020]  queued: /grapes_reps_v3_2/06/control
            LOG:[17:38:08 28.1.2020]  submitted: /grapes_geps_v1_2/12/members/pair_06/mem02/geps2tigge/geps2tigge_054 job_size:31866

        Parameters
        ----------
        status_line: str

        Returns
        -------

        """
        start_pos = 0
        end_pos = status_line.find(":", start_pos)
        if end_pos == -1:
            if status_line.strip()[0].isupper():
                pass
            else:
                # print("[ERROR] status record: event not found =>", self.log_record)
                pass
            return
        event = status_line[start_pos:end_pos]

        if event in ("active", "queued", "complete", "aborted"):
            self.event = event
            self.status = NodeStatus[event]
            start_pos = end_pos + 2
            end_pos = status_line.find(" ", start_pos)
            if end_pos == -1:
                # LOG:[23:12:00 9.10.2018] queued: /grapes_meso_3km_post/18/tograph/1h/prep_1h_10mw
                self.node_path = status_line[start_pos:].strip()
            else:
                # LOG:[11:09:31 20.9.2018]  aborted: /grapes_meso_3km_post/06/tograph/3h/prep_3h_10mw/plot_hour_030 try-no: 1 reason: trap
                # LOG:[04:35:14 9.2.2020]  aborted: /gmf_grapes_gfs_post/00/upload/ftp_togrib2/upload_togrib2_global/upload_togrib2_069 try-no: 2 reason: trap
                self.node_path = status_line[start_pos:end_pos]
                self.additional_attrs["reason"] = status_line[end_pos + 1:]
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
                self.additional_attrs["job_size"] = int(status_line[end_pos + 1:])
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
            # print("[ERROR] status record: event not supported =>", self.log_record)
