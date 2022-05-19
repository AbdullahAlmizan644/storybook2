from flask import Flask,Blueprint
from flask_mysqldb import MySQL
from flask_mail import Mail



db=MySQL()
mail=Mail()

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


    from .view import view
    from .shop import shop
    from .admin import admin
    from .auth import auth
    from .podcast import podcast
    from .audiobook import audiobook


    app.register_blueprint(view, url_prefix="/")
    app.register_blueprint(shop, url_prefix="/")
    app.register_blueprint(admin, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(podcast, url_prefix="/")
    app.register_blueprint(audiobook, url_prefix="/")

    return app