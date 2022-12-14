import unittest
from unittest.mock import Mock
from entities import Citation
from services.citation_service import CitationService
from services.citation_service import WrongAttributeTypeError


class TestCitationService(unittest.TestCase):
    def setUp(self):
        self.citation_repository_mock = Mock()
        self.citation_service = CitationService(self.citation_repository_mock)
        self.book = Citation(
            citation_name="testi",
            author="testaaja",
            title="testi kirja",
            publisher="testaaja",
            address="testi osoite",
            year="2022"
        )
        self.article = Citation(
            citation_name="testi",
            type="article",
            author="testaaja",
            title="testi kirja",
            journal="testi",
            year="2022",
            volume="1",
            number="2",
            pages="1--10"
        )
        self.inproceedings = Citation(
            citation_name="testi",
            type="inproceedings",
            author="testaaja",
            title="testi kirja",
            booktitle="testi otsikko",
            series="testi sarja",
            year="2022",
            pages="1--10",
            publisher="testaaja",
            address="testi osoite"
        )
        self.misc = Citation(
            citation_name="testi",
            type="misc",
            title="testi kirja",
            author="testaaja",
            howpublished=r"\url{https://www.test.com}",
            year="2022",
            note="Lorem ipsum"
        )
        self.phdthesis = Citation(
            citation_name="testi",
            type="phdthesis",
            author="testaaja",
            title="testi kirja",
            school="testi koulu",
            address="testi osoite",
            year="2022",
            month="joulukuu"
        )

    def test_can_add_book_citation(self):
        self.citation_service.create_book_citation(self.book)
        self.citation_repository_mock.insert_book_citation.assert_called_with(
            self.book)

    def test_can_add_article_citation(self):
        self.citation_service.create_article_citation(self.article)
        self.citation_repository_mock.insert_article_citation.assert_called_with(
            self.article)

    def test_can_add_inproceedings_citation(self):
        self.citation_service.create_inproceedings_citation(self.inproceedings)
        self.citation_repository_mock.insert_inproceedings_citation.assert_called_with(
            self.inproceedings)

    def test_can_add_misc_citation(self):
        self.citation_service.create_misc_citation(self.misc)
        self.citation_repository_mock.insert_misc_citation.assert_called_with(
            self.misc)

    def test_can_add_phdthesis_citation(self):
        self.citation_service.create_phdthesis_citation(self.phdthesis)
        self.citation_repository_mock.insert_phdthesis_citation.assert_called_with(
            self.phdthesis)

    def test_can_add_multiple_citations_of_same_type(self):
        self.citation_service.create_book_citation(self.book)
        self.citation_service.create_book_citation(self.book)
        self.citation_service.create_book_citation(self.book)

        self.assertEqual(
            self.citation_repository_mock.insert_book_citation.call_count, 3)

    def test_can_add_multiple_citations_of_different_type(self):
        self.citation_service.create_book_citation(self.book)
        self.citation_service.create_article_citation(self.article)
        self.citation_service.create_inproceedings_citation(self.inproceedings)
        self.citation_service.create_misc_citation(self.misc)
        self.citation_service.create_phdthesis_citation(self.phdthesis)

        self.assertEqual(
            self.citation_repository_mock.insert_book_citation.call_count, 1)
        self.assertEqual(
            self.citation_repository_mock.insert_article_citation.call_count, 1)
        self.assertEqual(
            self.citation_repository_mock.insert_inproceedings_citation.call_count, 1)
        self.assertEqual(
            self.citation_repository_mock.insert_misc_citation.call_count, 1)
        self.assertEqual(
            self.citation_repository_mock.insert_phdthesis_citation.call_count, 1)

    def test_can_find_specific_citation(self):
        self.citation_service.get_citation(3)

        self.citation_repository_mock.get_citation.assert_called_with(3)

    def test_can_list_all_citations(self):
        book_values = list(self.book.get_data().values())

        def returns():
            return [book_values, book_values, book_values]

        self.citation_repository_mock.get_citations.side_effect = returns
        citations = self.citation_service.get_citations()
        print(citations)
        self.assertEqual(len(citations), 3)
        self.assertEqual(citations, [book_values, book_values, book_values])

    def test_citation_validation_does_not_raise_a_typeerror_when_correct_attribute_type_is_used(self):
        try:
            self.citation_service.validate_citation(self.book)
        except WrongAttributeTypeError as exc:
            assert False, f"validate_citation raised an exception {exc}"

    def test_validate_citation_raises_typeerror_when_wrong_attribute_type_is_used(self):
        self.book.year = "test"
        self.assertRaises(WrongAttributeTypeError,
                          self.citation_service.validate_citation, self.book)

    def test_the_raised_typerror_includes_info_about_which_attribute_fails(self):
        self.book.year = "test"
        try:
            self.citation_service.validate_citation(self.book)
        except WrongAttributeTypeError as error:
            self.assertIn("year", str(error))
        self.article.year = "test"
        self.article.number = "two"
        try:
            self.citation_service.validate_citation(self.article)
        except WrongAttributeTypeError as error:
            self.assertIn("year", str(error))
            self.assertIn("number", str(error))

    def test_create_book_citation_raises_typeerror_when_wrong_attribute_type_is_used(self):
        setattr(self.book, "year", "test")
        self.assertRaises(WrongAttributeTypeError,
                          self.citation_service.create_book_citation, self.book)

    def test_create_article_citation_raises_typeerror_when_wrong_attribute_type_is_used(self):
        self.article.year = "test"
        self.assertRaises(WrongAttributeTypeError,
                          self.citation_service.create_article_citation, self.article)

    def test_create_inproceedings_citation_raises_typeerror_when_wrong_attribute_type_is_used(self):
        self.inproceedings.year = "test"
        self.assertRaises(WrongAttributeTypeError,
                          self.citation_service.create_inproceedings_citation, self.inproceedings)

    def test_create_misc_citation_raises_typeerror_when_wrong_attribute_type_is_used(self):
        self.misc.year = "test"
        self.assertRaises(WrongAttributeTypeError,
                          self.citation_service.create_misc_citation, self.misc)

    def test_create_phdthesis_citation_raises_typeerror_when_wrong_attribute_type_is_used(self):
        self.phdthesis.year = "test"
        self.assertRaises(WrongAttributeTypeError,
                          self.citation_service.create_phdthesis_citation, self.phdthesis)
