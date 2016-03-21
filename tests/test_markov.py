import mock
import os
from mongomock import MongoClient
from unittest import TestCase


class TestMarkov(TestCase):
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
        with open(os.path.join(os.path.dirname(__file__), '../helga_markovify/zen.txt')) as f:
            ingest(topic, f.read())
        result = generate(topic)
        print 'Generated: ' + result
        self.assertTrue(result)

    def test_ingest_text(self):
        from helga_markovify.markov import ingest, generate
        topic = 'zen'
        ingest(topic, "Mein Kampf is the best Kampf.")
        ingest(topic, "Don't be stupid, be a smarty. Come and join the nazi party.")
        ingest(topic, "Make America hate again.")
        ingest(topic, "Kampf America is hate nazi smarty. Hate party again filler sentence. America is the best at being terrible.")
        result = generate(topic)
        print 'Generated: ' + result
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
