from flask import Blueprint, redirect, render_template,request,flash,session
from website.__init__ import db,create_app
import os
from werkzeug.utils import secure_filename
from datetime import datetime



blog=Blueprint('blog',__name__)
app=create_app()


@blog.route("/blog")
def blog_post():
    cur=db.connection.cursor() 
    cur.execute("select * from blog")
    posts=cur.fetchall()
    return render_template("blog/blog.html",posts=posts)



@blog.route("/post/<int:id>")
def post(id):
    cur=db.connection.cursor() 
    cur.execute("select * from blog where post_id=%s",(id,))
    post=cur.fetchone()
    return render_template("blog/post.html",post=post)




