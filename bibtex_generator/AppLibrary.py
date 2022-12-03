import requests

class AppLibrary:
    def __init__(self):
        self._base_url = "http://localhost:5000"

    def create_citation(self, citation_name, title, year, author):
        data = {
            "citation_name": citation_name,
            "title": title,
            "year": year,
            "author": author
        }

        requests.post(f"{self._base_url}/new_citation", data=data)
