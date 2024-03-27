from bs4 import BeautifulSoup
import requests


class Scraper:
    def __init__(self, webpage) -> None:
        self.webpage = webpage
        page = requests.get(self.webpage)
        self.soup = BeautifulSoup(page.content, "html.parser")

    def searchForLinkWithText(self, text) -> str:
        for link in self.soup.find_all("a"):
            if link.text == text:
                return link.get("href")