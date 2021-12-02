from flask import Flask
from flask import render_template
from vlc_wrapper import play
import os

app = Flask(__name__)

audios = {} 
config = "config.txt"
player_instances = []

with open(config) as f:
    lines = f.readlines()
    for line in lines:
        name, uri = line.split("=")
        audios[name]=uri.strip()
        print(f"{name=}{uri=}")

for sound_file in os.listdir('sounds'):
    audios[sound_file] = os.path.join(os.getcwd(), 'sounds', sound_file)
    print(f'added file from soundfile folder: {sound_file}')


@app.route("/")
def home():
    return render_template("index.html", audios=audios)

@app.route("/<audio_name>")
def play_audio(audio_name):
    print(f"playing: {audio_name}")
    global player_instances
    player_instances.append(play(audios[audio_name], vol=100))
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

app.run()

