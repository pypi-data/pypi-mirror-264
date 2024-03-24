import httpx
from .manganeloManga import ManganeloManga
from bs4 import BeautifulSoup as Soup

url = "https://m.manganelo.com"
search_url = "/search/story/"
headers = {"Referer":"https://chapmanganelo.com/"}

class ManganeloSearchIndex():
     
    def __init__(self, link:str) -> None:
        self.manga_list = {}
        self.link = link
     
    def GetPage(self, page_num:int)->list[ManganeloManga]:
        manga_l = self.manga_list.get(page_num) 
        if manga_l is not None:
            return manga_l
              
        resp = httpx.get(f"{self.link}?page={page_num}")
        if resp.status_code != 200:
            raise Exception(f"Failed to load Manga List, status code {resp.status_code} on page {page_num}")
        
        html = Soup(resp.content.decode(),"html.parser")
        results = html.select(".panel-search-story .search-story-item .item-right h3 a")
        
        if len(results) == 0:
            return []
        
        manga_list = []
        for element in results:
            manga_list.append(ManganeloManga(element.get("title"), element.get("href")))
        self.manga_list[page_num] = manga_list
        
        return manga_list

class Manganelo():

    def build_manga_searcher(query:str)->ManganeloSearchIndex:
        return ManganeloSearchIndex(f"{url}{search_url}/{query.replace(" ", "_")}")  