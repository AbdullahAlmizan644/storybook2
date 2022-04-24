from flask import Blueprint, render_template

view=Blueprint('view',__name__)


@view.route("/")
def index():
    return render_template("view/index.html")


@view.route("/about")
def about():
    return render_template("view/about.html")



@view.route("/contact")
def contact():
    return render_template("view/contact.html")



@view.route("/service")
def service():
    return render_template("view/service.html")



@view.route("/audiobook2")
def audiobook():
    return render_template("view/audiobooks.html")

@view.route("/author")
def author():
    return render_template("view/author.html")


@view.route("/author_deatils")
def author_deatils():
    return render_template("view/author_deatils.html")

@view.route("/chapter")
def chapter():
    return render_template("view/chapter.html")