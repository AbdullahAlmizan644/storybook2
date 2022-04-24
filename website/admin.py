from flask import Blueprint, redirect, render_template,request,flash,session
from website.__init__ import db,create_app


admin=Blueprint('admin',__name__)
app=create_app()


@admin.route("/admin_login",methods=["GET","POST"])
def admin_login():
    if request.method=="POST":
        email=request.form.get("email")
        password=request.form.get("password")

        if email=="admin@gmail.com" and password=="12345678":
            session["admin"]=email
            return redirect("/dashboard")
        else:
            flash("wrong email or password.", category="error")
    return render_template("admin/login.html")


@admin.route("/admin_logout")
def admin_logout():
    session.pop("admin",None)
    return redirect("/")


@admin.route("/dashboard")
def dashboard():
    if "admin" in session:

        cur=db.connection.cursor()
        cur.execute("SELECT count(sno) from users ")
        total_user=cur.fetchone()
        return render_template("admin/index.html",total_user=total_user)
    else:
        return redirect("/admin_login")


@admin.route("/all_order")
def all_order():
    if "admin" in session:
        return render_template("admin/orders.html")
    else:
        return redirect("/admin_login")


@admin.route("/all_user")
def all_user():
    if "admin" in session:
        cur=db.connection.cursor()
        cur.execute("SELECT * FROM users")
        users=cur.fetchall()

        cur=db.connection.cursor()
        cur.execute("SELECT count(sno) from users ")
        total_user=cur.fetchone()
        return render_template("admin/user.html",users=users,total_user=total_user)
    else:
        return redirect("/admin_login")

@admin.route("/delete_user/<int:id>")
def delete_user(id):
    if "admin" in session:
        cur=db.connection.cursor()
        cur.execute("DELETE FROM users WHERE sno=%s",(id,))
        db.connection.commit()
        return redirect("/all_user")
    
    else:
        return redirect("/admin_login")