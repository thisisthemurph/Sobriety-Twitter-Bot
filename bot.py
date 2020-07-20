import tweepy
import logging
import re

from config import create_api, get_config
from chip import Chip

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

class TweetStreamListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()
    
    def on_status(self, tweet):
        logger.info(f"Tweeting to {tweet.user.name} ({tweet.user.screen_name})")

        self.reply_to_tweet(tweet)
        # self.like_tweet(tweet)

    def on_error(self, status):
        logger.error("There was an error with the stream listener")
        return False

    def like_tweet(self, tweet):
        if not tweet.favorited:
            try:
                tweet.favorite()
            except Exception:
                logger.error("Error favouriting tweet")

    def reply_to_tweet(self, tweet):
        # Ignore replies and own tweets
        if tweet.in_reply_to_status_id is not None or tweet.user.id == self.me.id:
            return

        # TODO Remove - only for testing
        test_accounts = get_config()["TESTING_ACCOUNTS"]
        if tweet.user.screen_name not in test_accounts:
            return
        
        regex = re.compile("([1-9][0-9]{0,2}) (days|weeks)", re.IGNORECASE)
        match = regex.search(tweet.text)
        number, duration = match.group().split(" ")

        chip = Chip(number)

        media_obj = self.api.media_upload(chip.path)

        self.api.update_status(
            status=f"@{tweet.user.screen_name} Congratulations!",
            media_ids=[media_obj.media_id],
            in_reply_to_status_id=tweet.id
        )

        chip.delete()


def main():
    api = create_api()

    twitter_listener = TweetStreamListener(api)
    stream = tweepy.Stream(api.auth, twitter_listener)
    stream.filter(track=["been sober for"], languages=["en"])

if __name__ == "__main__":
    main()
