===============
helga-markovify
===============

Ingest corpuses of text and output a sentence generated from markov chains

Installation
============

After installing and configuring helga, use::

    pip install helga-markovify

Add 'markovify' to your settings and restart helga.

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

Some example commands (file)::

    !markovify ingest zen file zen.txt
    !markovify generate zen
    helga> If the implementation is hard to explain, it may be a good idea.

Alternate example (text)::

    !markovify ingest hitler text "Mein Kampf is the best Kampf."
    !markovify ingest hitler text "Don't be stupid, be a smarty. Come and join the nazi party."
    !markovify ingest hitler text "Make America hate again."
    !markovify ingest hitler text "Kampf America is hate nazi smarty. Hate party again filler sentence. America is the best at being terrible."
    !markovify generate hitler
    helga> Mein Kampf is the best at being terrible.

TODO
====

* Tweets
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
