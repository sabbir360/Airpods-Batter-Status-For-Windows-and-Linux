class Pod:
    DISCONNECTED_STATUS = 15
    MAX_CONNECTED_STATUS = 10
    LOW_BATTERY_STATUS = 1

    def __init__(self, status, charging, in_ear):
        self.status = status
        self.charging = charging
        self.in_ear = in_ear

    def get_status(self):
        return self.status

    def parse_status(self):
        return str(self.int_status())+"%"

    def int_status(self):
        if self.status == self.MAX_CONNECTED_STATUS:
            return 100
        elif self.status < self.MAX_CONNECTED_STATUS:
            return self.status * 10 + 5
        else:
            return -1

    def is_charging(self):
        return self.charging

    def is_in_ear(self):
        return self.in_ear

    def is_connected(self):
        return self.status <= self.MAX_CONNECTED_STATUS

    def is_disconnected(self):
        return self.status == self.DISCONNECTED_STATUS

    def is_low_battery(self):
        return self.status <= self.LOW_BATTERY_STATUS

    def in_ear_visibility(self):
        return True if self.in_ear else False

    def bat_img_visibility(self):
        return True if (self.charging and self.is_connected()) or self.is_low_battery() else False

    def bat_img_src_id(self):
        return True if self.charging else False
