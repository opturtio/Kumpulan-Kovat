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


@app.route("/citations", methods=["GET"])
def citations():
    citations = citation_service.get_citations()
    return render_template("citations.html", count=len(citations), citations=citations)


#@app.route("/new_citation", methods=["GET", "POST"])
#def new_citation():
#    if request.method == "GET":
#        return render_template("new_citation.html", citation = False)
#
#    if request.method == "POST":
#        print(request.form["year"])
#        citation_object = Citation(
#            citation_name = request.form["citation_name"],
#            type = "book",
#            title = request.form["title"],
#            year = request.form["year"],
#            author = request.form["author"]
#        )
#        try:
#            citation_service.create_citation(citation_object)
#            return redirect_to_new_citation()
#        except WrongAttributeTypeError as error:
#            return render_template(
#                "new_citation.html",
#                error_message = "Wrong types for: " + str(error)
#            )

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

        print(citation_object, file=sys.stderr)
        return redirect("/new_book")
#        try:
#            citation_service.create_citation(citation_object)
#            return redirect_to_new_citation()
#        except WrongAttributeTypeError as error:
#            return render_template(
#                "new_citation.html",
#                error_message = "Wrong types for: " + str(error)
#            )

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
        
        return redirect("/new_article")
#        try:
#            citation_service.create_citation(citation_object)
#            return redirect_to_new_citation()
#        except WrongAttributeTypeError as error:
#            return render_template(
#                "new_citation.html",
#                error_message = "Wrong types for: " + str(error)
#            )

@app.route("/new_misc", methods=["GET", "POST"])
def new_misc():
    if request.method == "GET":
        return render_template("new_misc.html", citation = False)

    if request.method == "POST":
        citation_object = Citation(
            type = "article",
            citation_name = request.form["citation_name"],
            title = request.form["title"],
            author = request.form["author"],
            how_published = request.form["how_published"],
            year = request.form["year"],
            note = request.form["note"]
        )
        
        return redirect("/new_misc")
#        try:
#            citation_service.create_citation(citation_object)
#            return redirect_to_new_citation()
#        except WrongAttributeTypeError as error:
#            return render_template(
#                "new_citation.html",
#                error_message = "Wrong types for: " + str(error)
#            )

@app.route("/new_phdthesis", methods=["GET", "POST"])
def new_phdthesis():
    if request.method == "GET":
        return render_template("new_phdthesis.html", citation = False)

    if request.method == "POST":
        citation_object = Citation(
            type = "article",
            citation_name = request.form["citation_name"],
            author = request.form["author"],
            title = request.form["title"],
            school = request.form["school"],
            address = request.form["address"],
            year = request.form["year"],
            month = request.form["month"]
        )
        
        return redirect("/new_phdthesis")
#        try:
#            citation_service.create_citation(citation_object)
#            return redirect_to_new_citation()
#        except WrongAttributeTypeError as error:
#            return render_template(
#                "new_citation.html",
#                error_message = "Wrong types for: " + str(error)

@app.route("/new_inproceedings", methods=["GET", "POST"])
def new_inproceedings():
    if request.method == "GET":
        return render_template("new_inproceedings.html", citation = False)

    if request.method == "POST":
        citation_object = Citation(
            type = "article",
            citation_name = request.form["citation_name"],
            author = request.form["author"],
            title = request.form["title"],
            book_title = request.form["book_title"],
            series = request.form["series"],
            year = request.form["year"],
            pages = request.form["pages"],
            publisher = request.form["publisher"],
            address = request.form["address"]
        )
        
        return redirect("/new_inproceedings")
#        try:
#            citation_service.create_citation(citation_object)
#            return redirect_to_new_citation()
#        except WrongAttributeTypeError as error:
#            return render_template(
#                "new_citation.html",
#                error_message = "Wrong types for: " + str(error)

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
