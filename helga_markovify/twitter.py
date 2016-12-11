from helga import settings
import tweepy


def twitter_timeline(screen_name, since_id=None):
    """ Return relevant twitter timeline """
    consumer_key = twitter_credential('consumer_key')
    consumer_secret = twitter_credential('consumer_secret')
    access_token = twitter_credential('access_token')
    access_token_secret = twitter_credential('access_secret')
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return get_all_tweets(screen_name, api, since_id)


def get_all_tweets(screen_name, api, since_id):
    """ Get all tweets for the givens screen_name. Returns list of text/created_at pairs. """
    # Twitter only allows access to a users most recent 3240 tweets with this method
    all_tweets = []
    # initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name=screen_name, count=200, since_id=since_id)
    all_tweets.extend(new_tweets)
    if len(all_tweets) == 0:
        raise Exception("tweets up to date for screen_name: %s" % (screen_name))
    oldest = all_tweets[-1].id - 1
    while len(new_tweets) > 0:
        print("getting tweets before %s" % (oldest))
        new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest, since_id=since_id)
        all_tweets.extend(new_tweets)
        oldest = all_tweets[-1].id - 1
        print("...%s tweets downloaded so far" % (len(all_tweets)))
    return [tweet.text.encode("utf-8") for tweet in all_tweets], all_tweets[0].id


def twitter_credential(name):
    """ Grab twitter credential from settings """
    credential_name = 'TWITTER_' + name.upper()
    if hasattr(settings, credential_name):
        return getattr(settings, credential_name)
    else:
        raise AttributeError('Missing twitter credential in settings: ' + credential_name)
