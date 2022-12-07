class WrongAttributeTypeError(Exception):
    pass

class CitationService:
    def __init__(self, citation_repository):
        self._citation_repository = citation_repository
        self.attribute_types = {
            "citation_name" : str,
            "type" : str,
            "author" : str,
            "title" : str,
            "booktitle" : str,
            "series" : str,
            "publisher" : str,
            "school" : str,
            "address" : str,
            "journal" : str,
            "howpublished" : str,
            "year" : int,
            "month" : str,
            "volume" : str,
            "number" : int,
            "pages" : str,
            "note" : str
        }

    def create_book_citation(self, citation_object):
        self.validate_citation(citation_object)
        self._citation_repository.insert_book_citation(citation_object)

    def create_article_citation(self, citation_object):
        self.validate_citation(citation_object)
        self._citation_repository.insert_article_citation(citation_object)

    def create_misc_citation(self, citation_object):
        self.validate_citation(citation_object)
        self._citation_repository.insert_misc_citation(citation_object)

    def create_phdthesis_citation(self, citation_object):
        self.validate_citation(citation_object)
        self._citation_repository.insert_phdthesis_citation(citation_object)

    def create_inproceedings_citation(self, citation_object):
        self.validate_citation(citation_object)
        self._citation_repository.insert_inproceedings_citation(citation_object)

    def validate_citation(self, citation):
        errors = []
        for key, value in citation.get_data().items():
            try:
                setattr(citation, key, self.attribute_types[key](value))
            except ValueError:
                errors.append(key)
        if errors:
            raise WrongAttributeTypeError(*errors)

    def get_citation(self, id):
        return self._citation_repository.get_citation(id)

    def get_citations(self):
        return self._citation_repository.get_citations()

    def citation_search(self, query):
        return self._citation_repository.citation_search(query)
