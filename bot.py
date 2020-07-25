import tweepy
import logging
import re

from config import create_api, get_config
from chip import Chip
from quote import random_quote

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

class TweetStreamListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()
    
    def on_status(self, tweet):
        logger.info(f"Tweeting to {tweet.user.name} ({tweet.user.screen_name})")

        if tweet.in_reply_to_status_id is not None or tweet.user.id == self.me.id:
            logger.info("Ignoring reply to or own tweet")
            return

        days = self.get_duration_in_days(tweet)
        self.like_tweet(tweet)
        self.reply_to_tweet(tweet, days)

    def on_error(self, status):
        logger.error("There was an error with the stream listener")
        return False
    
    def get_duration_in_days(self, tweet) -> int or None:
        """
        Determines if the tweet has a specified sobriety duration
        Returns the length of sobriety in days

        Returns:
            int or None

        """
        regex = re.compile("([1-9][0-9]{0,2}) (days|weeks|months|years)", re.IGNORECASE)
        match = regex.search(tweet.text)

        if match:
            number, duration = match.group().split(" ")

            durations = {
                "day": 1,
                "days": 1,
                "week": 7,
                "weeks": 7,
                "month": 30.4161,
                "months": 30.4161,
                "year": 365,
                "years": 365
            }

            return round(int(number) * durations.get(duration, 1))
        else:
            return None

    def like_tweet(self, tweet):
        if not tweet.favorited:
            try:
                tweet.favorite()
            except Exception:
                logger.error("Error favouriting tweet")

    def reply_to_tweet(self, tweet, days=None):
        # TODO Remove - only for testing
        test_accounts = get_config()["TESTING_ACCOUNTS"]
        if tweet.user.screen_name not in test_accounts:
            return

        media_ids = []
        if days is not None:
            chip = Chip(days)
            media_obj = self.api.media_upload(chip.path)
            media_ids.append(media_obj.media_id)
        
        self.api.update_status(
            status=f"Congratulations @{tweet.user.screen_name}!\n\n{random_quote()}",
            media_ids=media_ids,
            in_reply_to_status_id=tweet.id
        )

        if days is not None:
            chip.delete()


def main():
    api = create_api()

    twitter_listener = TweetStreamListener(api)
    stream = tweepy.Stream(api.auth, twitter_listener)
    stream.filter(track=["been sober for"], languages=["en"])

if __name__ == "__main__":
    main()
