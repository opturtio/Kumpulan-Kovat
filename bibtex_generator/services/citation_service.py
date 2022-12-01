from repositories.citation_repository import (
    citation_repository as default_citation_repository
)

class CitationService:
    def __init__(self, citation_repository = default_citation_repository):
        self._citation_repository = citation_repository


    def create_citation(self, citation_name, title, published, author):
        self._citation_repository.insert_citation(citation_name, title, published, author)





citation_service = CitationService()
