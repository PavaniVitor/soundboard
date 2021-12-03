from flask import Flask
from flask import render_template
from vlc_wrapper import play
import os

app = Flask(__name__)

audios = {} 
config = "config.txt"
player_instances = []
vol_self = 50
vol_other = 100


def load():
    with open(config) as f:

        print("reading config.txt: ")
        for line in f.readlines():
            line = line.strip()
            if line:
                name, uri = line.split("=")
                audios[name] = uri.strip()
            print(f"{name=} {uri=}")
        print()

    print("reading files from /sounds:")
    for sound_file in os.listdir('sounds'):
        audios[sound_file] = os.path.join(os.getcwd(), 'sounds', sound_file)
        print(f'{sound_file}')
    print()

@app.route("/")
def home():
    load()
    return render_template("index.html", audios=audios)

@app.route("/<audio_name>")
def play_audio(audio_name):
    print(f"playing: {audio_name}")
    global player_instances, vol_self, vol_other
    player_instances.append(play(audios[audio_name], volume=vol_other))
    player_instances.append(play(audios[audio_name], volume=vol_self, vb_cable=False))
    return "boa!"

@app.route("/stop")
def stop_audio():
    global player_instances
    print(player_instances)
    for player in player_instances:
        player.stop()
    player_instances = []
    print("parando")
    return "paro"

@app.route("/volume_self/<amount>")
def volume_self(amount):
    global vol_self
    vol_self = int(amount)
    print(f"volume_self set to {amount}")
    return "volume!"

@app.route("/volume_other/<amount>")
def volume_other(amount):
    global vol_other
    vol_other = int(amount)
    print(f"volume_other set to {amount}")
    return "volume!"
    

app.run(host='0.0.0.0')

