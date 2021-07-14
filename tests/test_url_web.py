import url_web

import unittest

class GetWebTests(unittest.TestCase):

    def test_get_categories(self):
        categories_returned = url_web.get_categories()
        categories_expected = ['Le film de la semaine', 'Les autres nouveautés', 'Films au hasard']
        self.assertCountEqual(categories_expected, categories_returned)

    def test_get_videos_first(self):
        videos_returned = url_web.get_videos('Le film de la semaine')
        videos_expected = [{'name': "L'homme de la rue", 'thumb': 'https://horscine.org/wp-content/uploads/Affiche-lhomme-de-la-rue.jpg', 'video': 'https://archive.org/serve/lhomme-de-la-rue/lhomme-de-la-rue-DP.ia.mp4', 'genre': 'Film'}]
        self.assertCountEqual(videos_expected, videos_returned)

    def test_get_videos_second(self):
        videos_returned = url_web.get_videos('Les autres nouveautés')
        videos_expected = [{'name': 'La Parade, ou la vie en pull bleu', 'thumb': 'https://horscine.org/wp-content/uploads/la-parade-ou-la-vie-en-pull-bleu.jpg', 'video': 'https://player.vimeo.com/video/45519017?dnt=1&app_id=122963', 'genre': 'Film'}, {'name': 'De rien', 'thumb': 'https://horscine.org/wp-content/uploads/de-rien.jpg', 'video': 'https://player.vimeo.com/video/367593464?dnt=1&app_id=122963', 'genre': 'Film'}, {'name': 'Artist 110', 'thumb': 'https://horscine.org/wp-content/uploads/ARTIST110.jpg', 'video': 'https://player.vimeo.com/video/202509514?dnt=1&app_id=122963', 'genre': 'Film'}]
        self.assertCountEqual(videos_expected, videos_returned)

    def test_get_videos_third(self):
        videos_returned = url_web.get_videos('Films au hasard')
        videos_expected = [{'name': "The cavalier's dream", 'thumb': 'https://horscine.org/wp-content/uploads/the-cavaliers-dream.jpg', 'video': 'https://archive.org/serve/CavaliersDream/Cavalier%27s_Dream.mp4', 'genre': 'Film'}, {'name': 'Spring', 'thumb': 'https://horscine.org/wp-content/uploads/2020/11/spring.jpg', 'video': 'https://player.vimeo.com/video/77059630?dnt=1&app_id=122963', 'genre': 'Film'}, {'name': 'The balloonatic', 'thumb': 'https://horscine.org/wp-content/uploads/theballoonatic.jpg', 'video': 'https://player.vimeo.com/video/1084537?dnt=1&app_id=122963', 'genre': 'Food'}]
        self.assertCountEqual(videos_expected, videos_returned)

class SearchTests(unittest.TestCase):

    def test_nothing(self):
        self.assertTrue(1==1, "I don't always test my code; but when I do, I do it in PRODUCTION.")

class ConvertTests(unittest.TestCase):

    def test_nothing(self):
        self.assertTrue(1==1, "I don't always test my code; but when I do, I do it in PRODUCTION.")



if __name__ == '__main__':
    unittest.main()

