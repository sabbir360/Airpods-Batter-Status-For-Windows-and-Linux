from bleak import BleakScanner
from PIL import Image
from asyncio import new_event_loop, set_event_loop, get_event_loop
from pystray import Icon, Menu, MenuItem as Item
from multiprocessing import Process
from time import sleep
from win10toast import ToastNotifier

from PodStatus import PodsStatus

# Configure update duration (update after n seconds)
UPDATE_DURATION = 10
# Configure battery level when you get toast notification of discharging
LOW_LEVEL = 25


# Getting data with hex format
async def get_device():
    print("Scanning...")
    # Scanning for devices
    try:
        devices = await BleakScanner.discover(return_adv=True)
    except OSError:
        print("Device not available.")
        return False

    print("Device list found....")

    for _, device_data in devices.items():

        d = device_data[1].manufacturer_data
        print(d)
        hex_byte = d.get(76, b"")  # airpods mainly returns value under key 76
        hex_str = hex_byte.hex()

        if len(hex_str) == 54:  # 54 string len is apple
            print(f"Found {hex_str}")
            return hex_str
        else:
            print(f"No AirPods {hex_str}")


# Same as get_device() but it's standalone method instead of async
def get_data_hex():
    new_loop = new_event_loop()
    set_event_loop(new_loop)
    loop = get_event_loop()
    a = loop.run_until_complete(get_device())
    return a


# Getting data from hex string and converting it to dict(json)
def get_data()->dict:
    # for real
    raw = get_data_hex() or ""
    # for demo
    # raw = "07190114200baa8f0000044b82e277d9e683f1a2ee44503cfef38a"
    print(raw)
    # Return blank data if airpods not found
    if not raw:
        return dict(status=0, model="AirPods not found")

    pod_status = PodsStatus(raw)
    pod = pod_status.pods

    model = pod.get_model()
    left_pod = pod.get_pod(pod.LEFT)
    left = left_pod.int_status()

    right_pod = pod.get_pod(pod.RIGHT)
    right = right_pod.int_status()

    case_pod = pod.get_pod(pod.CASE)
    case = case_pod.int_status()

    # Return result info in dict format
    return dict(
        status=1,
        charge=dict(
            left=left,
            right=right,
            case=case
        ),
        charging=dict(
            left="Left Pod " if left_pod.is_charging() else "Left Pod not ",
            right="Right Pod " if right_pod.is_charging() else "Right Pod not ",
            case="Case " if case_pod.is_charging() else "Case not "
        ),
        model=model
    )


# Checking AirPods availability and create icon in tray
def create_icon(status, left, right, case, model, charge):
    # Rewriting data dict because cant pass all dict with multiprocessing lib
    data = dict(
        status=status,
        charge=dict(
            left=left,
            right=right,
            case=case
        ),
        model=model,
    )
    # Blank values
    a_left = True
    a_right = True
    a_case = True
    charges = dict(
        left=-1,
        right=-1,
        case=-1
    )

    if data["status"] == 0:
        # Setting false availability for all devices and setting icon path
        a_left = False
        a_right = False
        a_case = False
        image = "./icons/no.png"
    else:
        # Checking for availability and errors for connected devices
        charges = data["charge"]
        if charges["left"] == -1:
            a_left = False
        if charges["right"] == -1:
            a_right = False
        if charges["case"] == -1:
            a_case = False
    if charge == "":
        charge = "No Charge Info!"
    # Right click menu
    menu = Menu(
        Item(
            text=data["model"],
            action="",
            enabled=False
        ),
        Item(
            text="Left: {}%".format(charges["left"]),
            action="",
            enabled=True,
            visible=a_left
        ),
        Item(
            text="Right: {}%".format(charges["right"]),
            action="",
            enabled=True,
            visible=a_right
        ),
        Item(
            text="Case: {}%".format(charges["case"]),
            action="",
            enabled=True,
            visible=a_case
        ),
        Item(
            text=charge,
            action="",
            enabled=False,
            visible=False
        )
    )

    # Selecting lowest charge level for comparing and icon select
    if a_left and charges["left"] > charges["right"]:
        lowest = charges["left"]
    elif a_right and charges["right"] > charges["left"]:
        lowest = charges["right"]
    elif charges["right"] == charges["left"]:
        lowest = charges["right"]
    else:
        lowest = -1

    # Selecting icon for charge levels
    if lowest == -1:
        image = "./icons/no.png"
    elif lowest < 20:
        image = "./icons/empty.png"
    elif lowest < 40:
        image = "./icons/low.png"
    elif lowest < 60:
        image = "./icons/middle.png"
    elif lowest < 80:
        image = "./icons/much.png"
    elif lowest < 100:
        image = "./icons/full.png"
    else:
        image = "./icons/no.png"

    # Creating icon
    Icon(data["model"], Image.open(image), menu=menu).run()


# Simple method for notification show
def low_level_notification(model, percent):
    notifer = ToastNotifier()
    notifer.show_toast(model, "Your battery is going low ({}%)".format(percent), "./icons/low_n.ico", 5, True)


def run():

    connected = True
    cache = None
    cached_process = None
    while True:
        data = get_data()
        if data["status"] == 1:
            # Checking cache and current data for avoid Windows duplicate tray icon bug
            if cache != data["charge"] or not connected:
                # Flushing process(tray icon) and handling error that might be on start
                try:
                    cached_process.terminate()
                except AttributeError:
                    pass

                # Starting new thread(process)
                charge = ""
                for _, v in data["charging"].items():
                    charge += f"{v}charging, "

                if charge != "":
                    charge = charge[:-1]
                proc = Process(target=create_icon, args=(1,
                                                         data["charge"]["left"], # left
                                                         data["charge"]["right"], # right
                                                         data["charge"]["case"], # case
                                                         data["model"], charge))
                proc.start()

                # Setting cache vars
                cached_process = proc
                cache = data["charge"]

                # Checking for low level for notify show
                if int(data["charge"]["left"]) <= LOW_LEVEL or int(data["charge"]["right"]) <= LOW_LEVEL:
                    low_level_notification(data["model"], data["charge"]["right"])

        elif data["status"] == 0:
            # Checking cache and current data for avoid Windows duplicate tray icon bug
            if connected:
                # Flushing process(tray icon) and handling error that might be on start
                try:
                    cached_process.terminate()
                except AttributeError:
                    pass
                # Creating process and setting cache var
                proc = Process(
                    target=create_icon, args=(0, -1, -1, -1, data["model"], ""), )
                connected = False
                proc.start()

        sleep(UPDATE_DURATION)


if __name__ == '__main__':
    run()


