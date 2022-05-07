from flask import Blueprint, render_template,request,flash
from website.__init__ import db

audiobook=Blueprint('audiobook',__name__)



@audiobook.route("/audiobook")
def audiobooks():
    cur=db.connection.cursor()
    cur.execute("SELECT * FROM audiobooks")
    audiobooks=cur.fetchall()
    return render_template("audiobook/index.html",audiobooks=audiobooks)




@audiobook.route("/single_audiobook/<int:sno>")
def single_audiobook(sno):
    cur=db.connection.cursor()
    cur.execute("SELECT * FROM audiobooks")
    audiobooks=cur.fetchall()


    cur=db.connection.cursor()
    cur.execute("SELECT * FROM audiobooks where id=%s",(sno,))
    audiobook=cur.fetchone()
    return render_template("audiobook/single-post.html",audiobook=audiobook,audiobooks=audiobooks)


@audiobook.route("/search_audiobook",methods=["GET","POST"])
def search_audiobook():
    if request.method=="POST":
        search_audio=request.form.get("search_audio")

        cur=db.connection.cursor()
        cur.execute(f"SELECT * FROM audiobooks where name LIKE '%{search_audio}%' ")
        audiobooks=cur.fetchall()

        return render_template("audiobook/search_audiobook.html",audiobooks=audiobooks,search_audio=search_audio)



@audiobook.route("/audiobook_category/<string:cat>")
def audiobook_category(cat):
    cur=db.connection.cursor()
    cur.execute("SELECT * FROM audiobooks where category=%s",(cat,))
    audiobooks=cur.fetchall()

    return render_template("audiobook/audiobook_category.html",audiobooks=audiobooks)
