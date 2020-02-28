import configparser
import sys
from player import Player
from pathlib import Path
from pynput.keyboard import Key
from pynput.keyboard import Listener
from threading import Thread

DEBUG = True

keys = {
    "Key.f1" : "f1",
    "Key.f2" : "f2",
    "Key.f3" : "f3",
    "Key.f4" : "f4",
    "Key.f5" : "f5",
    "Key.f6" : "f6",
    "Key.f7" : "f7",
    "Key.f8" : "f8",
    "Key.f9" : "f9",
    "Key.f10" : "f10",
    "Key.f11" : "f11",
    "Key.f12" : "f12",
    "Key.shift" : "shift",
    "Key.shift_r" : "shift_r",
    "Key.ctrl_r" : "ctrl_r",
    "Key.ctrl_l" : "ctrl_r",
    "Key.enter" : "enter",
    "<96>" : "num0",
    "<97>" : "num1",
    "<98>" : "num2",
    "<99>" : "num3",
    "<100>" : "num4",
    "<101>" : "num5",
    "<102>" : "num6",
    "<103>" : "num7",
    "<104>" : "num8",
    "<105>" : "num9"
}

def get_vb_index(pyaudio_player):
    """
    auto detect VB-Cable device index
    """
    for i in range(pyaudio_player.get_device_count()):
        device = pyaudio_player.get_device_info_by_index(i)

        if device["name"] == 'CABLE Input (VB-Audio Virtual C':
            return device["index"]
    else:
        return None

config = configparser.ConfigParser()
config.read("config.cfg")

sound_folder = Path(config["DEFAULT"]["sound folder"])

if not config["DEFAULT"]["cable index"]:
    vb_index = get_vb_index(Player.pyaudio_instance)
else:
    vb_index = config.getint("DEFAULT", "cable index")


def on_press(key):
    key = str(key)
    k = keys.get(key, key)
    k = k.replace("'", "")

    if DEBUG:
        print('{} ({}) pressed'.format(key, k))

    if k == "f10":
        return False

    try:
        file_path = sound_folder / config["BINDS"][k]
    except KeyError:
        sys.stderr.write("bind {} not found".format(k))
        return True

    if file_path:
        Thread(target=play, args=(file_path, )).start()             # play for me
        Thread(target=play, args=(file_path, vb_index)).start()       # play in vb output
    elif DEBUG:
        print("file_path {} not found".format(file_path))


def play(file_path, device=None):
    Player.play(str(file_path), device)

def main():
    with Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == '__main__': main()
