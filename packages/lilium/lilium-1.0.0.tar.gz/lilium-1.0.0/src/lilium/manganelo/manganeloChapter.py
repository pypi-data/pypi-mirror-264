import httpx
import os
from pathvalidate import sanitize_filepath,sanitize_filename
from bs4 import BeautifulSoup as Soup

class ManganeloChapter:

    _headers = {"Referer":"https://chapmanganelo.com/"}

    def __init__(self, title:str, url:str) -> None:
        self.title = title
        self.url = url
    
    def download(self, location:str="."):
        resp = httpx.get(self.url)
        if resp.status_code != 200:
            raise Exception(f"Cannot download chapter '{self.title}' at '{self.url}'")
        pages_url = [page.get("src") for page in Soup(resp.content.decode(),"html.parser").select(".reader-content")]
        for page_url in pages_url:
            resp = httpx.get(page_url, headers=self._headers)
            if resp.status_code != 200:
                raise Exception(f"Error downloading page")
            with open(os.path.join(location, sanitize_filename(os.path.basename(page_url))), "wb") as f:
                f.write(resp.content)