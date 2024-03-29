import unittest
import shutil
from lilium.manganelo import *

class Test(unittest.TestCase):

    temp_folder = "temp"
    skip_intensive = True

    def test_get_exactly_one_manga(self):
        manga_title = "Uratarou"
        si:ManganeloSearchIndex = Manganelo.BuildMangaSearcher(manga_title)
        
        self.assertEqual(len(si.manga_list),0) #check dict is empty

        manga_l = si.GetPage(1)
        
        self.assertEqual(len(manga_l), 1)
        self.assertEqual(len(si.manga_list), 1)
        self.assertEqual(len(si.manga_list.get(1)), 1)
        self.assertEqual(manga_l[list(manga_l.keys())[0]].title, manga_title)
    
    def test_get_page_with_0_result(self):
        manga_title = "Boku No Hero Academia "
        si = Manganelo.BuildMangaSearcher(manga_title)
        manga_l = si.GetPage(999)
        self.assertEqual(len(manga_l), 0)
        self.assertEqual(len(si.manga_list), 0)
    
    @unittest.skipIf(skip_intensive, "Time consuming test")
    def test_download_one_chapter(self):
        manga = ManganeloManga("Boku No Hero Academia", "https://chapmanganelo.com/manga-jq89184")
        manga.download_chapter(1, self.temp_folder)
        
    @unittest.skipIf(skip_intensive, "Time consuming test")
    def test_download_all_chapters(self):
        manga = ManganeloManga("Boku No Hero Academia", "https://chapmanganelo.com/manga-jq89184")
        manga.download_all_chapters(self.temp_folder)
    
    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(cls.temp_folder, ignore_errors=True)
        return super().tearDownClass()

if __name__ == "__main__":
    unittest.main()