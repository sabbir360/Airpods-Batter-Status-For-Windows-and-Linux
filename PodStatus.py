import time
from Pod import Pod
from RegularPods import RegularPods
from Airpods import AirPodsPro2, AirPods1, AirPods2, AirPods3, AirPodsPro


class PodsStatus:
    DISCONNECTED = None

    def __init__(self, status=None):
        self.pods = None
        self.timestamp = int(time.time() * 1000)

        if status is None:
            return

        flip = self.is_flipped(status)

        left_status = int(status[12 if flip else 13], 16)
        right_status = int(status[13 if flip else 12], 16)
        case_status = int(status[15], 16)
        # single_status = int(status[13], 16)

        charge_status = int(status[14], 16)

        charge_l = (charge_status & (0b00000010 if flip else 0b00000001)) != 0
        charge_r = (charge_status & (0b00000001 if flip else 0b00000010)) != 0
        charge_case = (charge_status & 0b00000100) != 0
        # charge_single = (charge_status & 0b00000001) != 0

        in_ear_status = int(status[11], 16)

        in_ear_l = (in_ear_status & (0b00001000 if flip else 0b00000010)) != 0
        in_ear_r = (in_ear_status & (0b00000010 if flip else 0b00001000)) != 0

        left_pod = Pod(left_status, charge_l, in_ear_l)
        right_pod = Pod(right_status, charge_r, in_ear_r)
        case_pod = Pod(case_status, charge_case, False)
        # single_pod = Pod(single_status, charge_single, False)
        #
        # id_single = status[7]
        id_full = status[6:10]

        if id_full == "0220":
            self.pods = AirPods1(left_pod, right_pod, case_pod)
        elif id_full == "0F20":
            self.pods = AirPods2(left_pod, right_pod, case_pod)
        elif id_full == "1320":
            self.pods = AirPods3(left_pod, right_pod, case_pod)
        elif id_full == "0E20":
            self.pods = AirPodsPro(left_pod, right_pod, case_pod)
        elif id_full == "1420":
            self.pods = AirPodsPro2(left_pod, right_pod, case_pod)
        # elif id_single == 'A':
        #     self.pods = AirPodsMax(single_pod)
        # elif id_single == 'B':
        #     self.pods = PowerbeatsPro(left_pod, right_pod, case_pod)
        # elif id_full == "0520":
        #     self.pods = BeatsX(single_pod)
        # elif id_full == "1020":
        #     self.pods = BeatsFlex(single_pod)
        # elif id_full == "0620":
        #     self.pods = BeatsSolo3(single_pod)
        # elif id_single == '9':
        #     self.pods = BeatsStudio3(single_pod)
        # elif id_full == "0320":
        #     self.pods = Powerbeats3(single_pod)
        else:
            self.pods = RegularPods(left_pod, right_pod, case_pod)
        # print(self.get_airpods())

    @staticmethod
    def is_flipped(string):
        return (int(string[10], 16) & 0x02) == 0

    def get_airpods(self):
        return self.pods

    def is_all_disconnected(self):
        if self is self.DISCONNECTED:
            return True

        return self.pods.is_disconnected()

    def get_timestamp(self):
        return self
