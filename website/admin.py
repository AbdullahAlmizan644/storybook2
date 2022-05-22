from flask import Blueprint, redirect, render_template,request,flash,session
from website.__init__ import db,create_app
import os
from werkzeug.utils import secure_filename
from datetime import datetime



admin=Blueprint('admin',__name__)
app=create_app()




"""Admin"""
@admin.route("/admin_login",methods=["GET","POST"])
def admin_login():
    if request.method=="POST":
        email=request.form.get("email")
        password=request.form.get("password")

        if email=="abdullahalmizan644@gmail.com" and password=="12345678":
            session["admin"]=email
            flash("Login Successfully!", category="success")
            return redirect("/dashboard")
        else:
            flash("wrong email or password.", category="error")
    return render_template("admin/login.html")


@admin.route("/admin_logout")
def admin_logout():
    session.pop("admin",None)
    return redirect("/admin_login")


@admin.route("/admin_profile")
def admin_profile():
    if "admin" in session:
        return render_template("admin/profile.html")
    else:
        return redirect("/admin_login")



@admin.route("/dashboard")
def dashboard():
    if "admin" in session:
        cur=db.connection.cursor()
        cur.execute("SELECT count(sno) from users ")
        total_user=cur.fetchone()


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

        cur=db.connection.cursor()
        cur.execute("SELECT * FROM suscriber")
        subscribers=cur.fetchall()

        return render_template("admin/index.html",total_users=total_users,total_audiobooks=total_audiobooks,total_podcasts=total_podcasts,total_books=total_books,subscribers=subscribers)
    else:
        return redirect("/admin_login")





"""Orders"""
@admin.route("/all_order")
def all_order():
    if "admin" in session:
        return render_template("admin/orders.html")
    else:
        return redirect("/admin_login")





"""users"""
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
        flash("you remove a user",category="error")
        return redirect("/all_user")
    
    else:
        return redirect("/admin_login")





"""AudioBook"""

@admin.route("/all_audiobook")
def all_audiobook():
    if "admin" in session:
        cur=db.connection.cursor()
        cur.execute("SELECT * FROM audiobooks")
        books=cur.fetchall()

        cur=db.connection.cursor()  
        cur.execute("SELECT count(id) from audiobooks ")
        total_book=cur.fetchone()
        return render_template("admin/audiobook.html",books=books,total_book=total_book)
    else:
        return redirect("/admin_login")


@admin.route("/delete_audiobook/<int:id>")
def delete_audiobok (id):
    if "admin" in session:
        cur=db.connection.cursor()
        cur.execute("DELETE FROM audiobooks WHERE id=%s",(id,))
        db.connection.commit()
        flash("Audiobook delete",category="error")
        return redirect("/all_audiobook")
    
    else:
        return redirect("/admin_login")




@admin.route("/add_audiobook",methods=["GET","POST"])
def add_audiobok ():
    if "admin" in session:
        if request.method=="POST":
            name=request.form.get("name")
            description=request.form.get("description")
            writer=request.form.get("writer")
            category=request.form.get("category")
            Type=request.form.get("type")

            image = request.files['image']
            audio = request.files['audio']
            if image.filename == '' and audio.filename == "":
                flash('No selected file', category="error")
                return redirect(request.url)
            else:
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(image.filename)))
                audio.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(audio.filename)))
                cur=db.connection.cursor()
                cur.execute("INSERT INTO audiobooks(name,description,writer,image,audio,date,category,Type) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",(name,description,writer,image.filename,audio.filename,datetime.now(),category,Type,))
                db.connection.commit()
                flash("Audiobook added successfully!",category="success")
                return redirect("/all_audiobook")
        
        return render_template("admin/add_audiobook.html")
    
    else:
        return redirect("/admin_login")



@admin.route("/edit_audiobook/<int:id>",methods=["POST","GET"])
def edit_audiobook(id):
    if "admin" in session:
        cur=db.connection.cursor()
        cur.execute("SELECT * FROM audiobooks WHERE id=%s",(id,))
        audiobook=cur.fetchone()
        if request.method=="POST":
            name=request.form.get("name")
            description=request.form.get("description")
            writer=request.form.get("writer")
            category=request.form.get("category")

            image = request.files['image']
            audio = request.files['audio']
            if image.filename == '' and audio.filename == "":
                flash('No selected file', category="error")
                return redirect(request.url)
            else:
                cur=db.connection.cursor()
                cur.execute("update audiobooks set name=%s,description=%s,writer=%s,category=%s,image=%s,audio=%s where id=%s",(name,description,writer,category,image.filename,audio.filename,id,))
                db.connection.commit()
            flash("Audiobook edited successfully!",category="success")
            return redirect("/all_audiobook")
        return render_template("admin/edit_audiobook.html",audiobook=audiobook)
    else:
        return redirect("/admin_login")





"""Podcast"""

@admin.route("/all_podcast")
def all_podcast():
    if "admin" in session:
        cur=db.connection.cursor()
        cur.execute("SELECT * FROM podcast")
        podcasts=cur.fetchall()

        cur=db.connection.cursor()  
        cur.execute("SELECT count(id) from podcast ")
        total_podcasts=cur.fetchone()
        return render_template("admin/podcast.html",podcasts=podcasts,total_podcasts=total_podcasts)
    else:
        return redirect("/admin_login")


@admin.route("/delete_podcast/<int:id>")
def delete_podcast(id):
    if "admin" in session:
        cur=db.connection.cursor()
        cur.execute("DELETE FROM podcast WHERE id=%s",(id,))
        db.connection.commit()
        flash("podcast deleted successfully!",category="error")
        return redirect("/all_podcast")
    
    else:
        return redirect("/admin_login")



@admin.route("/edit_podcast/<int:id>",methods=["POST","GET"])
def edit_podcast(id):
    if "admin" in session:
        cur=db.connection.cursor()
        cur.execute("SELECT * FROM podcast WHERE id=%s",(id,))
        podcast=cur.fetchone()
        if request.method=="POST":
            name=request.form.get("name")
            description=request.form.get("description")
            podcaster=request.form.get("podcaster")

            image = request.files['image']
            audio = request.files['audio']
            if image.filename == '' and audio.filename == "":
                flash('No selected file', category="error")
                return redirect(request.url)
            else:
                cur=db.connection.cursor()
                cur.execute("update podcast set name=%s,description=%s,podcaster=%s,image=%s,audio=%s where id=%s",(name,description,podcaster,image.filename,audio.filename,id,))
                db.connection.commit()
            flash("podcast edited successfully!",category="success")
            return redirect("/all_podcast")
        return render_template("admin/edit_podcast.html",podcast=podcast)
    else:   
        return redirect("/admin_login")



@admin.route("/add_podcast",methods=["GET","POST"])
def add_podcast():
    if "admin" in session:
        if request.method=="POST":
            name=request.form.get("name")
            description=request.form.get("description")
            podcaster=request.form.get("podcaster")
            type=request.form.get("type")

            image = request.files['image']
            audio = request.files['audio']
            if image.filename == '' and audio.filename == "":
                flash('No selected file', category="error")
                return redirect(request.url)
            else:
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(image.filename)))
                audio.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(audio.filename)))
                cur=db.connection.cursor()
                cur.execute("INSERT INTO podcast(name,description,podcaster,image,audio,date,type) VALUES (%s,%s,%s,%s,%s,%s,%s)",(name,description,podcaster,image.filename,audio.filename,datetime.now(),type,))
                db.connection.commit()
                return redirect("/all_podcast")
        return render_template("admin/add_podcast.html")
    
    else:
        return redirect("/admin_login")










"""Book Shop"""
@admin.route("/all_book")
def all_book():
    if "admin" in session:
        cur=db.connection.cursor()
        cur.execute("SELECT * FROM books")
        books=cur.fetchall()

        cur=db.connection.cursor()  
        cur.execute("SELECT count(book_id) from books ")
        total_books=cur.fetchone()
        return render_template("admin/book.html",books=books,total_books=total_books)
    else:
        return redirect("/admin_login")


@admin.route("/delete_book/<int:id>")
def delete_book(id):
    if "admin" in session:
        cur=db.connection.cursor()
        cur.execute("DELETE FROM books WHERE book_id=%s",(id,))
        db.connection.commit()
        return redirect("/all_book")
    
    else:
        return redirect("/admin_login")



@admin.route("/add_book",methods=["GET","POST"])
def add_book():
    if "admin" in session:
        if request.method=="POST":
            name=request.form.get("name")
            description=request.form.get("description")
            price=request.form.get("price")
            category=request.form.get("category")


            image = request.files['image']
            if image.filename == '':
                flash('No selected file', category="error")
                return redirect(request.url)
            else:
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(image.filename)))
                cur=db.connection.cursor()
                cur.execute("INSERT INTO books(name,description,price,image,date,category) VALUES (%s,%s,%s,%s,%s,%s)",(name,description,price,image.filename,datetime.now(),category,))
                db.connection.commit()
                return redirect("/all_book")
        return render_template("admin/add_book.html")
    
    else:
        return redirect("/admin_login")





@admin.route("/all_order_dashboard")
def all_order_in_admin():
    if "admin" in session:
        cur=db.connection.cursor()
        cur.execute("SELECT * FROM orders")
        orders=cur.fetchall()

        cur=db.connection.cursor()  
        cur.execute("SELECT count(order_id) from orders")
        total_orders=cur.fetchone()
        return render_template("admin/orders.html",orders=orders,total_orders=total_orders)
    else:
        return redirect("/admin_login")



@admin.route("/delete_order_dashboard/<int:id>")
def delete_order_dashboard(id):
    if "admin" in session:
        cur=db.connection.cursor()
        cur.execute("DELETE FROM orders WHERE order_id=%s",(id,))
        db.connection.commit()
        return redirect("/all_order_dashboard")
    
    else:
        return redirect("/admin_login")




@admin.route("/all_rent_book")
def all_rent_book():
    if "admin" in session:
        cur=db.connection.cursor()
        cur.execute("SELECT * FROM rents")
        rents=cur.fetchall()

        cur=db.connection.cursor()  
        cur.execute("SELECT count(rent_id) from rents ")
        total_rents=cur.fetchone()
        return render_template("admin/rent.html",rents=rents,total_rents=total_rents)
    else:
        return redirect("/admin_login")




# @admin.route("/all_suscriber_dashboard")
# def all_subscriber_dashboard():
#     if "admin" in session:
#         cur=db.connection.cursor()
#         cur.execute("SELECT * FROM subscriber")
#         subscribers=cur.fetchall()

#         cur=db.connection.cursor()  
#         cur.execute("SELECT count(subscriber_no) from subscriber")
#         total_subscribers=cur.fetchone()
#         return render_template("admin/subscriber.html",subscribers=subscribers,total_subscribers=total_subscribers)
#     else:
#         return redirect("/admin_login")


@admin.route("/delete_subscriber/<int:id>")
def delete_subscriber(id):
    if "admin" in session:
        cur=db.connection.cursor()
        cur.execute("DELETE FROM suscriber WHERE suscriber_no=%s",(id,))
        db.connection.commit()
        return redirect("/dashboard")
    
    else:
        return redirect("/admin_login")

