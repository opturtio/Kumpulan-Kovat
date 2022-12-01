import unittest
from unittest.mock import Mock
from services.citation_service import CitationService


class TestCitationService(unittest.TestCase):
    def setUp(self):
        self.citation_repository_mock = Mock()
        self.citation_service = CitationService(self.citation_repository_mock)

    def test_can_add_citation(self):
        self.citation_service.create_citation(
            "testi", "testi kirja", 2022, "testaaja")

        self.citation_repository_mock.insert_citation.assert_called_with(
            "testi", "testi kirja", 2022, "testaaja")

    def test_can_add_multiple_citations(self):
        self.citation_service.create_citation(
            "testi", "testi kirja", 2022, "testaaja")
        self.citation_service.create_citation(
            "testi2", "testi kirja", 2022, "testaaja")
        self.citation_service.create_citation(
            "testi3", "testi kirja", 2022, "testaaja")

        self.assertEqual(
            self.citation_repository_mock.insert_citation.call_count, 3)

    def test_can_find_specific_citation(self):
        self.citation_service.get_citation(3)

        self.citation_repository_mock.get_citation.assert_called_with(3)

    def test_can_list_all_citations(self):
        def returns():
            return [["testi", "testi kirja", 2022, "testaaja"], ["testi2", "testi kirja", 2022, "testaaja"]]

        self.citation_repository_mock.get_citations.side_effect = returns
        citations = self.citation_service.get_citations()
        print(citations)
        self.assertEqual(len(citations), 2)
