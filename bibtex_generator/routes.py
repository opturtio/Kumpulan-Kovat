import sys
from flask import render_template, request, redirect, abort, session
from app import app
from db import db
from entities import Citation
from entities.bibtex_formatter import create_bibtex_citation_html
from services.citation_service import CitationService, WrongAttributeTypeError
from repositories.citation_repository import CitationRepository

citation_service = CitationService(CitationRepository(db))


def redirect_to_new_citation():
    return redirect("/new_citation")


@app.route("/", methods=["GET"])
def root():
    return render_template("index.html")


@app.route("/citations", methods=["GET", "POST"])
def citations():
    if request.method == "GET":
        citations = citation_service.get_citations()
        return render_template("citations.html", count=len(citations), citations=citations)

    if request.method == "POST":
        id = request.form["remove"]
        citation_service.remove_citation(id)
        citations = citation_service.get_citations()
        return render_template("citations.html", count=len(citations), citations=citations)


@app.route("/doi", methods=["GET", "POST"])
def doi():
    if request.method == "GET":
        return render_template("doi.html", citation = False)

    if request.method == "POST":
        pass


@app.route("/new_book", methods=["GET", "POST"])
def new_book():
    if request.method == "GET":
        return render_template("new_book.html", citation = False)

    if request.method == "POST":
        citation_object = Citation(
            type = "book",
            citation_name = request.form["citation_name"],
            author = request.form["author"],
            title = request.form["title"],
            publisher = request.form["publisher"],
            address = request.form["address"],
            year = request.form["year"]
        )

        try:
            citation_service.create_book_citation(citation_object)
            return redirect("/new_book")
        except WrongAttributeTypeError as error:
            return render_template(
                "new_book.html",
                error_message = "Wrong types for: " + str(error)
            )


@app.route("/new_article", methods=["GET", "POST"])
def new_article():
    if request.method == "GET":
        return render_template("new_article.html", citation = False)

    if request.method == "POST":
        citation_object = Citation(
            type = "article",
            citation_name = request.form["citation_name"],
            author = request.form["author"],
            title = request.form["title"],
            journal = request.form["journal"],
            year = request.form["year"],
            volume = request.form["volume"],
            number = request.form["number"],
            pages = request.form["pages"]
        )

        try:
            citation_service.create_article_citation(citation_object)
            return redirect("/new_article")
        except WrongAttributeTypeError as error:
            return render_template(
                "new_article.html",
                error_message = "Wrong types for: " + str(error)
            )


@app.route("/new_misc", methods=["GET", "POST"])
def new_misc():
    if request.method == "GET":
        return render_template("new_misc.html", citation = False)

    if request.method == "POST":
        citation_object = Citation(
            type = "misc",
            citation_name = request.form["citation_name"],
            title = request.form["title"],
            author = request.form["author"],
            howpublished = request.form["how_published"],
            year = request.form["year"],
            note = request.form["note"]
        )

        try:
            citation_service.create_misc_citation(citation_object)
            return redirect("/new_misc")
        except WrongAttributeTypeError as error:
            return render_template(
                "new_misc.html",
                error_message = "Wrong types for: " + str(error)
            )


@app.route("/new_phdthesis", methods=["GET", "POST"])
def new_phdthesis():
    if request.method == "GET":
        return render_template("new_phdthesis.html", citation = False)

    if request.method == "POST":
        citation_object = Citation(
            type = "phdthesis",
            citation_name = request.form["citation_name"],
            author = request.form["author"],
            title = request.form["title"],
            school = request.form["school"],
            address = request.form["address"],
            year = request.form["year"],
            month = request.form["month"]
        )

        try:
            citation_service.create_phdthesis_citation(citation_object)
            return redirect("/new_phdthesis")
        except WrongAttributeTypeError as error:
            return render_template(
                "new_phdthesis.html",
                error_message = "Wrong types for: " + str(error)
            )


@app.route("/new_inproceedings", methods=["GET", "POST"])
def new_inproceedings():
    if request.method == "GET":
        return render_template("new_inproceedings.html", citation = False)

    if request.method == "POST":
        citation_object = Citation(
            type = "inproceedings",
            citation_name = request.form["citation_name"],
            author = request.form["author"],
            title = request.form["title"],
            booktitle = request.form["book_title"],
            series = request.form["series"],
            year = request.form["year"],
            pages = request.form["pages"],
            publisher = request.form["publisher"],
            address = request.form["address"]
        )

        try:
            citation_service.create_inproceedings_citation(citation_object)
            return redirect("/new_inproceedings")
        except WrongAttributeTypeError as error:
            return render_template(
                "new_inproceedings.html",
                error_message = "Wrong types for: " + str(error)
            )


@app.route("/citations/<int:id>")
def citation(id):
    citation = citation_service.get_citation(id)
    bibtex_string = create_bibtex_citation_html(citation)
    return render_template("citation.html", id=id, citation=citation, bibtex_string=bibtex_string)


@app.route("/search")
def result():
    prequery = request.args["query"]
    query = prequery.lower()
    citations = citation_service.citation_search(query)
    return render_template("citations.html", citations=citations)


@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "GET":
        return render_template("upload.html", citation = False)

    if request.method == "POST":
        pass
