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
