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


def ingest(topic, text, add_punctuation=True, **kwargs):
    """ Ingest the given text for the topic """
    if not text:
        raise ValueError('No text given to ingest for topic: ' + topic)
    topic_query = db.markovify.find_one({'topic': topic})
    if topic_query:
        topic_query['text'] = punctuate(topic_query['text'].strip(), text, add_punctuation)
        topic_query.update(kwargs)
        db.markovify.find_one_and_replace({'topic': topic}, topic_query)
    else:
        data = {'topic': topic, 'text': text}
        data.update(kwargs)
        db.markovify.insert(data)


def generate(topic, character_count=None):
    """ Generate the text for a given topic """
    topic_query = db.markovify.find_one({'topic': topic})
    if(topic_query):
        text = topic_query['text']
        text_model = markovify.Text(text)
        sentence = text_model.make_short_sentence(character_count) \
            if character_count else text_model.make_sentence()
        if not sentence:
            raise Exception('There is not enough in the corpus to generate a sentence.')
        return sentence
    raise Exception('No text found for topic: ' + topic)
