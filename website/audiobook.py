from flask import Blueprint, render_template
from website.__init__ import db

audiobook=Blueprint('audiobook',__name__)



@audiobook.route("/audiobook")
def audiobooks():
    cur=db.connection.cursor()
    cur.execute("SELECT * FROM audiobooks")
    audiobooks=cur.fetchall()
    return render_template("podcast/audiobook.html",audiobooks=audiobooks)




@audiobook.route("/single_audiobook/<int:sno>")
def single_audiobook(sno):
    cur=db.connection.cursor()
    cur.execute("SELECT * FROM audiobooks where id=%s",(sno,))
    audiobook=cur.fetchone()
    return render_template("podcast/single-music.html",audiobook=audiobook)


