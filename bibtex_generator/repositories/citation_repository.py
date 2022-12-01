
from entities.citation import Citation
from db import db

class CitationRepository:
    def __init__(self):
        self._citation = Citation()

    def insert_citation(self, citation_name, title, published, author):
        sql = """INSERT INTO citations (citation_name, title, published, author)
                 VALUES (:citation_name, :title, :published, :author)"""
        db.session.execute(sql, {
                                "citation_name":citation_name,
                                "title":title,
                                "published":published,
                                "author":author
                                }
                           )
        db.session.commit()

    def something(self):
        pass




citation_repository = CitationRepository()
