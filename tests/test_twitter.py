import mock
import os
from mongomock import MongoClient
from unittest import TestCase
from helga_markovify.twitter import get_all_tweets


class TestTwitter(TestCase):
    def setUp(self):
        super(TestTwitter, self).setUp()
        self.tweet1 = mock.MagicMock()
        self.tweet1.text = 'hey1'
        self.tweet1.id = 1
        self.tweet2 = mock.MagicMock()
        self.tweet2.text = 'hey2'
        self.tweet2.id = 2
        self.tweet3 = mock.MagicMock()
        self.tweet3.text = 'hey3'
        self.tweet3.id = 3

    def test_get_all_tweets(self):
        api = mock.MagicMock()
        def user_timeline(screen_name, since_id=0, count=200, max_id=-1):
            if max_id != -1:
                return []
            return [self.tweet1, self.tweet2]
        api.user_timeline = user_timeline
        tweets, since_id = get_all_tweets('sname', api, 0)
        self.assertEqual(2, len(tweets))
        self.assertEqual(1, since_id)

    def test_get_all_tweets_complex(self):
        api = mock.MagicMock()
        def user_timeline(screen_name, since_id=0, count=200, max_id=-1):
            if max_id == 2:
                return [self.tweet1]
            elif max_id == 0:
                return []
            return [self.tweet2, self.tweet3]
        api.user_timeline = user_timeline
        tweets, since_id = get_all_tweets('sname', api, 0)
        self.assertEqual(3, len(tweets))
        self.assertEqual(2, since_id)


if __name__ == '__main__':
    unittest.main()
