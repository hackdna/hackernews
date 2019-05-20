import time
import unittest

import hn


class TestGetStoryRank(unittest.TestCase):

    def setUp(self):
        self.current_time = int(time.time())
        self.story = {'score': 100, 'time': self.current_time - 5400}

    def test_get_rank_with_no_url(self):
        rank = hn.get_rank(self.story, self.current_time)
        self.assertEqual(rank, 1.656706847121287)

    def test_get_rank_with_blank_url(self):
        self.story['url'] = ''
        rank = hn.get_rank(self.story, self.current_time)
        self.assertEqual(rank, 1.656706847121287)

    def test_get_rank_with_url(self):
        self.story['url'] = 'http://example.com'
        rank = hn.get_rank(self.story, self.current_time)
        self.assertEqual(rank, 4.141767117803218)


if __name__ == '__main__':
    unittest.main()
