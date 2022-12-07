from entities.citation import Citation
from db import db


class CitationRepository:
    def __init__(self, db):
        self._citation = Citation()
        self._db = db

    def insert_citation(self, citation_object):
        sql = """INSERT INTO citations (citation_name, type, title, year, author)
                 VALUES (:citation_name, :type, :title, :year, :author)"""
        self._db.session.execute(sql, {
            "citation_name": citation_object.citation_name,
            "type": citation_object.type,
            "title": citation_object.title,
            "year": citation_object.year,
            "author": citation_object.author
        }
        )
        self._db.session.commit()

    def get_citation(self, id):
        sql = "SELECT * FROM citations WHERE id=:id"
        result = self._db.session.execute(sql, {"id": id})
        citation = result.fetchone()
        return citation

    def get_citations(self):
        result = self._db.session.execute("""SELECT * FROM citations""")
        citations = result.fetchall()
        return citations

    def citation_search(self, query):
        sql = "SELECT * FROM citations " \
              "WHERE lower(citation_name) LIKE :query or lower(type) LIKE :query"
        result = db.session.execute(sql, {"query": "%" + query + "%"})
        citations = result.fetchall()
        return citations

    def remove_citation(self, id):
        sql = "DELETE FROM citations WHERE id=:number"
        self._db.session.execute(sql, {"number": id})
        self._db.session.commit()
