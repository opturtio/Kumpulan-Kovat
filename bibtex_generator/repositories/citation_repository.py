from entities.citation import Citation
from db import db


class CitationRepository:
    def __init__(self, db):
        self._citation = Citation()
        self._db = db

    def insert_citation(self, citation_name, title, published, author):
        sql = """INSERT INTO citations (citation_name, title, published, author)
                 VALUES (:citation_name, :title, :published, :author)"""
        self._db.session.execute(sql, {
            "citation_name": citation_name,
            "title": title,
            "published": published,
            "author": author
        }
        )
        self._db.session.commit()

    def get_citation(self, id):
        sql = "SELECT id, citation_name, title, published, author FROM citations WHERE id=:id"
        result = self._db.session.execute(sql, {"id": id})
        citation = result.fetchone()
        return citation

    def get_citations(self):
        result = self._db.session.execute("""SELECT id, citation_name, title, published, author
                                             FROM citations""")
        citations = result.fetchall()
        return citations
