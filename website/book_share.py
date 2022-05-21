from flask import Blueprint, redirect, render_template,request,flash,session
from website.__init__ import db,create_app
import os
from werkzeug.utils import secure_filename
from datetime import datetime



book_share=Blueprint('book_share',__name__)
app=create_app()


@book_share.route("/book_share")
def share():
    cur=db.connection.cursor() 
    cur.execute("select * from book_share")
    books=cur.fetchall()
    return render_template("book_share/book_share.html",books=books)



@book_share.route("/share_details/<int:id>")
def share_details(id):
    cur=db.connection.cursor() 
    cur.execute("select * from book_share where share_id=%s",(id,))
    book=cur.fetchone()
    return render_template("book_share/share_details.html",book=book)





