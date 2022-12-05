import unittest
from unittest.mock import Mock
from services.citation_service import CitationService
from services.citation_service import WrongAttributeTypeError


class TestCitationService(unittest.TestCase):
    def setUp(self):
        self.citation_repository_mock = Mock()
        self.citation_service = CitationService(self.citation_repository_mock)
        self.citation = Mock()
        self.citation.citation_name = "test"
        self.citation.title = "testi kirja"
        self.citation.year = 2022
        self.citation.author = "testaaja"
        def returns():
            return {
                "citation_name" : self.citation.citation_name,
                "title" : self.citation.title, 
                "year" : self.citation.year,
                "author" : self.citation.author
            }
        self.citation.get_data.side_effect = returns

    def test_can_add_citation(self):
        self.citation_service.create_citation(self.citation)

        self.citation_repository_mock.insert_citation.assert_called_with(self.citation)

    def test_can_add_multiple_citations(self):
        self.citation_service.create_citation(self.citation)
        self.citation_service.create_citation(self.citation)
        self.citation_service.create_citation(self.citation)

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
    
    def test_citation_validation_returns_an_empty_list_when_correct_attribute_type_is_used(self):
        self.assertEqual(self.citation_service.validate_citation(self.citation), [])

    def test_citation_validation_returns_a_non_empty_list_when_wrong_attribute_type_is_used(self):
        self.citation.year = "test"
        self.assertEqual(type(self.citation_service.validate_citation(self.citation)), list)
        self.assertTrue(len(self.citation_service.validate_citation(self.citation)) > 0)

    def test_create_citation_raises_typeerror_when_wrong_attribute_type_is_used(self):
        self.citation.year = "test"
        self.assertRaises(WrongAttributeTypeError, self.citation_service.create_citation, self.citation)