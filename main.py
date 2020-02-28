import configparser
from player import Player
from pathlib import Path
from pynput.keyboard import Key
from pynput.keyboard import Listener
from threading import Thread

DEBUG = False

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

player = Player()

if not config["DEFAULT"]["cable index"]:
    vb_ind = get_vb_index(player.pyaudio_instance)
else:
    vb_ind = config.getint("DEFAULT", "cable index")

sound_folder = Path(config["DEFAULT"]["sound folder"])
f = sound_folder / "chirp.wav"


def play(f):
    player.play(str(f))
    player.play(str(f),device=vb_ind)


def on_press(key):
    if DEBUG:
        print('{0} pressed'.format(key))
    
    try:
        k = keys['{0}'.format(key)]
    except:
        k = '{0}'.format(key)
    
    if DEBUG:
        print(k)

    # acha o audio pra tocar

    if key == Key.f1: # menos feio porem correto
        Thread(target=play, args=(f, )).start()
        
def on_release(key):
    if DEBUG:
        print('{0} release'.format(key))

    if key == Key.f10:
        # Stop listener
        return False


with Listener(
    on_press=on_press,
    on_release=on_release) as listener:
        listener.join()
