import html
from pylatexenc.latexencode import unicode_to_latex

def create_bibtex_citation(citation):
    bibtex_string = f"@{citation.type}{{{citation.citation_name}\n"
    for key in citation.keys():
        if key != "id" and key != "citation_name" and key != "type" and citation[key]:
            bibtex_string += f"\t{key}: \"{unicode_to_latex(citation[key])}\"\n"
    bibtex_string += "}"

    return bibtex_string

def create_bibtex_citation_html(citation):
    bibtex_string = create_bibtex_citation(citation)
    bibtex_string = html.escape(bibtex_string)
    bibtex_string = bibtex_string.replace("\n", "<br>").replace("\t", "&emsp;&emsp;")
    return bibtex_string
