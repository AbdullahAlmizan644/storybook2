from flask import Blueprint, render_template

podcast=Blueprint('podcast',__name__)

@podcast.route("/podcast")
def listen_podcast():
    return render_template("podcast/index.html")


