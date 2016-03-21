import mock
import mongomock
from unittest import TestCase


class TestMarkov(TestCase):
    def setUp(self):
        super(TestMarkov, self).setUp()
        self.db_patch = mock.patch(
            'pymongo.MongoClient',
            new_callable=lambda: mongomock.MongoClient
        )
        self.db_patch.start()
        self.addCleanup(self.db_patch.stop)

    def test_ingest_generate(self):
        from helga_markovify.markov import ingest, generate
        topic = 'hitler'
        ingest(topic, "Mein Kampf is the best Kampf.")
        ingest(topic, "Don't be stupid, be a smarty. Come and join the nazi party.")
        ingest(topic, "Make America hate again.")
        result = generate(topic)
        print 'Generated: ' + result
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
