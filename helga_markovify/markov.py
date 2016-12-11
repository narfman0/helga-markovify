""" Module to ingest to corpus and generate markov chains from corpus """
import markovify
import string
from helga.db import db


def punctuate(current_text, new_text, add_punctuation):
    """ Add punctuation as needed """
    if add_punctuation and current_text and not current_text[-1] in string.punctuation:
        current_text += '. '
    spacer = ' ' if not current_text or (not current_text[-1].isspace() and not new_text[0].isspace()) else ''
    return current_text + spacer + new_text


def ingest(topic, text, **kwargs):
    """ Ingest the given text for the topic """
    if not text:
        raise ValueError('No text given to ingest for topic: ' + topic)
    data = {'topic': topic, 'text': text.strip()}
    data.update(kwargs)
    db.markovify.insert(data)


def generate(topic, add_punctuation, character_count=None):
    """ Generate the text for a given topic """
    corpus_cursor = db.markovify.find({'topic': topic})
    if(corpus_cursor):
        corpus = ''
        for text in corpus_cursor:
            corpus = punctuate(corpus, text['text'], add_punctuation)
        text_model = markovify.Text(corpus)
        sentence = text_model.make_short_sentence(character_count) \
            if character_count else text_model.make_sentence()
        if not sentence:
            raise Exception('There is not enough in the corpus to generate a sentence.')
        return sentence
    raise Exception('No text found for topic: ' + topic)
