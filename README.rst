===============
helga-markovify
===============

.. image:: https://badge.fury.io/py/helga-markovify.png
    :target: https://badge.fury.io/py/helga-markovify

.. image:: https://travis-ci.org/narfman0/helga-markovify.png?branch=master
    :target: https://travis-ci.org/narfman0/helga-markovify

Ingest corpuses of text and output a sentence generated from markov chains.
Helga will now listen to your IRC channel and ingest dialog along the way,
learning to speak your lingo. You may jump start this with 'logs' ingestion or
any other ingestion technique.

Installation
============

After installing and configuring helga, use::

    pip install helga-markovify

Add ``markovify`` to your settings and restart helga. To use twitter timelines,
you must also add the following to settings (with your credentials)::

    TWITTER_CONSUMER_KEY = 'asad'
    TWITTER_CONSUMER_SECRET = 'sdfs'
    TWITTER_ACCESS_TOKEN = 'fghf'
    TWITTER_ACCESS_SECRET = 'ghjg'

Usage
=====

Note: Please use punctuation in your text. This is a tough sticking point in
practice, but it is important to be able to differentiate sentences.

Command syntax::

    ingest <topic> <learning_type> <learning_type_source>
    generate <topic>
    drop <topic>

Arguments
---------

``topic``: like tagging, so helga can respond in different ways

``learning_type``: how helga is going to ingest. Can be text, a url to raw data,
a url to dpaste, or a twitter account.

``learning_type_source``: the corresponding data e.g. plaintext if learning_type
is "text", a url if "url", twitter screen name if "twitter", helga_log_reader
arguments for "logs" (suggest you go old and use current channel)


The ``ingest`` command teaches the bot about the topic from the referenced
corpus. You may teach the bot from any number of sources, it can be twitter or
text. Mix and matching is fine.

The ``generate`` command generates a sentence from the corpus.

The ``drop`` command drops a particular topic from storage. If a corpus becomes
corrupt for whatever reason, a user may drop it and re-ingest data to populate
it again.

Settings
--------

``MARKOVIFY_ADD_PUNCTUATION``: If we should add periods after lines. You always
want good punctuation for good generated sentences, this is a pretty safe "True"
by default.

``MARKOVIFY_CHANNEL_LISTEN``: Ingest current channel chatter. A bit expensive,
and possibly not great privacy-wise, but that's where the lol-train arrives.

``MARKOVIFY_CHANNEL_GENERATE``: Regex helga listens to to generate response for
default channel chatter

``MARKOVIFY_TOPIC_DEFAULT``: Default ingestion topic for channel data

``TWITTER_CONSUMER_KEY TWITTER_CONSUMER_SECRET TWITTER_ACCESS_TOKEN TWITTER_ACCESS_SECRET``:
if using twitter, you'll want these from your configured twitter apps.

Examples
========

The following are different ways you may usage helga-markovify. Most are
different ways to ingest/learn data.

URL
---

.. code-block::

    !markovify ingest zen url https://hg.python.org/peps/raw-file/tip/pep-0020.txt
    !markovify generate zen
    helga> Sparse is better than ugly.

Text
----

.. code-block::

    !markovify ingest hitler text "Mein Kampf is the best Kampf."
    !markovify ingest hitler text "Don't be stupid, be a smarty. Come and join the nazi party."
    !markovify ingest hitler text "Make America hate again."
    !markovify ingest hitler text "Kampf America is hate nazi smarty. Hate party again filler sentence. America is the best at being terrible."
    !markovify generate hitler
    helga> Mein Kampf is the best at being terrible.

dpaste
------

.. code-block::

    !markovify ingest zen dpaste http://dpaste.com/1JF2P4S
    !markovify generate zen
    helga> If the implementation is hard to explain, it may be a good idea.

Twitter
-------

.. code-block::

    !markovify ingest narf twitter narfman0
    !markovify generate narf
    helga> You won't believe this one weird trick to get the target populace hooked.
    !markovify generate narf
    helga> FOSS: it only takes one highly incentivized dealer to get 4057$ a month doing nothing!

Channel logs
------------

.. code-block::

    !markovify ingest channel logs --channel #bots --start_date 1999-01-01
    !markovify generate channel
    helga> dropbox serving it does ASAP

    helga, thoughts?
    helga> it could be a crackhead, who wants to haskell bees

Drop corpus
-----------

If you have somehow screwed up or broken a corpus, you may drop it completely::

    !markovify drop zen

TODO
====

* Travis
* Talk about specific topics
* Keep history aka conversations
* Weighted round-robin type conversation

License
=======

Copyright (c) 2016 Jon Robison

See included LICENSE for licensing information
