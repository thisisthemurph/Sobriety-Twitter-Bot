import tweepy
import logging

from config import create_api, get_config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

class TweetStreamListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()
    
    def on_status(self, tweet):
        log = f"Tweeting to {tweet.user.name} ({tweet.user.screen_name})"
        logger.info(log)
        print(tweet.user.screen_name)

        self.reply_to_tweet(tweet)
        self.like_tweet(tweet)

    def on_error(self, status):
        logger.error("There was an error with the stream listener")
        return False

    def like_tweet(self, tweet):
        if not tweet.favorited:
            try:
                tweet.favorite()
            except Exception:
                logger.error("Error favouriting tweet", exc_info=True)

    def reply_to_tweet(self, tweet):
        # Ignore replies and own tweets
        if tweet.in_reply_to_status_id is not None or tweet.user.id == self.me.id:
            return

        # TODO Remove - only for testing
        test_accounts = get_config()["TESTING_ACCOUNTS"]
        if tweet.user.screen_name not in test_accounts:
            return

        self.api.update_status(
            status=f"@{tweet.user.screen_name} Congratulations!",
            in_reply_to_status_id=tweet.id
        )

def main():
    api = create_api()

    twitter_listener = TweetStreamListener(api)
    stream = tweepy.Stream(api.auth, twitter_listener)
    stream.filter(track=["been sober for"], languages=["en"])

if __name__ == "__main__":
    main()
