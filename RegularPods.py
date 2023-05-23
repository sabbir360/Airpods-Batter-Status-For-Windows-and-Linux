from abc import ABC, abstractmethod


class IPods(ABC):
    @abstractmethod
    def get_model(self):
        pass

    @abstractmethod
    def is_single(self):
        pass

    @abstractmethod
    def is_disconnected(self):
        pass

    @abstractmethod
    def parse_status_for_logger(self):
        pass


class RegularPods(IPods):
    LEFT = 0
    RIGHT = 1
    CASE = 2

    def __init__(self, left_pod, right_pod, case_pod):
        self.pods = [left_pod, right_pod, case_pod]

    def get_pod(self, pos):
        return self.pods[pos]

    def get_parsed_status(self, pos):
        return self.pods[pos].parse_status()

    def get_in_ear_visibility(self, pos):
        return self.pods[pos].in_ear_visibility()

    def get_bat_img_visibility(self, pos):
        return self.pods[pos].bat_img_visibility()

    def get_bat_img_src_id(self, pos):
        return self.pods[pos].bat_img_src_id()

    def get_left_drawable(self):
        return True if self.get_pod(self.LEFT).is_connected() else False

    def get_right_drawable(self):
        return True if self.get_pod(self.RIGHT).is_connected() else False

    def get_case_drawable(self):
        return True if self.get_pod(self.CASE).is_connected() else False

    def get_model(self):
        return "Unknown"

    def is_single(self):
        return False

    def is_disconnected(self):
        return self.get_pod(self.LEFT).is_disconnected() and \
               self.get_pod(self.RIGHT).is_disconnected() and \
               self.get_pod(self.CASE).is_disconnected()

    def parse_status_for_logger(self):
        left_pod = self.get_pod(self.LEFT)
        right_pod = self.get_pod(self.RIGHT)
        case_pod = self.get_pod(self.CASE)
        return f"Left: {left_pod.get_status()}{'+ ' if left_pod.is_charging() else ''}{'$ ' if left_pod.is_in_ear() else ''}" \
               f"Right: {right_pod.get_status()}{'+ ' if right_pod.is_charging() else ''}{'$ ' if right_pod.is_in_ear() else ''}" \
               f"Case: {case_pod.get_status()}{'+ ' if case_pod.is_charging() else ''} Model: {self.get_model()}"
