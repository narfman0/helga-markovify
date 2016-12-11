import mock
import os
import unittest
from mongomock import MongoClient


class TestMarkov(unittest.TestCase):
    def setUp(self):
        super(TestMarkov, self).setUp()
        self.db_patch = mock.patch(
            'pymongo.MongoClient',
            new_callable=lambda: MongoClient
        )
        self.db_patch.start()
        self.addCleanup(self.db_patch.stop)

    def test_ingest_zen(self):
        from helga_markovify.markov import ingest, generate
        topic = 'zen'
        with open(os.path.join(os.path.dirname(__file__), 'zen.txt')) as f:
            ingest(topic, f.read())
        result = generate(topic, True)
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
