import unittest
import os
from unittest.mock import Mock
from services import BibtexService
from entities import Citation

class TestBibtexService(unittest.TestCase):
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

    def test_parse_type_parses_the_type_correctly(self):
        bibtex_string = '''@book{book1
            author: "author1"
            title: "title1"
            publisher: "publisher1"
            address: "address1"
            year: "2001"
        }
        '''
        self.assertEqual(self.bibtex_service._parse_type(bibtex_string), "book")

    def test_parse_name_parses_the_name_correctly(self):
        bibtex_string = '''@book{book1
            author: "author1"
            title: "title1"
            publisher: "publisher1"
            address: "address1"
            year: "2001"
        }
        '''
        self.assertEqual(self.bibtex_service._parse_name(bibtex_string), "book1")

    def test_parse_book_parses_the_citation_field_correctly(self):
        bibtex_string = '''@book{book1
            author: "author1"
            title: "title1"
            publisher: "publisher1"
            address: "address1"
            year: "2001"
        }
        '''
        return_value = self.bibtex_service._parse_book(bibtex_string).items()
        self.assertIn(('author', 'author1'), return_value)
        self.assertIn(('title', 'title1'), return_value)
        self.assertIn(('publisher', 'publisher1'), return_value)
        self.assertIn(('address', 'address1'), return_value)
        self.assertIn(('year', '2001'), return_value)

    def test_parse_article_parses_the_citation_field_correctly(self):
        bibtex_string = '''@article{article1
            author: "author1"
            title: "title1"
            journal: "journal1"
            year: "2001"
            volume: "1"
            number: "1"
            pages: "1"
        }
        '''

        return_value = self.bibtex_service._parse_article(bibtex_string).items()
        self.assertIn(('author', 'author1'), return_value)
        self.assertIn(('title', 'title1'), return_value)
        self.assertIn(('journal', 'journal1'), return_value)
        self.assertIn(('year', '2001'), return_value)
        self.assertIn(('volume', '1'), return_value)
        self.assertIn(('number', '1'), return_value)
        self.assertIn(('pages', '1'), return_value)

    def test_parse_misc_parses_the_citation_field_correctly(self):
        bibtex_string = '''@misc{misc1
            author: "author1"
            title: "title1"
            howpublished: "somehow"
            year: "2001"
            note: "note1"
        }
        '''

        return_value = self.bibtex_service._parse_misc(bibtex_string).items()
        self.assertIn(('author', 'author1'), return_value)
        self.assertIn(('title', 'title1'), return_value)
        self.assertIn(('howpublished', 'somehow'), return_value)
        self.assertIn(('year', '2001'), return_value)
        self.assertIn(('note', 'note1'), return_value)

    def test_parse_phdthesis_parses_the_citation_field_correctly(self):
        bibtex_string = '''@phdthesis{phdthesis1
            author: "author1"
            title: "title1"
            school: "school1"
            address: "address1"
            year: "2001"
            month: "January"
        }
        '''

        return_value = self.bibtex_service._parse_phdthesis(bibtex_string).items()
        self.assertIn(('author', 'author1'), return_value)
        self.assertIn(('title', 'title1'), return_value)
        self.assertIn(('school', 'school1'), return_value)
        self.assertIn(('address', 'address1'), return_value)
        self.assertIn(('year', '2001'), return_value)
        self.assertIn(('month', 'January'), return_value)

    def test_parse_inproceedings_parses_the_citation_field_correctly(self):
        bibtex_string = '''@inproceedings{inproceedings1
            author: "author1"
            title: "title1"
            booktitle: "book title 1"
            series: "series1"
            publisher: "publisher1"
            address: "address1"
            year: "2001"
            pages: "1"
        }
        '''

        return_value = self.bibtex_service._parse_inproceedings(bibtex_string).items()
        self.assertIn(('author', 'author1'), return_value)
        self.assertIn(('title', 'title1'), return_value)
        self.assertIn(('booktitle', 'book title 1'), return_value)
        self.assertIn(('series', 'series1'), return_value)
        self.assertIn(('publisher', 'publisher1'), return_value)
        self.assertIn(('address', 'address1'), return_value)
        self.assertIn(('year', '2001'), return_value)
        self.assertIn(('pages', '1'), return_value)

    def test_upload_bibtex_calls_right_method_of_citation_service_when_citation_type_is_book(self):
        bibtex_string = '''@book{book1
            author: "author1"
            title: "title1"
            publisher: "publisher1"
            address: "address1"
            year: "2001"
        }
        '''
        self.bibtex_service.upload_bibtex(bibtex_string)
        self.citation_service.create_book_citation.assert_called()

    def test_upload_bibtex_calls_right_method_of_citation_service_when_citation_type_is_article(self):
        bibtex_string = '''@article{article1
            author: "author1"
            title: "title1"
            journal: "journal1"
            year: "2001"
            volume: "1"
            number: "1"
            pages: "1"
        }
        '''
        self.bibtex_service.upload_bibtex(bibtex_string)
        self.citation_service.create_article_citation.assert_called()

    def test_upload_bibtex_calls_right_of_method_citation_service_when_citation_type_is_misc(self):
        bibtex_string = '''@misc{misc1
            author: "author1"
            title: "title1"
            howpublished: "somehow"
            year: "2001"
            note: "note1"
        }
        '''
        self.bibtex_service.upload_bibtex(bibtex_string)
        self.citation_service.create_misc_citation.assert_called()

    def test_upload_bibtex_calls_right_method_of_citation_service_when_citation_type_is_phdthesis(self):
        bibtex_string = '''@phdthesis{phdthesis1
            author: "author1"
            title: "title1"
            school: "school1"
            address: "address1"
            year: "2001"
            month: "January"
        }
        '''
        self.bibtex_service.upload_bibtex(bibtex_string)
        self.citation_service.create_phdthesis_citation.assert_called()


    def test_upload_bibtex_calls_right_method_of_citation_service_when_citation_type_is_inproceedings(self):
        bibtex_string = '''@inproceedings{inproceedings1
            author: "author1"
            title: "title1"
            booktitle: "book title 1"
            series: "series1"
            publisher: "publisher1"
            address: "address1"
            year: "2001"
            pages: "1"
        }
        '''
        self.bibtex_service.upload_bibtex(bibtex_string)
        self.citation_service.create_inproceedings_citation.assert_called()
