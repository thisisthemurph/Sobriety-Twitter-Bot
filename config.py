import tweepy
import logging
import json
import os

logger = logging.getLogger()

def get_config():
    with open("config.json") as json_file:
        return json.load(json_file)

def create_api():
    config = get_config()

    auth = tweepy.OAuthHandler(config["CONSUMER_KEY"], config["CONSUMER_SECRET"])
    auth.set_access_token(config["ACCESS_TOKEN"], config["ACCESS_TOKEN_SECRET"])

    api = tweepy.API(
        auth,
        wait_on_rate_limit=True,
        wait_on_rate_limit_notify=True
    )

    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exec_info=True)
        raise e

    logger.info("API created")
    return api