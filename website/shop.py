from datetime import datetime
import email
from flask import Blueprint, redirect, render_template,request,flash,session
from .__init__ import db,create_app
from flask_mail import Mail,Message


shop=Blueprint('shop',__name__)

app=create_app()
mail=Mail()

@shop.route("/shop")
def shops():

    cur=db.connection.cursor()
    cur.execute("SELECT count(book_id) from books")
    total_books=cur.fetchone()


    cur=db.connection.cursor()
    cur.execute("SELECT * FROM books")    
    books=cur.fetchall()
    return render_template("shop/shop.html",books=books)



@shop.route("/book_details/<int:sno>/<int:count>")
def book_details(sno,count):
    cur=db.connection.cursor()
    cur.execute("SELECT * FROM books where book_id=%s",(sno,))    
    book=cur.fetchone()
    return render_template("shop/book_details.html",book=book,count=count)


@shop.route("/book_category/<string:cat>")
def book_category(cat):
    cur=db.connection.cursor()
    cur.execute("SELECT * FROM books where category=%s",(cat,))    
    books=cur.fetchall()
    return render_template("shop/book_category.html",books=books,cat=cat)



@shop.route("/rent_checkout/<int:id>",methods=["GET","POST"])
def rent_checkout(id):
    if "user" in session:
        cur=db.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username=%s",(session["user"],))    
        user=cur.fetchone()

        cur=db.connection.cursor()
        cur.execute("SELECT * FROM books WHERE book_id=%s",(id,))    
        book=cur.fetchone()
        if request.method=="POST":
            address=request.form.get("address")
            phone=request.form.get("phone")
            payment=request.form.get("payment")

            cur=db.connection.cursor() 
            cur.execute("INSERT INTO rents(username,email,phone,address,product_name,date,payment_method) VALUES(%s,%s,%s,%s,%s,%s,%s)",(user[1],user[2],phone,address,book[1],datetime.now(),payment,))
            db.connection.commit()
            cur.close()
            m=f"Product:{book[1]} Address:{address} Rent cost:50Tk"

            msg = Message("Book rent",sender="dekbovideo@gmail.com",recipients=[user[2]])
            msg.html = f'<h1>Your Rent Taken<h1><br><h2>{m}</h2>'  
            mail.send(msg)

            flash("Send Mail",category="success")
            return redirect("/rent_thankyou")           
        return render_template("shop/rent_checkout.html",book=book)

    else:
        return redirect("/login")


@shop.route("/rent_thankyou")
def rent_thankyou():
    return render_template("shop/rent_thankyou.html")

@shop.route("/cart")
def cart():
    return render_template("shop/cart.html")



@shop.route("/checkout",methods=["GET","POST"])
def checkout():
    if "user" in session:
        cur=db.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username=%s",(session["user"],))    
        user=cur.fetchone()
        if request.method=="POST":
            state=request.form.get("state")
            address=request.form.get("address")
            zip=request.form.get("zip")
            phone=request.form.get("phone")
            notes=request.form.get("notes")
            payment=request.form.get("payment")
            product=request.form.get("product_details")
            total=request.form.get("total")

            cur=db.connection.cursor() 
            cur.execute("INSERT INTO orders(username,email,phone,address,state,zip,order_note,product_details,payment_method,date,order_total) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(user[1],user[2],phone,address,state,zip,notes,product,payment,datetime.now(),total,))
            db.connection.commit()
            cur.close()
            m=f"Product:{product} Address:{address} Total Price:{total}"

            msg = Message("Book Order",sender="dekbovideo@gmail.com",recipients=[user[2]])
            msg.html = f'<h1>Your Order Taken<h1><br><h2>{m}</h2>'  
            mail.send(msg)

            flash("Send Mail",category="success")
            return redirect("/thankyou")           
        return render_template("shop/checkout.html")

    else:
        return redirect("/login")


@shop.route("/thankyou")
def thankyou():
    return render_template("shop/thankyou.html")