===============
helga-markovify
===============

Ingest corpuses of text and output a sentence generated from markov chains

Installation
============

After installing and configuring helga, use::

    pip install helga-markovify

Add ``markovify`` to your settings and restart helga. To use twitter timelines, you
must add the following to settings as well::

    TWITTER_CONSUMER_KEY = 'asdasd'
    TWITTER_CONSUMER_SECRET = 'sdfsdfsd'
    TWITTER_ACCESS_TOKEN = 'fghfghfgh'
    TWITTER_ACCESS_SECRET = 'ghjghjkghjk'

Usage
=====

Note: Please use punctuation in your text. This is a tough sticking point in
practice, but it is helpful.

Command syntax::

    ingest <topic> <learning_type> <learning_type_source>
    generate <topic>

Arguments::

    topic: like tagging, so helga can respond in different ways
    learning_type: how helga is going to ingest. Can be text, a url to raw data,
    a relatively pathed (relative to plugin folder) file, or a twitter account.
    learning_type_source: the corresponding data e.g. plaintext if learning_type
    is "text", a url if "url", twitter id if "twitter"

Examples
========

Example commands (url)::

    !markovify ingest zen url https://hg.python.org/peps/raw-file/tip/pep-0020.txt
    !markovify generate zen
    helga> Sparse is better than ugly.

Alternate example (text)::

    !markovify ingest hitler text "Mein Kampf is the best Kampf."
    !markovify ingest hitler text "Don't be stupid, be a smarty. Come and join the nazi party."
    !markovify ingest hitler text "Make America hate again."
    !markovify ingest hitler text "Kampf America is hate nazi smarty. Hate party again filler sentence. America is the best at being terrible."
    !markovify generate hitler
    helga> Mein Kampf is the best at being terrible.

Some example commands (dpaste)::

    !markovify ingest zen dpaste http://dpaste.com/1JF2P4S
    !markovify generate zen
    helga> If the implementation is hard to explain, it may be a good idea.

Tweet ingestion (twitter)::

    !markov ingest narf twitter narfman0
    !markov generate narf
    helga> You won't believe this one weird trick to get the target populace hooked.
    !markov generate narf
    helga> FOSS: it only takes one highly incentivized dealer to get 4057$ a month doing nothing!

If you have somehow screwed up or broken a corpus, you may drop it completely::

    !markovify drop zen

TODO
====

* Generate default data from channel
* Add settings for max corpus count, max corpus length
* Travis
* Talk about specific topics
* Keep history aka conversations
* Weighted round-robin type conversation, e.g. trump vs jesus vs samuel l jackson vs kim jong un

License
=======

Copyright (c) 2016 Jon Robison

See included LICENSE for licensing information
