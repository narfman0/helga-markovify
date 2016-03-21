""" Plugin entry point for helga """
import requests
from helga import settings
from helga.plugins import command, match
from helga_markovify.markov import ingest, generate


_ADD_PUNCTUATION = settings.MARKOVIFY_ADD_PUNCTUATION or True
_DEFAULT_TOPIC = settings.MARKOVIFY_TOPIC_DEFAULT or 'default'
_HELP_TEXT = """Ingest data to produve markov chain text. Helga always listens.
Please refer to README for usage: https://github.com/narfman0/helga-markovify/#helga-markovify
"""

@command('markovify', help=_HELP_TEXT, shlex=True)
def markovify(client, channel, nick, message, match):
    response = ''
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
        elif learning_type == 'file':
            with open(os.path.join(os.path.dirname(__file__), learning_type_source)) as f:
                ingest(topic, f.read())
        elif learning_type == 'twitter':
            return 'TODO Twitter not currently supported :('
        if _ADD_PUNCTUATION:
            kwargs{'add_punctuation':_ADD_PUNCTUATION}
        try:
            response = ingest(topic, text, **kwargs)
        except ValueError as e:
            return str(e)
    elif args[0] == 'generate':
        try:
            response = generate(topic, **kwargs)
        except Exception as e:
            return str(e)
    else:
        response = "I don't understand %s" % args[0]
    return response
