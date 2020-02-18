from .record import EcflowLogRecord, LogType, EventType


class ClientLogRecord(EcflowLogRecord):
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
        self.event_type = EventType.Client
        self.command = None

    def parse_record(self, line: str):
        """
        Parse client record

        Example
            MSG:[06:35:57 12.1.2020] --force=complete /grapes_geps_v1_2/00/members/pair_05/mem02/model/forecast  :nwp
            MSG:[13:30:29 8.1.2020] --news=0 1 0  :nwp [:NO_NEWS]
            MSG:[13:30:35 8.1.2020] --server_version :nwp
            MSG:[13:30:35 8.1.2020] --sync_full=0 :nwp

        Parameters
        ----------
        line: str

        Returns
        -------

        """
        start_pos = 0
        end_pos = line.find(" ", start_pos)
        if end_pos == -1:
            # print("[ERROR] client record: event not found =>", self.log_record)
            return
        event = line[start_pos:end_pos]

        if event == "requeue":
            # MSG:[07:50:49 31.1.2020] --requeue force /grapes_reps_v3_2/00/control/model/fcst_monitor  :nwp_qu
            self.event = event
            start_pos = end_pos + 1
            tokens = line[start_pos:].split()
            if len(tokens) == 3:
                requeue_option = tokens[0]
                node_path = tokens[1]
                user = tokens[2]
                self.node_path = node_path
                self.additional_attrs["requeue_option"] = requeue_option
                self.additional_attrs["user"] = user
            else:
                # print("[ERROR] client record: requeue parse error =>", self.log_record)
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
            user = tokens[-1]
            node_path = tokens[-2]
            self.node_path = node_path
            self.additional_attrs["options"] = " ".join(tokens[:-2])
            self.additional_attrs["user"] = user
        elif event.startswith("force="):
            # MSG:[05:55:30 9.2.2020] --force=complete recursive /grapes_meso_3km_post/12  :nwp_pd
            # LOG:[05:55:30 9.2.2020]  complete: /grapes_meso_3km_post/12
            # LOG:[05:55:30 9.2.2020]  complete: /grapes_meso_3km_post/12/initial
            self.event = "force"
            start_pos = end_pos + 1
            tokens = line[start_pos:].split()
            node_path = tokens[-2]
            user = tokens[-1]
            self.node_path = node_path
            self.additional_attrs["options"] = " ".join(tokens[:-2])
            self.additional_attrs["user"] = user
        elif event.startswith("file="):
            # MSG:[06:54:07 13.1.2020] --file=/grapes_reps_v3_2/00/control/pre_data/gmf_get/gmf_get_000 script 10000  :operator
            self.event = "file"
            node_path = event[5:]
            self.node_path = node_path
            start_pos = end_pos + 1
            tokens = line[start_pos:].split()
            user = tokens[-1]
            self.additional_attrs["options"] = " ".join(tokens[:-1])
            self.additional_attrs["user"] = user
        elif event.startswith("load="):
            # MSG:[03:14:32 19.1.2020] --load=gmf_grapes_gfs_post.def  :nwp_pd
            self.event = "load"
            node_path = event[5:]
            self.node_path = node_path
            start_pos = end_pos + 1
            self.additional_attrs = line[start_pos:]
        elif event.startswith("begin="):
            self.event = "begin"
            node_path = event[6:]
            self.node_path = node_path
            start_pos = end_pos + 1
            self.additional_attrs = line[start_pos:]
        elif event.startswith("replace="):
            # MSG:[02:54:48 13.1.2020] --replace=/gmf_grapes_gfs_post gmf_grapes_gfs_post.def parent  :nwp_pd
            self.event = "replace"
            node_path = event[5:]
            self.node_path = node_path
            start_pos = end_pos + 1
            self.additional_attrs = line[start_pos:]
        elif event.startswith("order="):
            self.event = "order"
            node_path = event[6:]
            self.node_path = node_path
            start_pos = end_pos + 1
            self.additional_attrs = line[start_pos:]
        elif event in (
                "restart",
                "suites",
                "stats",
                "edit_history",
                "zombie_get",
                "server_version",
                "ping",
                "check_pt",
        ):
            # MSG:[13:26:35 8.1.2020] --restart :nwp_pd

            # MSG:[00:11:32 10.1.2020] --suites :nwp

            # MSG:[05:42:50 9.2.2020] --stats :nwp_pd

            # MSG:[00:40:04 12.2.2020] --edit_history /gda_grapes_gfs_post/12  :nwp_pd
            # MSG:[00:40:08 12.2.2020] --edit_history /  :nwp_pd

            # MSG:[07:48:03 13.2.2020] --zombie_get :nwp_pd

            # MSG:[11:40:17 9.1.2020] --server_version :nwp

            # MSG:[11:40:17 9.1.2020] --ping :nwp

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
        ):
            self.event = event[: event.find("=")]
        else:
            self.event = event
            # print("[ERROR] client record: event not supported =>", self.log_record)
        self.command = self.event
