import email
from flask import Blueprint, redirect, render_template,request,flash,session
from .__init__ import db


shop=Blueprint('shop',__name__)



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
            address=request.form.get("address")
            state=request.form.get("state")
            address=request.form.get("address")
            zip=request.form.get("zip")
            phone=request.form.get("phone")
            email=request.form.get("email")
            notes=request.form.get("notes")
            payment=request.form.get("payment")
            total=request.form.get("total")
            

            cur=db.connection.cursor()
            cur.execute("INSERT INTO orders(username,email,phone,address,state,zip,order_note,product_details,order_total,payment_method,date) VALUES(%s,%s,%s,%s)",(user[1],email,phone,address,state,zip,notes,product_details,order_total,payment,datetime.now(),))
            db.connection.commit()
            cur.close()
            
        
        return render_template("shop/checkout.html")

    else:
        return redirect("/login")

@shop.route("/thankyou")
def thankyou():
    return render_template("shop/thankyou.html")