""" Plugin entry point for helga """
import requests
from bs4 import BeautifulSoup
from helga import settings
from helga.db import db
from helga.plugins import command, random_ack
from helga_markovify.markov import add_punctuation, ingest, generate
from helga_markovify.twitter import twitter_timeline


_ADD_PUNCTUATION = settings.MARKOVIFY_ADD_PUNCTUATION if hasattr(settings, 'MARKOVIFY_ADD_PUNCTUATION') else True
_DEFAULT_TOPIC = settings.MARKOVIFY_TOPIC_DEFAULT if hasattr(settings, 'MARKOVIFY_TOPIC_DEFAULT') else  'default'
_HELP_TEXT = """Ingest data to produve markov chain text. Helga always listens.
Please refer to README for usage: https://github.com/narfman0/helga-markovify/#helga-markovify
"""


@command('markovify', aliases=['markov'], help=_HELP_TEXT, shlex=True)
def markovify(client, channel, nick, message, cmd, args):
    topic = args[1] if len(args) > 1 else _DEFAULT_TOPIC
    kwargs = {}
    if args[0] == 'ingest' or args[0] == 'learn':
        learning_type = args[2] if len(args) > 2 else ''
        learning_type_source = args[3] if len(args) > 3 else ''
        text = ''
        if learning_type == 'text':
            text = learning_type_source
        elif learning_type == 'url':
            text = requests.get(learning_type_source).text
        elif learning_type == 'dpaste':
            soup = BeautifulSoup(requests.get(learning_type_source).text, "html.parser")
            text = soup.select('.highlight')[0].text
        elif learning_type == 'twitter':
            twitter_kwargs = {}
            topic_tweet = db.markovify.find_one({'topic':topic})
            if topic_tweet:
                twitter_kwargs['since_id'] = topic_tweet['since_id']
            try:
                tweets, since_id = twitter_timeline(learning_type_source, **twitter_kwargs)
                text = ''
                for tweet in tweets:
                    text = add_punctuation(text, tweet, add_punctuation)
                kwargs['since_id'] = since_id
            except Exception as e:
                return 'Error ingesting topic: ' + topic + ' error: ' + str(e)
        if _ADD_PUNCTUATION:
            kwargs['add_punctuation'] = _ADD_PUNCTUATION
        try:
            ingest(topic, text, **kwargs)
            return random_ack()
        except ValueError as e:
            return str(e)
    elif args[0] == 'generate':
        try:
            return generate(topic, **kwargs)
        except Exception as e:
            return str(e)
    elif args[0] == 'drop' or args[0] == 'delete':
        db.markovify.delete_many({'topic':topic})
        return random_ack()
    return "I don't understand args %s" % str(args)
