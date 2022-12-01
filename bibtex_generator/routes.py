from flask import render_template, request, redirect, abort, session
from app import app
from db import db
from services.citation_service import citation_service


def redirect_to_new_citation():
    return redirect("/new_citation")


@app.route("/", methods=["GET"])
def root():
    return render_template("index.html")


@app.route("/citations", methods=["GET"])
def citations():
    result = db.session.execute("SELECT citation_name, title, published, author FROM citations")
    citations = result.fetchall()
    return render_template("citations.html", count=len(citations), citations=citations)


@app.route("/new_citation", methods=["GET", "POST"])
def new_citation():
    if request.method == "GET":
        return render_template("new_citation.html")

    if request.method == "POST":
        citation_name = request.form["citation_name"]
        title = request.form["title"]
        published = request.form["published"]
        author = request.form["author"]

        citation_service.create_citation(citation_name, title, published, author)

        return redirect_to_new_citation()
