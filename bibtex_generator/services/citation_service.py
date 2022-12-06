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

    def create_citation(self, citation_object):
        errors = self.validate_citation(citation_object)
        if errors:
            raise WrongAttributeTypeError(*errors)
        self._citation_repository.insert_citation(citation_object)

    def validate_citation(self, citation):
        errors = []
        for key, value in citation.get_data().items():
            try:
                setattr(citation, key, self.attribute_types[key](value))
            except ValueError:
                errors.append(key)
        return errors

    def get_citation(self, id):
        return self._citation_repository.get_citation(id)

    def get_citations(self):
        return self._citation_repository.get_citations()

    def citation_search(self, query):
        return self._citation_repository.citation_search(query)

    def remove_citation(self, id):
        return self._citation_repository.remove_citation(id)

