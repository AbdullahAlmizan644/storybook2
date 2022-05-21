from flask import Flask,Blueprint
from flask_mysqldb import MySQL
from flask_mail import Mail
from flask_ckeditor import CKEditor



db=MySQL()
mail=Mail()
ckeditor=CKEditor()



def create_app():
    UPLOAD_FOLDER = '/home/zeus/storybook2/website/static/image'
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','mp3'}
    app=Flask(__name__)
    app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
    app.config['SECRET_KEY']='mizan_project'
    app.config['MYSQL_HOST']='127.0.0.1'
    app.config['MYSQL_USER']='root'
    app.config['MYSQL_PASSWORD']=''
    app.config['MYSQL_DB']='storybook'

    app.config["MAIL_SERVER"]='smtp.gmail.com' 
    app.config["MAIL_PORT"] = 465
    app.config['MAIL_USE_TLS'] = False  
    app.config['MAIL_USE_SSL'] = True  
    app.config["MAIL_USERNAME"] = 'dekbovideo@gmail.com'  
    app.config['MAIL_PASSWORD'] = '5255452554'  

    db.init_app(app)
    mail.init_app(app)
    ckeditor.init_app(app)


    from .view import view
    from .shop import shop
    from .admin import admin
    from .auth import auth
    from .podcast import podcast
    from .audiobook import audiobook
    from .blog import blog
    from .book_share import book_share
    from .user_dashboard import user_dashboard


    app.register_blueprint(view, url_prefix="/")
    app.register_blueprint(shop, url_prefix="/")
    app.register_blueprint(admin, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(podcast, url_prefix="/")
    app.register_blueprint(audiobook, url_prefix="/")
    app.register_blueprint(blog, url_prefix="/")
    app.register_blueprint(book_share, url_prefix="/")
    app.register_blueprint(user_dashboard, url_prefix="/")

    return app