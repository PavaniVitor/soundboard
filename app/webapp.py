from flask import Flask
from flask import render_template
from vlc_wrapper import play

app = Flask(__name__)

audios = {} 
config = "config.txt"

with open(config) as f:
    lines = f.readlines()
    for line in lines:
        name, uri = line.split("=")
        audios[name]=uri.strip()
        print(f"{name=}{uri=}")


@app.route("/")
def home():
    return render_template("index.html", audios=audios)

@app.route("/<audio_name>")
def play_audio(audio_name):
    print(f"playing: {audio_name}")
    play(audios[audio_name])


    return "boa!"

app.run()

