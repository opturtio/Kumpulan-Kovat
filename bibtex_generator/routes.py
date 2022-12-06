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


@app.route("/new_citation", methods=["GET", "POST"])
def new_citation():
    if request.method == "GET":
        return render_template("new_citation.html", citation = False)

    if request.method == "POST":
        print(request.form["year"])
        citation_object = Citation(
            citation_name = request.form["citation_name"],
            type = "book",
            title = request.form["title"],
            year = request.form["year"],
            author = request.form["author"]
        )
        try:
            citation_service.create_citation(citation_object)
            return redirect_to_new_citation()
        except WrongAttributeTypeError as error:
            return render_template(
                "new_citation.html",
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
