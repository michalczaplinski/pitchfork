from pitchfork.pitchfork import search, Review, MultiReview
import json
import unittest


class TestReview(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.review = search('mogwai', 'come on')

    def test_review(self):
        self.assertIsInstance(self.review, Review)

    def test_review_album(self):
        self.assertEqual(self.review.album(), "Come On Die Young")

    def test_reviev_artist(self):
        self.assertEqual(self.review.artist(), 'Mogwai')

    def test_review_label(self):
        self.assertEqual(self.review.label(), 'Chemikal Underground')

    def test_review_year(self):
        self.assertEqual(self.review.year(), '1999/2014')

    def test_score(self):
        self.assertEqual(self.review.score(), 8.3)

    def test_editorial(self):
        self.assertTrue(self.review.editorial().startswith('Though few of their songs contain actual words'))

    def test_review_url(self):
        self.assertEqual(self.review.url, '/reviews/albums/19466-mogwai-come-on-die-young-deluxe-edition/')

    def test_review_to_json(self):
        input_dict = self.review._json_safe_dict()
        output_dict = json.loads(self.review.to_json())
        for input_key in input_dict.keys():
            self.assertEqual(output_dict[input_key], input_dict[input_key])

if __name__ == '__main__':
    unittest.main()
