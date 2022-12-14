import requests


class AppLibrary:
    def __init__(self):
        self._base_url = "http://localhost:5000"

    def create_book(self, citation_name, author, title, publisher, address, year):  # pylint: disable=too-many-arguments
        data = {
            "citation_name": citation_name,
            "author": author,
            "title": title,
            "publisher": publisher,
            "address": address,
            "year": year,
        }

        requests.post(f"{self._base_url}/new_book", data=data)
