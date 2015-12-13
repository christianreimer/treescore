"""
API to connet and interact with twitter.
"""

import pickle

import twitter
import cv2

from .api import Connection
from .scribe import post_to_twitter
from .scribe import scribe

from ..judge import utils
from ..judge import shape
from .. import judge
from . import scribe

History = set()


def save_history():
    with open('history.data', 'wb') as pfile:
        pickle.dump(History, pfile)


def load_history():
    global History
    with open('history.data', 'rb') as pfile:
       History = pickle.load(pfile)


def creds():
    """Return OAuth object based on credentials store locally"""
    with open('creds.secret') as pfile:
        return twitter.OAuth(pickle.load(pfile))


def manual(con, path, picker):
    global History

    if not len(History):
        load_history()

    for user, image_url in con.images():
        if image_url in History:
            print("{}'s tree {} already processed".format(user, image_url))
            continue

        print('Checking image from {}'.format(user))
        if user == 'treescore':
            print('Skipping own post ...')
            continue

        fname = "{}/{}".format(path, user)
        con.fetch_image(image_url, fname)
        try:
            scores, _, image = judge.score(fname, picker, images=True)
        except:
            continue
        print(scores)
        utils.display_img(image)
        print('Should post to twitter: {}'.format(
            scribe.post_to_twitter(scores)))
        answer = input('Post to Twitter (y/n)?: ')
        if answer in ('y', 'Y'):
            text = scribe.scribe(scores, user)
            fname2 = "{}.composite.png".format(fname)
            cv2.imwrite(fname2, image)
            con.post(text, fname2)
        History.add(image_url)

