"""
Functionality related to the Twitter api interactions.
"""

import os
import urllib.request
import shutil
import twitter


class Connection(object):
    """Connection to the Twitter API"""
    def __init__(self, search_tag='#christmastree', twitter_creds=None):
        self.search_tag = search_tag
        self.auth = twitter_creds or (
            os.environ['twitter_access_tok'],
            os.environ['twitter_access_tok_sec'],
            os.environ['twitter_consumer_key'],
            os.environ['twitter_consumer_sec'])
        self.api = twitter.Twitter(auth=self.auth)
        self.upload = twitter.Twitter(domain='upload.twitter.com',
                                      auth=self.auth)
        self.last_id = 0

    def images(self):
        """Fetches new tweets with the chritmastree tag"""
        tweet_lst, meta = self.api.search.tweets(q=self.search_tag,
                                                 since_id=self.last_id)
        self.last_id = meta['max_id_str']
        self.refresh_url = meta['refresh_url']
        for tweet in tweet_lst:
            user = teewt['user']['screen_name']
            for e in t['entities']:
                if 'media_url' in e:
                    yield (user, e['media_url'])

    def post(self, text, image):
        """Post new tweet with image attachment"""
        with open(image, 'rb') as imagefile:
            img = imagefile.read()
        id_img1 = self.upload.media.upload(media=img)["media_id_string"]
        id_img2 = self.upload.media.upload(media=img)["media_id_string"]
        self.api.statuses.update(status=text,
                                 media_ids=','.join([id_img1, id_img2]))

    def fetch_image(self, url, fname):
        """Downloads an image from the specified URL"""
        with urllib.request.urlopen(url) as res, open(fname, 'wb') as ofile:
            shutil.copyfileobj(res, ofile)

