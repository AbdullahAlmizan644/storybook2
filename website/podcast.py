from flask import Blueprint, render_template,redirect,session
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
    if "user" in session:
        cur=db.connection.cursor()
        cur.execute("SELECT * FROM users where username=%s",(session["user"],))
        user=cur.fetchone()
            
        cur=db.connection.cursor()
        cur.execute("SELECT * FROM podcast where id=%s",(sno,))
        podcast=cur.fetchone()

        cur=db.connection.cursor()
        cur.execute("SELECT * FROM podcast")
        podcasts=cur.fetchall()

        if "free" in podcast[7]:
            return render_template("podcast/single-post.html",podcast=podcast,podcasts=podcasts)

        elif "premium" in user[8] and "premium" in podcast[7]:
            return render_template("podcast/single-post.html",podcast=podcast,podcasts=podcasts)
            
        else:
            return redirect("/pricing")

    else:
        return redirect("/login")

@podcast.route("/podcaster/<string:name>")
def podcaster(name):
    cur=db.connection.cursor()
    cur.execute("SELECT * FROM podcast where podcaster=%s",(name,))
    podcasts=cur.fetchall()
    return render_template("podcast/podcaster.html",podcasts=podcasts)