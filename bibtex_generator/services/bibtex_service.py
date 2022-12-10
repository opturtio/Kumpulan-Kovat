from bibtex_generator.entities import create_bibtex_citation, Citation
from bibtex_generator.services import CitationService

class BibtexService:
    def __init__(self, service: CitationService):
        self._service = service

    def _get_citations(self, ids: list) -> list:
        citations = []
        for id in ids:
            citations.append(self._convert_to_citation(self._service.get_citation(id)))
        return citations

    def _convert_to_citation(self, data):
        citation = Citation(**{k: v for k, v in dict(data).items() if v is not None})
        return citation

    def _convert_citations_to_bibtex(self, citations):
        bibtex = ""
        for citation in citations:
            bibtex += create_bibtex_citation(citation)+"\n"
        return bibtex

    def generate_bibtex_file(self, citation_ids: list):
        citations = self._get_citations(citation_ids)
        bibtex = self._convert_citations_to_bibtex(citations)
        file = open("generated_bibtex.bib", "w+")
        file.write(bibtex)
        file.close()
