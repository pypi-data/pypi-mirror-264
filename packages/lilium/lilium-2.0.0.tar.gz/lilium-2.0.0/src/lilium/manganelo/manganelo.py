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
        self.current_page = 0
     
    def GetPage(self, page_num:int)->dict[ManganeloManga]:
        dict_manga = self.manga_list.get(page_num) 
        if dict_manga is not None:
            return dict_manga
              
        resp = httpx.get(f"{self.link}?page={page_num}")
        if resp.status_code != 200:
            raise Exception(f"Failed to load Manga List, status code {resp.status_code} on page {page_num}")
        
        html = Soup(resp.content.decode(),"html.parser")
        results = html.select(".panel-search-story .search-story-item .item-right h3 a")
        
        if len(results) == 0:
            return {}
        
        dict_manga = {}
        for element in results:
            m = ManganeloManga(element.get("title"), element.get("href"))
            dict_manga[m.title] = m
        self.manga_list[page_num] = dict_manga
        
        return dict_manga
    
    def GetNextPage(self):
        self.current_page += 1
        return self.GetPage(self.current_page)
    
    async def GetPageAsync(self, page_num:int)->dict[ManganeloManga]:
        dict_manga = self.manga_list.get(page_num) 
        if dict_manga is not None:
            return dict_manga
              
        resp = httpx.get(f"{self.link}?page={page_num}")
        if resp.status_code != 200:
            raise Exception(f"Failed to load Manga List, status code {resp.status_code} on page {page_num}")
        
        html = Soup(resp.content.decode(),"html.parser")
        results = html.select(".panel-search-story .search-story-item .item-right h3 a")
        
        if len(results) == 0:
            return {}
        
        dict_manga = {}
        for element in results:
            m = ManganeloManga(element.get("title"), element.get("href"))
            dict_manga[m.title] = m
        self.manga_list[page_num] = dict_manga
        
        return dict_manga
    
    def GetNextPageAsync(self):
        self.current_page += 1
        return self.GetPageAsync(self.current_page) 
    

class Manganelo():

    def BuildMangaSearcher(query:str)->ManganeloSearchIndex:
        return ManganeloSearchIndex(f"{url}{search_url}/{query.replace(" ", "_")}")  