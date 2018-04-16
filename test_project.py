import unittest
import main
import tweepy
from twitter_credentials import *
import os

class Test(unittest.TestCase):

    def setUp(self):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.client = tweepy.API(auth)
        self.dirname = os.path.dirname(__file__)

    def tearDown(self):
        pass

    def test_email_1date(self):
        filename = os.path.join(self.dirname, 'test_emails/test_email_1_success.html')
        extracted_dates = main.parse_email(filename)
        self.assertEqual(extracted_dates[0], 'April 14 2018')

    def test_email_empty(self):
        filename = os.path.join(self.dirname, "test_emails/test_email_2_fail.html")
        extracted_dates = main.parse_email(filename)
        self.assertEqual(extracted_dates, [])

    def test_email_2dates(self):
        filename = os.path.join(self.dirname, "test_emails/test_email_3_success.html")
        extracted_dates = main.parse_email(filename)
        self.assertEqual(extracted_dates[0], "September 23 2018")
        self.assertEqual(extracted_dates[1], "September 26 2018")

    def check_twitter(self):
        main.request_pickup('test tweet')
        tweet = self.client.user_timeline(id=self.client_id, count=1)[0]
        self.assertEqual(tweet.text, 'test tweet')


if __name__ == '__main__':
    unittest.main()