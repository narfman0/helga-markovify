""" Plugin entry point for helga """
import re
import requests
from bs4 import BeautifulSoup
from helga import settings
from helga.db import db
from helga.plugins import command, match, random_ack
from helga_log_reader.plugin import parse_logs
from helga_markovify.markov import punctuate, ingest, generate
from helga_markovify.twitter import twitter_timeline


_ADD_PUNCTUATION = settings.MARKOVIFY_ADD_PUNCTUATION if hasattr(settings, 'MARKOVIFY_ADD_PUNCTUATION') else True
_CHANNEL_LISTEN = settings.MARKOVIFY_CHANNEL_LISTEN if hasattr(settings, 'MARKOVIFY_CHANNEL_LISTEN') else False
_CHANNEL_GENERATE = settings.CHANNEL_GENERATE if hasattr(settings, 'MARKOVIFY_CHANNEL_GENERATE') else r'.*[what|have]?.*[think|thoughts?|say|respon\w+]\?'
_CHANNEL_GENERATE_REGEX = re.compile(settings.NICK + _CHANNEL_GENERATE, re.I)
_DEFAULT_TOPIC = settings.MARKOVIFY_TOPIC_DEFAULT if hasattr(settings, 'MARKOVIFY_TOPIC_DEFAULT') else 'default'
_HELP_TEXT = """Ingest data to produve markov chain text. Helga always listens.
Please refer to README for usage: https://github.com/narfman0/helga-markovify#examples"""


def _handle_command(client, channel, nick, message, cmd, args):
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
            topic_tweet = db.markovify.find_one({'topic': topic})
            if topic_tweet:
                twitter_kwargs['since_id'] = topic_tweet['since_id']
            try:
                tweets, since_id = twitter_timeline(learning_type_source, **twitter_kwargs)
                for tweet in tweets:
                    text = punctuate(text, tweet, _ADD_PUNCTUATION)
                kwargs['since_id'] = since_id
            except Exception as e:
                return 'Error ingesting topic: ' + topic + ' error: ' + str(e)
        elif learning_type == 'logs':
            # would be wise to save the last accessed date, but we also save on
            # chat. since you can drop corpus, let's avoid this for now.
            _, logs = parse_logs(args[3:], channel=learning_type_source)
            regex = re.compile(r'\n[0-9][0-9]:[0-9][0-9]:[0-9][0-9] - \w+ - ', re.I)
            text = re.sub(regex, '. ', logs)
        try:
            ingest(topic, text, **kwargs)
            return random_ack()
        except ValueError as e:
            return str(e)
    elif args[0] == 'generate':
        try:
            return generate(topic, _ADD_PUNCTUATION, **kwargs)
        except Exception as e:
            return str(e)
    elif args[0] == 'drop' or args[0] == 'delete':
        db.markovify.delete_many({'topic': topic})
        return random_ack()
    return "I don't understand args %s" % str(args)


def _handle_match(client, channel, nick, message, matches):
    """ Match stores all channel info. If helga is asked something to
    stimulate a markov response about channel data, then we shall graciously
    provide it.
    """
    generate_interrogative = _CHANNEL_GENERATE_REGEX.match(message)
    if generate_interrogative:
        return generate(_DEFAULT_TOPIC, _ADD_PUNCTUATION)
    current_topic = db.markovify.find_one({'topic': _DEFAULT_TOPIC})
    if current_topic:
        message = punctuate(current_topic['text'], message, _ADD_PUNCTUATION)
    try:
        ingest(_DEFAULT_TOPIC, message)
    except ValueError as e:
        # not good, but this is done every message so just move along
        print str(e)


@match(lambda x: _CHANNEL_LISTEN)
@command('markovify', aliases=['markov'], help=_HELP_TEXT, shlex=True)
def markovify(client, channel, nick, message, *args):
    fn = _handle_command if len(args) == 2 else _handle_match
    return fn(client, channel, nick, message, *args)
