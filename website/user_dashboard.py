from flask import Blueprint, redirect, render_template,request,flash,session
from website.__init__ import db,create_app
import os
from werkzeug.utils import secure_filename
from datetime import datetime



user_dashboard=Blueprint('user_dashboard',__name__)
app=create_app()


@user_dashboard.route("/user_dashboard")
def user_dash():
    if "user" in session:
        cur=db.connection.cursor() 
        cur.execute("select * from orders where username=%s",(session["user"],))
        orders=cur.fetchall()


        cur=db.connection.cursor()
        cur.execute("SELECT count(share_id) from book_share where username=%s",(session["user"],))
        total_book_share=cur.fetchone()


        cur=db.connection.cursor()
        cur.execute("SELECT count(post_id) from blog where writer=%s",(session["user"],))
        total_post=cur.fetchone()


        cur=db.connection.cursor()
        cur.execute("SELECT count(order_id) from orders where username=%s",(session["user"],))
        total_orders=cur.fetchone()


        cur=db.connection.cursor()
        cur.execute("SELECT count(rent_id) from rents where username=%s",(session["user"],))
        total_rents=cur.fetchone()

        return render_template("user_dashboard/user_dashboard.html",orders=orders,total_book_share=total_book_share,total_orders=total_orders,total_rents=total_rents,total_post=total_post)
    else:
        return redirect("/login")



@user_dashboard.route("/write_post",methods=["POST","GET"])
def write_post():
    if "user" in session:
        


        cur=db.connection.cursor() 
        cur.execute("select * from users where username=%s",(session["user"],))
        user=cur.fetchone()
        if request.method=="POST":
            name=request.form.get("name")
            details=request.form.get('ckeditor')

                        
            cur=db.connection.cursor()
            cur.execute("INSERT INTO blog(title,details,writer,writer_image,date) VALUES(%s,%s,%s,%s,%s)",(name,details,user[1],user[4],datetime.now(),))
            db.connection.commit()
            cur.close()
            flash("Blog Share Successfully!",category="success")
            return redirect("/all_user_post")
        return render_template("user_dashboard/write_post.html")
    else:
        return redirect("/login")



@user_dashboard.route("/edit_post/<int:id>",methods=["POST","GET"])
def edit_post(id):
    if "user" in session:
        cur=db.connection.cursor() 
        cur.execute("select * from blog where post_id=%s",(id,))
        post=cur.fetchone()
        if request.method=="POST":
            name=request.form.get("name")
            details=request.form.get('ckeditor')

                        
            cur=db.connection.cursor()
            cur.execute("UPDATE blog  set title=%s, details=%s where post_id=%s",(name,details,id,))
            db.connection.commit()
            cur.close()
            flash("Edit Book Successfully!",category="success")
            return redirect("/all_user_post")
        return render_template("user_dashboard/edit_user_post.html",post=post)
    else:
        return redirect("/login")


@user_dashboard.route("all_user_post")
def user_all_post():
    if "user" in session:
        cur=db.connection.cursor()
        cur.execute("SELECT count(post_id) from blog where writer=%s",(session["user"],))
        total_post=cur.fetchone()

        cur=db.connection.cursor() 
        cur.execute("select * from blog where writer=%s",(session["user"],))
        posts=cur.fetchall()
        return render_template("user_dashboard/user_all_post.html",posts=posts,total_post=total_post)
    
    else:
        return redirect("/login")

@user_dashboard.route("/delete_post/<int:id>")
def delete_post(id):
    if "user" in session:
        cur=db.connection.cursor() 
        cur.execute("DELETE from blog where post_id=%s",(id,))
        db.connection.commit()
        flash("delete post",category="error")
        return redirect("/all_user_post")
    else:
        return redirect("/login")






@user_dashboard.route("/book_share_post",methods=["GET","POST"])
def share_post():
    if "user" in session:
        cur=db.connection.cursor() 
        cur.execute("select * from users where username=%s",(session["user"],))
        user=cur.fetchone()

        cur=db.connection.cursor() 
        cur.execute("select * from book_share where username=%s",(session["user"],))
        posts=cur.fetchall()

        if request.method=="POST":
            name=request.form.get("name")
            image = request.files['image']
            details=request.form.get('ckeditor')
            phone=request.form.get('phone')
            
            
            if image.filename == '':
                flash('No selected file', category="error")
                return redirect(request.url)
            else:
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(image.filename)))        
                cur=db.connection.cursor() 
                cur.execute("INSERT INTO book_share(username,image,email,book_name,book_image,details,phone,date) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",(user[1],user[3],user[2],name,image.filename,details,phone,datetime.now(),))
                db.connection.commit()
                cur.close()
                flash("Post Share Successfully!",category="success")
                return redirect("/all_book_share_post")
    return render_template("user_dashboard/book_share_post.html")


@user_dashboard.route("/edit_book_share_post/<int:id>",methods=["POST","GET"])
def edit_book_share_post(id):
    if "user" in session:
        cur=db.connection.cursor() 
        cur.execute("select * from users where username=%s",(session["user"],))
        user=cur.fetchone()

        cur=db.connection.cursor() 
        cur.execute("select * from book_share where share_id=%s",(id,))
        post=cur.fetchone()

        if request.method=="POST":
            name=request.form.get("name")
            image = request.files['image']
            details=request.form.get('ckeditor')
            phone=request.form.get('phone')
            
            
            if image.filename == '':
                flash('No selected file', category="error")
                return redirect(request.url)
            else:
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(image.filename)))        
                cur=db.connection.cursor() 
                cur.execute("INSERT INTO book_share(username,image,email,book_name,book_image,details,phone,date) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",(user[1],user[3],user[2],name,image.filename,details,phone,datetime.now(),))
                db.connection.commit()
                cur.close()
                flash("Edit Post Share Successfully!",category="success")
                return redirect("/all_book_share_post")
    return render_template("user_dashboard/edit_book_share_post.html",post=post)


@user_dashboard.route("all_book_share_post")
def all_book_share_post():
    if "user" in session:

        cur=db.connection.cursor()
        cur.execute("SELECT count(share_id) from book_share where username=%s",(session["user"],))
        total_book_share=cur.fetchone()

        cur=db.connection.cursor() 
        cur.execute("select * from book_share where username=%s",(session["user"],))
        posts=cur.fetchall()
        return render_template("user_dashboard/all_book_share_post.html",posts=posts,total_book_share=total_book_share)
    
    else:
        return redirect("/login")

@user_dashboard.route("/delete_book_share_post/<int:id>")
def delete_book_share_post(id):
    if "user" in session:
        cur=db.connection.cursor() 
        cur.execute("DELETE from book_share where share_id=%s",(id,))
        db.connection.commit()
        flash("delete post",category="error")
        return redirect("/all_book_share_post")
    else:
        return redirect("/login")


@user_dashboard.route("/user_order_history")
def order_history():
    if "user" in session:
        cur=db.connection.cursor() 
        cur.execute("select * from orders where username=%s",(session["user"],))
        orders=cur.fetchall()

        cur=db.connection.cursor()
        cur.execute("SELECT count(order_id) from orders where username=%s",(session["user"],))
        total_orders=cur.fetchone()
        return render_template("user_dashboard/order_history.html",orders=orders,total_orders=total_orders)
    else:
        return redirect("/login")



@user_dashboard.route("/user_rent_history")
def rent_history():
    if "user" in session:
        cur=db.connection.cursor() 
        cur.execute("select * from rents where username=%s",(session["user"],))
        rents=cur.fetchall()

        cur=db.connection.cursor()
        cur.execute("SELECT count(rent_id) from rents where username=%s",(session["user"],))
        total_rents=cur.fetchone()
        return render_template("user_dashboard/rent_history.html",total_rents=total_rents,rents=rents)
    else:
        return redirect("/login")




