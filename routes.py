from flask import render_template, request, redirect

@app.route("/", methods=["GET"]):
def root(): #nimen voi vaihtaa
    return render_template("index.html")