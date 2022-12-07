from entities.citation import Citation
from db import db
from flask import request

class CitationRepository:
    def __init__(self, db):
        self._citation = Citation()
        self._db = db

    def insert_book_citation(self, citation_object):
        sql = """INSERT INTO citations (citation_name, type, author, title, publisher, address, year)
                 VALUES (:citation_name, :type, :author, :title, :publisher, :address, :year)"""
        self._db.session.execute(sql, {
            "citation_name": citation_object.citation_name,
            "type": citation_object.type,
            "author": citation_object.author,
            "title": citation_object.title,
            "publisher": citation_object.publisher,
            "address": citation_object.address,
            "year": citation_object.year
        })
        self._db.session.commit()

    def insert_article_citation(self, citation_object):
        sql = """INSERT INTO citations (citation_name, type, author, title, journal, year, volume, number, pages)
                 VALUES (:citation_name, :type, :author, :title, :journal, :year, :volume, :number, :pages)"""
        self._db.session.execute(sql, {
            "citation_name": citation_object.citation_name,
            "type": citation_object.type,
            "author": citation_object.author,
            "title": citation_object.title,
            "journal": citation_object.journal,
            "year": citation_object.year,
            "volume": citation_object.volume,
            "number": citation_object.number,
            "pages": citation_object.pages
        })
        self._db.session.commit()

    def insert_misc_citation(self, citation_object):
        sql = """INSERT INTO citations (citation_name, type, author, title, howpublished, year, note)
                 VALUES (:citation_name, :type, :author, :title, :howpublished, :year, :note)"""
        self._db.session.execute(sql, {
            "citation_name": citation_object.citation_name,
            "type": citation_object.type,
            "author": citation_object.author,
            "title": citation_object.title,
            "howpublished": citation_object.howpublished,
            "year": citation_object.year,
            "note": citation_object.note
        })
        self._db.session.commit()

    def insert_phdthesis_citation(self, citation_object):
        sql = """INSERT INTO citations (citation_name, type, author, title, school, address, year, month)
                 VALUES (:citation_name, :type, :author, :title, :school, :address, :year, :month)"""
        self._db.session.execute(sql, {
            "citation_name": citation_object.citation_name,
            "type": citation_object.type,
            "author": citation_object.author,
            "title": citation_object.title,
            "school": citation_object.school,
            "address": citation_object.address,
            "year": citation_object.year,
            "month": citation_object.month
        })
        self._db.session.commit()

    def insert_inproceedings_citation(self, citation_object):
        sql = """INSERT INTO citations (citation_name, type, author, title, booktitle, series, year, pages, publisher, address)
                 VALUES (:citation_name, :type, :author, :title, :booktitle, :series, :year, :pages, :publisher, :address)"""
        self._db.session.execute(sql, {
            "citation_name": citation_object.citation_name,
            "type": citation_object.type,
            "author": citation_object.author,
            "title": citation_object.title,
            "booktitle": citation_object.booktitle,
            "series": citation_object.series,
            "year": citation_object.year,
            "pages": citation_object.pages,
            "publisher": citation_object.publisher,
            "address": citation_object.address
        })
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
