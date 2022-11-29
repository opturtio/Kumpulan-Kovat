from flask import render_template, request, redirect, abort, session
from app import app
from db import db

@app.route("/", methods=["GET"])
def root(): #nimen voi vaihtaa
    return render_template("index.html")


@app.route("/citations", methods=["GET"])
def citations():
    result = db.session.execute("SELECT citation_name, title, published, author FROM citations")
    citations = result.fetchall()
    return render_template("citations.html", count=len(citations), citations=citations)