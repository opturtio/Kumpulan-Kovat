import unittest
import os
from unittest.mock import Mock
from services import BibtexService
from entities import Citation

class TestBibtexFromatter(unittest.TestCase):
    def setUp(self):
        self.citation_service = Mock()
        self.citation_service.get_citation.return_value = {"test_a" : 1, "test_b" : 2, "test_c" : 3, "test_d" : 4}
        self.bibtex_formatter_function = Mock()
        def method(citation = None):
            try:
                if citation is not None:
                    return citation.bib
            except AttributeError:
                return "test_a 1\n test_b 2\n test_c 3\n test_d 4"
        self.bibtex_formatter_function.side_effect = method
        self.bibtex_service = BibtexService(self.citation_service, self.bibtex_formatter_function)
        self.citations = [Mock(), Mock(), Mock(), Mock()]
        self.citations[0].bib = "bibtex 1"
        self.citations[1].bib = "bibtex 2"
        self.citations[2].bib = "bibtex 3"
        self.citations[3].bib = "bibtex 4"
        self.id_list = [1,2,3,4]

    def test_get_citations_asks_citation_service_for_citations_when_given_a_list_of_ids(self):
        self.bibtex_service._get_citations(self.id_list)
        self.assertEqual(self.citation_service.get_citation.call_count, 4)
        self.citation_service.get_citation.assert_any_call(self.id_list[0])
        self.citation_service.get_citation.assert_any_call(self.id_list[1])
        self.citation_service.get_citation.assert_any_call(self.id_list[2])
        self.citation_service.get_citation.assert_any_call(self.id_list[3])
    
    def test_get_citation_returns_a_list_of_citations_when_given_a_list_of_ids(self):
        return_val = self.bibtex_service._get_citations(self.id_list)
        self.assertEqual(type(return_val), list)
        self.assertEqual(len(return_val), 4)
        for item in return_val:
            self.assertEqual(type(item), Citation)
    
    def test_convert_to_citation_returns_a_citation_object_when_given_a_row_element(self):
        row_element = {"a" : 1, "b" : 2, "c" : 3, "d" : 4}
        return_val = self.bibtex_service._convert_to_citation(row_element)
        self.assertEqual(type(return_val), Citation)

    def test_citations_to_bibtex_asks_the_bibtex_formatter_to_generate_a_bibtex_string(self):
        self.bibtex_service._convert_citations_to_bibtex(self.citations)
        self.assertEqual(self.bibtex_formatter_function.call_count, 4)
        self.bibtex_formatter_function.assert_any_call(self.citations[0])
        self.bibtex_formatter_function.assert_any_call(self.citations[1])
        self.bibtex_formatter_function.assert_any_call(self.citations[2])
        self.bibtex_formatter_function.assert_any_call(self.citations[3])
    
    def test_citations_to_bibtex_returns_a_string_containing_the_provided_citations(self):
        return_val = self.bibtex_service._convert_citations_to_bibtex(self.citations)
        self.assertIn(self.citations[0].bib, return_val)
        self.assertIn(self.citations[1].bib, return_val)
        self.assertIn(self.citations[2].bib, return_val)
        self.assertIn(self.citations[3].bib, return_val)

    def test_generate_bibtex_file_creates_references_bib_when_passed_a_list_of_ids(self):
        self.bibtex_service.generate_bibtex_file(self.id_list)
        with open("references.bib", "r") as file:
            text = file.read()
            for key in self.citation_service.get_citation().keys():
                self.assertIn(key, text)
    
    def test_generate_bibtex_file_creates_references_bib_when_passed_a_list_of_row_elements(self):
        self.bibtex_service.generate_bibtex_file(self.citations)
        with open("references.bib", "r") as file:
            text = file.read()
            for key in self.citations:
                self.assertIn(key.bib, text)
