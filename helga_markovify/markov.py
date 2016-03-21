""" Module to ingest to corpus and generate markov chains from corpus """
import markovify
import string
from helga.db import db


def ingest(topic, text, add_punctuation=True):
    """ Ingest the given text for the topic """
    if not text:
        return 'No text given to ingest for topic: ' + topic
    query = db.markovify.find({'topic':topic})
    topic_text = query.next() if query.count() else ''
    if add_punctuation and topic_text:
        if not topic_text.strip()[-1] in string.punctuation:
            topic_text += '. '
    topic_text += text
    db.markovify.update({'topic':topic}, {'text':topic_text}, upsert=True)


def generate(topic, character_count=99999):
    """ Generate the text for a given topic """
    query = db.markovify.find({'topic':topic})
    if(query.count()):
        text_model = markovify.Text(query.next())
        return text_model.make_sentence(character_count)
    return 'No text found for topic: ' + topic
