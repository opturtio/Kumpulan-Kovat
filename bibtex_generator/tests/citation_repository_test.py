import unittest
from unittest.mock import Mock
from repositories.citation_repository import CitationRepository
from entities import Citation

class TestCitationRepository(unittest.TestCase):
    def setUp(self):
        self.db_mock = Mock()
        self.citation_repository = CitationRepository(self.db_mock)
        self.book = Citation(
            id = 1,
            citation_name = "testi",
            type = "book",
            author = "testaaja",
            title = "testi kirja",
            publisher = "testaaja",
            address = "testi osoite",
            year = "2022"
        )
        self.article = Citation(
            citation_name = "testi",
            type = "article",
            author = "testaaja",
            title = "testi kirja",
            journal = "testi",
            year = "2022",
            volume = "1",
            number = "2",
            pages = "1--10"
            )
        self.inproceedings = Citation(
            citation_name = "testi",
            type = "inproceedings",
            author = "testaaja",
            title = "testi kirja",
            booktitle = "testi otsikko",
            series = "testi sarja",
            year = "2022",
            pages = "1--10",
            publisher = "testaaja",
            address = "testi osoite"
            )
        self.misc = Citation(
            citation_name = "testi",
            type = "misc",
            title = "testi kirja",
            author = "testaaja",
            howpublished = r"\url{https://www.test.com}",
            year = "2022",
            note = "Lorem ipsum"
            )
        self.phdthesis = Citation(
            citation_name = "testi",
            type = "phdthesis",
            author = "testaaja",
            title = "testi kirja",
            school = "testi koulu",
            address = "testi osoite",
            year = "2022",
            month = "joulukuu"
            )


    def test_insert_book_citation(self):
        self.citation_repository.insert_book_citation(self.book)
        self.db_mock.session.execute.assert_called()

    def test_insert_article_citation(self):
        self.citation_repository.insert_article_citation(self.article)
        self.db_mock.session.execute.assert_called()

    def test_insert_misc_citation(self):
        self.citation_repository.insert_misc_citation(self.misc)
        self.db_mock.session.execute.assert_called()

    def test_insert_phdthesis_citation(self):
        self.citation_repository.insert_phdthesis_citation(self.phdthesis)
        self.db_mock.session.execute.assert_called()

    def test_insert_inproceedings_citation(self):
        self.citation_repository.insert_inproceedings_citation(self.inproceedings)
        self.db_mock.session.execute.assert_called()


    def test_remove_citation(self):
        self.citation_repository.remove_citation(4)
        self.db_mock.session.execute.assert_called_with("DELETE FROM citations WHERE id=:number", {
            "number": 4
        })

    def test_get_citations(self):
        self.citation_repository.get_citations()
        self.db_mock.session.execute.called_with("""SELECT * FROM citations""")

    def test_get_citation(self):
        self.citation_repository.insert_book_citation(self.book)
        self.citation_repository.get_citation(1)
        self.db_mock.session.execute.assert_called_with("SELECT * FROM citations WHERE id=:id", {"id": 1})

    def test_citation_search(self):
        self.citation_repository.insert_book_citation(self.book)
        self.citation_repository.citation_search("testi")
        self.db_mock.session.execute.assert_called_with(
            "SELECT * FROM citations WHERE lower(citation_name) LIKE :query or lower(type) LIKE :query", {"query": "%testi%"})

