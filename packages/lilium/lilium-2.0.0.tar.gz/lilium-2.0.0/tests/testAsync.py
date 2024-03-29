import unittest
import shutil
from lilium.manganelo import *
#TODO
class TestAsync(unittest.IsolatedAsyncioTestCase):

    temp_folder = "temp"
    skip_intensive = True

    async def test_get_exactly_one_manga_async(self):
        manga_title = "Uratarou"
        si:ManganeloSearchIndex = Manganelo.BuildMangaSearcher(manga_title)
        
        self.assertEqual(len(si.manga_list),0) #check dict is empty

        manga_l = await si.GetPageAsync(1)
        
        self.assertEqual(len(manga_l), 1)
        self.assertEqual(len(si.manga_list), 1)
        self.assertEqual(len(si.manga_list.get(1)), 1)
        self.assertEqual(manga_l[list(manga_l.keys())[0]].title, manga_title)
    
    async def test_get_page_with_0_result_async(self):
        manga_title = "Boku No Hero Academia "
        si:ManganeloSearchIndex = Manganelo.BuildMangaSearcher(manga_title)
        manga_l = await si.GetPageAsync(999)
        self.assertEqual(len(manga_l), 0)
        self.assertEqual(len(si.manga_list), 0)
    
    @unittest.skipIf(skip_intensive, "Time consuming test")
    def test_download_one_chapter_async(self):
        manga = ManganeloManga("Boku No Hero Academia", "https://chapmanganelo.com/manga-jq89184")
        manga.download_chapter(1, self.temp_folder)
        
    @unittest.skipIf(skip_intensive, "Time consuming test")
    def test_download_all_chapters_async(self):
        manga = ManganeloManga("Boku No Hero Academia", "https://chapmanganelo.com/manga-jq89184")
        manga.download_all_chapters(self.temp_folder)
    
    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(cls.temp_folder, ignore_errors=True)
        return super().tearDownClass()

if __name__ == "__main__":
    unittest.main()