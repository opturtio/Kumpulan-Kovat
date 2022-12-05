from entities.citation import Citation
from db import db
from flask import request

class CitationRepository:
    def __init__(self, db):
        self._citation = Citation()
        self._db = db

    def insert_citation(self, citation_object):
        sql = """INSERT INTO citations (citation_name, title, year, author)
                 VALUES (:citation_name, :title, :year, :author)"""
        self._db.session.execute(sql, {
            "citation_name": citation_object.citation_name,
            "title": citation_object.title,
            "year": citation_object.year,
            "author": citation_object.author
        }
        )
        self._db.session.commit()

    def get_citation(self, id):
        sql = "SELECT id, citation_name, title, year, author FROM citations WHERE id=:id"
        result = self._db.session.execute(sql, {"id": id})
        citation = result.fetchone()
        return citation

    def get_citations(self):
        result = self._db.session.execute("""SELECT id, citation_name, title, year, author
                                             FROM citations""")
        citations = result.fetchall()
        return citations

    def citation_search(self):
        prequery = request.args["query"]
        query = prequery.lower()
        sql = "SELECT id, citation_name, type, title, year, author FROM citations " \
              "WHERE lower(citation_name) LIKE :query or lower(type) LIKE :query"
        result = db.session.execute(sql, {"query": "%" + query + "%"})
        citations = result.fetchall()
        return citations
