from flask import Blueprint, render_template,redirect,session,flash,request
from website.__init__ import db
from datetime import datetime,timedelta
view=Blueprint('view',__name__)


@view.route("/")
def index():
    cur=db.connection.cursor()
    cur.execute("SELECT count(sno) from users ")
    total_users=cur.fetchone()


    cur=db.connection.cursor()
    cur.execute("SELECT count(id) from audiobooks ")
    total_audiobooks=cur.fetchone()


    cur=db.connection.cursor()
    cur.execute("SELECT count(id) from podcast ")
    total_podcasts=cur.fetchone()

    cur=db.connection.cursor()  
    cur.execute("SELECT count(book_id) from books ")
    total_books=cur.fetchone()

    return render_template("view/index.html",total_users=total_users,total_books=total_books,total_audiobooks=total_audiobooks,total_podcasts=total_podcasts)


@view.route("/pricing")
def pricing():
    if "user" in session:
        return render_template("view/pricing.html")
    else:
        return redirect("/login")


@view.route("/buy_package/<int:day>/<string:name>",methods=["GET","POST"])
def buy_package(day,name):
    if "user" in session:
        a=day
        b=name
        buying_date=datetime.now()
        validity=buying_date+timedelta(day)
        
        if request.method=="POST":
            payment=request.form.get("payment")

            

            cur=db.connection.cursor()
            cur.execute("INSERT INTO suscriber(username,buying_date,validity,payment_method) VALUES (%s,%s,%s,%s)",(session["user"],buying_date,validity,payment,))
            db.connection.commit()

            status="premium"

            cur=db.connection.cursor()
            cur.execute("UPDATE users set status=%s where username=%s",(status,session["user"],))
            db.connection.commit()

            flash("Buying complete",category="success")
            return redirect("/confirm_package")
        return render_template("view/buy_package.html",a=a,b=b,buying_date=buying_date,validity=validity)

    else:
        return redirect("/login")


@view.route("/confirm_package")
def confirm_package():
    if "user" in session:
        cur=db.connection.cursor()
        cur.execute("SELECT * FROM suscriber where username=%s",(session["user"],))
        data=cur.fetchall()
        print(data)
        user=len(data)-1

        for i in range(user,-1,-1):
            s_data=data[i]
            if s_data is not None:
                break

        print(s_data) 
        return render_template("view/confirm_package.html",s_data=s_data)
    
    else:
        return redirect("/login")



@view.route("/about")
def about():
    return render_template("view/about.html")



@view.route("/contact")
def contact():
    return render_template("view/contact.html")



@view.route("/service")
def service():
    return render_template("view/service.html")


@view.route("/author")
def author():
    return render_template("view/author.html")


@view.route("/author_deatils")
def author_deatils():
    return render_template("view/author_deatils.html")

@view.route("/chapter")
def chapter():
    return render_template("view/chapter.html")