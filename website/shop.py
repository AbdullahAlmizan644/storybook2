from flask import Blueprint, redirect, render_template
from .__init__ import db


shop=Blueprint('shop',__name__)



@shop.route("/shop")
def shops():
    cur=db.connection.cursor()
    cur.execute("SELECT * FROM books")    
    books=cur.fetchall()
    return render_template("shop/shop.html",books=books)



@shop.route("/book_details/<int:sno>")
def book_details(sno):
    cur=db.connection.cursor()
    cur.execute("SELECT * FROM books where book_id=%s",(sno,))    
    book=cur.fetchone()
    return render_template("shop/book_details.html",book=book)