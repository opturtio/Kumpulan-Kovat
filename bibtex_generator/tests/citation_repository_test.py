import unittest
from unittest.mock import Mock
from repositories.citation_repository import CitationRepository
from entities import Citation

class TestCitationRepository(unittest.TestCase):
    def setUp(self):
        self.db_mock = Mock()
        self.citation_repository = CitationRepository(self.db_mock)
        self.book = Citation(
            citation_name = "testi",
            type = "book",
            author = "testaaja",
            title = "testi kirja",
            publisher = "testaaja",
            address = "testi osoite",
            year = "2022"
        )
 

    def test_insert_book_citation(self):
        self.citation_repository.insert_book_citation(self.book)
        self.db_mock.session.execute.assert_called()

    def test_remove_citation(self):
        self.citation_repository.remove_citation(4)
        self.db_mock.session.execute.assert_called_with("DELETE FROM citations WHERE id=:number", {
            "number": 4
        })

    def test_get_citations(self):
        self.citation_repository.get_citations()
        self.db_mock.session.execute.called_with("""SELECT * FROM citations""")
