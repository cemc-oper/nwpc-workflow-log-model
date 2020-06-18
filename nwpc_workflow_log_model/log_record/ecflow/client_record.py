import datetime

from loguru import logger

from .record import EcflowLogRecord, LogType, EventType


class ClientLogRecord(EcflowLogRecord):
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
        self.event_type: EventType = EventType.Client
        self.command: str or None = None
        self.user: str or None = None

    def parse_record(
            self,
            line: str,
            debug: bool = False,
    ):
        """
        Parse client record

        Example
            MSG:[06:35:57 12.1.2020] --force=complete /grapes_geps_v1_2/00/members/pair_05/mem02/model/forecast  :nwp
            < EcflowLogParser.parse ><----------------------   ClientLogRecord.parse_record  ----------------------->

            MSG:[13:30:29 8.1.2020] --news=0 1 0  :nwp [:NO_NEWS]
            <EcflowLogParser.parse> <ClientLogRecord.parse_record>

            MSG:[13:30:35 8.1.2020] --server_version :nwp
            MSG:[13:30:35 8.1.2020] --sync_full=0 :nwp

        Parameters
        ----------
        line: str
        debug: bool

        """
        start_pos = 0
        end_pos = line.find(" ", start_pos)
        if end_pos == -1:
            if debug:
                logger.error(f"client record: event not found => {self.log_record}")
            return
        event = line[start_pos:end_pos]

        user_start_pos = line.rfind(":")
        if user_start_pos == -1:
            if debug:
                logger.error(f"client record: user not found => {self.log_record}")
        else:
            self.user = line[user_start_pos+1:].strip()

        if event == "requeue":
            # MSG:[07:50:49 31.1.2020] --requeue force /grapes_reps_v3_2/00/control/model/fcst_monitor  :nwp_qu
            # MSG:[02:06:46 9.6.2020] --requeue force /grapes_tym_post/12/data/000/shanxi /grapes_tym_post/12/data/001/shanxi /grapes_tym_post/12/data/002/shanxi /grapes_tym_post/12/data/003/shanxi /grapes_tym_post/12/data/004/shanxi /grapes_tym_post/12/data/005/shanxi /grapes_tym_post/12/data/006/shanxi /grapes_tym_post/12/data/007/shanxi /grapes_tym_post/12/data/008/shanxi /grapes_tym_post/12/data/009/shanxi  :nwp_pd
            # MSG:[02:36:55 27.5.2020] --requeue force /meso_post/00/meso_chartos/rundir_area_1h/prep_1hr_10mw/prep_1hr_10mw_037 /meso_post/00/meso_chartos/rundir_area_1h/prep_1hr_10mw/prep_1hr_10mw_038  :nwp_pd
            self.event = event
            start_pos = end_pos + 1
            tokens = line[start_pos:].split()
            if len(tokens) >= 3:
                requeue_option = tokens[0]
                node_path = tokens[1:-1]
                if len(node_path) == 1:
                    self.node_path = node_path[0]
                else:
                    self.node_path = node_path
                self.additional_attrs["option"] = requeue_option
            else:
                if debug:
                    logger.error(f"client record: requeue parse error => {self.log_record}")
                return
        elif event in (
                "alter",
                "free-dep",
                "kill",
                "delete",
                "suspend",
                "resume",
                "run",
                "status",
        ):
            # MSG:[06:45:59 12.1.2020] --alter change meter fcstHours 360 /grapes_geps_v1_2/00/members/pair_15/mem01/model/fcst_monitor  :nwp
            # MSG:[16:52:50 8.2.2020] --kill /meso_post/12/uploadAll/upload_togrib2/027/upload_togrib2_027  :nwp
            self.event = event
            start_pos = end_pos + 1
            tokens = line[start_pos:].split()
            node_path = tokens[-2]
            self.node_path = node_path
            self.additional_attrs["options"] = tokens[:-2]
        elif event.startswith("force="):
            # MSG:[05:55:30 9.2.2020] --force=complete recursive /grapes_meso_3km_post/12  :nwp_pd
            # LOG:[05:55:30 9.2.2020]  complete: /grapes_meso_3km_post/12
            # LOG:[05:55:30 9.2.2020]  complete: /grapes_meso_3km_post/12/initial
            self.event = "force"
            start_pos = end_pos + 1
            tokens = line[start_pos:].split()
            node_path = tokens[-2]
            self.node_path = node_path
            self.additional_attrs["options"] = tokens[:-2]
        elif event.startswith("file="):
            # MSG:[06:54:07 13.1.2020] --file=/grapes_reps_v3_2/00/control/pre_data/gmf_get/gmf_get_000 script 10000  :operator
            self.event = "file"
            node_path = event[5:]
            self.node_path = node_path
            start_pos = end_pos + 1
            tokens = line[start_pos:].split()
            user = tokens[-1]
            self.additional_attrs["options"] = tokens[:-1]
        elif event.startswith("load="):
            # MSG:[03:14:32 19.1.2020] --load=gmf_grapes_gfs_post.def  :nwp_pd
            self.event = "load"
            def_path = event[5:]
            self.node_path = def_path
            self.additional_attrs["def_path"] = def_path
        elif event.startswith("begin="):
            # MSG:[20:23:09 28.5.2020] --begin=NWP_OCEAN_v2.0 --force :nwp_qu
            self.event = "begin"
            suite_name = event[6:]
            self.node_path = suite_name
            start_pos = end_pos + 1
            self.additional_attrs["suite_name"] = suite_name
            self.additional_attrs["option"] = line[start_pos:user_start_pos].strip()
        elif event.startswith("replace="):
            # MSG:[02:54:48 13.1.2020] --replace=/gmf_grapes_gfs_post gmf_grapes_gfs_post.def parent  :nwp_pd
            self.event = "replace"
            node_path = event[5:]
            self.node_path = node_path
            start_pos = end_pos + 1
            self.additional_attrs["option"] = line[start_pos:user_start_pos].strip()
        elif event.startswith("order="):
            # MSG:[13:04:50 21.5.2020] --order=/grapes_meso_3km_post/00/tograph/meso_radar down  :nwp_pd
            self.event = "order"
            node_path = event[6:]
            self.node_path = node_path
            start_pos = end_pos + 1
            self.additional_attrs["option"] = line[start_pos:user_start_pos].strip()
        elif event in (
                "restart",
                "suites",
                "stats",
                "edit_history",
                "zombie_get",
                "server_version",
                "ping",
                "check_pt",
                "get",
        ):
            # MSG:[13:26:35 8.1.2020] --restart :nwp_pd

            # MSG:[00:11:32 10.1.2020] --suites :nwp

            # MSG:[05:42:50 9.2.2020] --stats :nwp_pd

            # MSG:[00:40:04 12.2.2020] --edit_history /gda_grapes_gfs_post/12  :nwp_pd
            # MSG:[00:40:08 12.2.2020] --edit_history /  :nwp_pd

            # MSG:[07:48:03 13.2.2020] --zombie_get :nwp_pd

            # MSG:[11:40:17 9.1.2020] --server_version :nwp

            # MSG:[11:40:17 9.1.2020] --ping :nwp

            # MSG:[00:20:04 26.5.2020] --get :csm_exp

            self.event = event
        elif (
                event.startswith("sync_full=")
                or event.startswith("news=")
                or event.startswith("sync=")
                or event.startswith("edit_script=")
                or event.startswith("zombie_fail=")
                or event.startswith("zombie_kill=")
                or event.startswith("zombie_fob=")
                or event.startswith("zombie_adopt=")
                or event.startswith("zombie_remove=")
                or event.startswith("log=")
                or event.startswith("halt=")
                or event.startswith("terminate=")
                or event.startswith("order=")
                or event.startswith("ch_register=")
                or event.startswith("ch_drop=")
                or event.startswith("get_state=")
                or event.startswith("shutdown=")
        ):
            # MSG:[00:34:26 26.5.2020] --get_state=/web_post_v1_0/GRAPES_MESO/FST/FST_getResult_03 :csm_exp

            # MSG:[04:09:39 15.5.2020] --shutdown=yes :nwp_pd

            self.event = event[: event.find("=")]
        else:
            self.event = event
            if debug:
                logger.error(f"client record: event not supported => {self.log_record}")
        self.command = self.event
