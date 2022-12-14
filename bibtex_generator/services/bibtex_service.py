import re
from entities import create_bibtex_citation, Citation
from services import CitationService

class BibtexService:
    def __init__(self, service: CitationService, bibtex_formatter = create_bibtex_citation):
        self._service = service
        self.bibtex_formatter = bibtex_formatter

    def _get_citations(self, ids: list) -> list:
        citations = []
        for citation_id in ids:
            citation = self._service.get_citation(citation_id)
            citations.append(self._convert_to_citation(citation))
        return citations

    def _convert_to_citation(self, data):
        citation = Citation(**{k: v for k, v in dict(data).items() if v is not None})
        return citation

    def _convert_citations_to_bibtex(self, citations):
        bibtex = ""
        for citation in citations:
            bibtex += self.bibtex_formatter(citation)+"\n\n"
        return bibtex

    def generate_bibtex_file(self, citation_ids: list):
        if isinstance(citation_ids[0], int):
            citations = self._get_citations(citation_ids)
        else:
            citations = citation_ids
        bibtex = self._convert_citations_to_bibtex(citations)
        with open("references.bib", "w+", encoding="utf8") as file:
            file.write(bibtex)

    def upload_bibtex(self, bibtex_string):
        type = self._parse_type(bibtex_string)
        citation_name = self._parse_name(bibtex_string)

        if type == "book":
            field_values = self._parse_book(bibtex_string)
            citation_object = Citation(
                type=type,
                citation_name=citation_name,
                author=field_values["author"],
                title=field_values["title"],
                publisher=field_values["publisher"],
                address=field_values["address"],
                year=field_values["year"]
            )
            self._service.create_book_citation(citation_object)

        elif type == "article":
            field_values = self._parse_article(bibtex_string)
            citation_object = Citation(
                type=type,
                citation_name=citation_name,
                author=field_values["author"],
                title=field_values["title"],
                journal=field_values["journal"],
                year=field_values["year"],
                volume=field_values["volume"],
                number=field_values["number"],
                pages=field_values["pages"]
            )
            self._service.create_article_citation(citation_object)

        elif type == "misc":
            field_values = self._parse_misc(bibtex_string)
            citation_object = Citation(
                type=type,
                citation_name=citation_name,
                title=field_values["title"],
                author=field_values["author"],
                howpublished=field_values["howpublished"],
                year=field_values["year"],
                note=field_values["note"]
            )
            self._service.create_misc_citation(citation_object)

        elif type == "phdthesis":
            field_values = self._parse_phdthesis(bibtex_string)
            citation_object = Citation(
                type=type,
                citation_name=citation_name,
                author=field_values["author"],
                title=field_values["title"],
                school=field_values["school"],
                address=field_values["address"],
                year=field_values["year"],
                month=field_values["month"]
            )
            self._service.create_phdthesis_citation(citation_object)

        elif type == "inproceedings":
            field_values = self._parse_inproceedings(bibtex_string)
            citation_object = Citation(
                type=type,
                citation_name=citation_name,
                author=field_values["author"],
                title=field_values["title"],
                booktitle=field_values["booktitle"],
                series=field_values["series"],
                year=field_values["year"],
                pages=field_values["pages"],
                publisher=field_values["publisher"],
                address=field_values["address"]
            )
            self._service.create_inproceedings_citation(citation_object)

    def _parse_type(self, bibtex_string):
        return re.search(r'^@[a-z]+{', bibtex_string).group()[1:-1]

    def _parse_name(self, bibtex_string):
        return re.search(r'{\w+', bibtex_string).group()[1:]

    def _parse_book(self, bibtex_string):
        field_values = {}
        field_values["author"] = re.search(r'author:\s".*"', bibtex_string).group()[len('author: "'):-1]
        field_values["title"] = re.search(r'title:\s".*"', bibtex_string).group()[len('title: "'):-1]
        field_values["publisher"] = re.search(r'publisher:\s".*"', bibtex_string).group()[len('publisher: "'):-1]
        field_values["address"] = re.search(r'address:\s".*"', bibtex_string).group()[len('address: "'):-1]
        field_values["year"] = re.search(r'year:\s".*"', bibtex_string).group()[len('year: "'):-1]
        return field_values

    def _parse_article(self, bibtex_string):
        field_values = {}
        field_values["author"] = re.search(r'author:\s".*"', bibtex_string).group()[len('author: "'):-1]
        field_values["title"] = re.search(r'title:\s".*"', bibtex_string).group()[len('title: "'):-1]
        field_values["journal"] = re.search(r'journal:\s".*"', bibtex_string).group()[len('journal: "'):-1]
        field_values["year"] = re.search(r'year:\s".*"', bibtex_string).group()[len('year: "'):-1]
        field_values["volume"] = re.search(r'volume:\s".*"', bibtex_string).group()[len('volume: "'):-1]
        field_values["number"] = re.search(r'number:\s".*"', bibtex_string).group()[len('number: "'):-1]
        field_values["pages"] = re.search(r'pages:\s".*"', bibtex_string).group()[len('pages: "'):-1]
        return field_values

    def _parse_misc(self, bibtex_string):
        field_values = {}
        field_values["author"] = re.search(r'author:\s".*"', bibtex_string).group()[len('author: "'):-1]
        field_values["title"] = re.search(r'title:\s".*"', bibtex_string).group()[len('title: "'):-1]
        field_values["howpublished"] = re.search(r'howpublished:\s".*"', bibtex_string).group()[len('howpublished: "'):-1]
        field_values["year"] = re.search(r'year:\s".*"', bibtex_string).group()[len('year: "'):-1]
        field_values["note"] = re.search(r'note:\s".*"', bibtex_string).group()[len('note: "'):-1]
        return field_values

    def _parse_phdthesis(self, bibtex_string):
        field_values = {}
        field_values["author"] = re.search(r'author:\s".*"', bibtex_string).group()[len('author: "'):-1]
        field_values["title"] = re.search(r'title:\s".*"', bibtex_string).group()[len('title: "'):-1]
        field_values["school"] = re.search(r'school:\s".*"', bibtex_string).group()[len('school: "'):-1]
        field_values["address"] = re.search(r'address:\s".*"', bibtex_string).group()[len('address: "'):-1]
        field_values["year"] = re.search(r'year:\s".*"', bibtex_string).group()[len('year: "'):-1]
        field_values["month"] = re.search(r'month:\s".*"', bibtex_string).group()[len('month: "'):-1]
        return field_values

    def _parse_inproceedings(self, bibtex_string):
        field_values = {}
        field_values["author"] = re.search(r'author:\s".*"', bibtex_string).group()[len('author: "'):-1]
        field_values["title"] = re.search(r'title:\s".*"', bibtex_string).group()[len('title: "'):-1]
        field_values["booktitle"] = re.search(r'booktitle:\s".*"', bibtex_string).group()[len('booktitle: "'):-1]
        field_values["series"] = re.search(r'series:\s".*"', bibtex_string).group()[len('series: "'):-1]
        field_values["publisher"] = re.search(r'publisher:\s".*"', bibtex_string).group()[len('publisher: "'):-1]
        field_values["address"] = re.search(r'address:\s".*"', bibtex_string).group()[len('address: "'):-1]        
        field_values["year"] = re.search(r'year:\s".*"', bibtex_string).group()[len('year: "'):-1]        
        field_values["pages"] = re.search(r'pages:\s".*"', bibtex_string).group()[len('pages: "'):-1]
        return field_values
