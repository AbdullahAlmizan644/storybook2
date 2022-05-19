from flask import Blueprint, render_template
from website.__init__ import db

podcast=Blueprint('podcast',__name__)

@podcast.route("/podcast")
def listen_podcast():
    cur=db.connection.cursor()
    cur.execute("SELECT * FROM podcast")
    podcasts=cur.fetchall()

    cur=db.connection.cursor()
    cur.execute("SELECT podcaster FROM podcast ")
    podcaster=cur.fetchall()
    print(podcaster)
    return render_template("podcast/index.html",podcasts=podcasts)


@podcast.route("/single_podcast/<int:sno>")
def single_podcast(sno):
    cur=db.connection.cursor()
    cur.execute("SELECT * FROM podcast")
    podcasts=cur.fetchall()

    cur=db.connection.cursor()
    cur.execute("SELECT * FROM podcast where id=%s",(sno,))
    podcast=cur.fetchone()
    return render_template("podcast/single-post.html",podcast=podcast,podcasts=podcasts)


@podcast.route("/podcaster/<string:name>")
def podcaster(name):
    cur=db.connection.cursor()
    cur.execute("SELECT * FROM podcast where podcaster=%s",(name,))
    podcasts=cur.fetchall()
    return render_template("podcast/podcaster.html",podcasts=podcasts)