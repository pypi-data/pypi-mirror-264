import httpx
import os
from pathvalidate import sanitize_filepath,sanitize_filename
from .manganeloChapter import *
from bs4 import BeautifulSoup as Soup

class ManganeloManga():
    def __init__(self, title:str, url:str, lazy=True) -> None:
        self.title = title
        self.url = url
        self._chapters:list[ManganeloChapter] = None
    
    def get_chapters(self)->list[ManganeloChapter]:
        if self._chapters is None:
            self._initialize()
        return self._chapters

    def _download_chapter(self, chapter:int, location:str="."):
        path=os.path.join(location, 
                          sanitize_filepath(self.title),
                          sanitize_filename(self._chapters[chapter].title))
        os.makedirs(path, exist_ok=True)
        self._chapters[chapter].download(path)

    def download_chapter(self, chapter:int, location:str="."):
        if self._chapters is None:
            self._initialize()
        self._download_chapter(chapter,location)

    def download_all_chapters(self, location:str="."):
        if self._chapters is None:
            self._initialize()
        for chapter_i in range(len(self._chapters)):
            self._download_chapter(chapter_i,location)

    def _initialize(self):
        resp = httpx.get(self.url)
        if resp.status_code != 200:
            raise Exception(f"Cannot read manga data at {self.url}")
        html = Soup(resp.content.decode(),"html.parser")
        chapters = html.select(".chapter-name")
        self._chapters = []
        for chapter in chapters:
            self._chapters.append(ManganeloChapter(chapter.contents[0], chapter.get("href")))

    def __str__(self) -> str:
        return f"title: {self.title}, url: {self.url}"
    def __repr__(self) -> str:
        return f"{self.title} {self.url}"