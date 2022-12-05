import unittest
from entities.bibtex_formatter import create_bibtex_citation, create_bibtex_citation_html
from entities.citation import Citation

class TestBibtexFromatter(unittest.TestCase):
    def setUp(self):
        self.citation_object = Citation(
            citation_name = "Test22",
            type = "book",
            author = "TestAuthor",
            title = "TestBook",
            year = 2022
        )
        self.correct_string = ("@book{Test22\n"
            "\tauthor: \"TestAuthor\"\n"
            "\ttitle: \"TestBook\"\n"
            "\tyear: \"2022\"\n"
            "}"
        )
        self.correct_string_html = ("@book{Test22<br>"
        "&emsp;&emsp;author: &quot;TestAuthor&quot;<br>"
        "&emsp;&emsp;title: &quot;TestBook&quot;<br>"
        "&emsp;&emsp;year: &quot;2022&quot;<br>"
        "}"
        )
    
    def test_create_bibtex_citation_works(self):
        bibtex_string = create_bibtex_citation(self.citation_object)
        self.assertEqual(bibtex_string, self.correct_string)
    
    def test_create_bibtex_citation_html_works(self):
        bibtex_string_html = create_bibtex_citation_html(self.citation_object)
        self.assertEqual(bibtex_string_html, self.correct_string_html)