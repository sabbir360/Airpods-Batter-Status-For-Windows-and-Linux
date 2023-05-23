from RegularPods import RegularPods


class AirPodsPro2(RegularPods):
    def __init__(self, left_pod, right_pod, case_pod):
        super().__init__(left_pod, right_pod, case_pod)

    def get_left_drawable(self):
        return True if self.get_pod(self.LEFT).is_connected() else False

    def get_right_drawable(self):
        return True if self.get_pod(self.RIGHT).is_connected() else False

    def get_case_drawable(self):
        return True if self.get_pod(self.CASE).is_connected() else False

    def get_model(self):
        return "Airpods Pro 2"


class AirPods1(AirPodsPro2):
    def get_model(self):
        return "Airpods"


class AirPods2(AirPodsPro2):
    def get_model(self):
        return "AirPods 2"


class AirPods3(AirPodsPro2):
    def get_model(self):
        return "AirPods 3"


class AirPodsPro(AirPodsPro2):
    def get_model(self):
        return "AirPods Pro"
