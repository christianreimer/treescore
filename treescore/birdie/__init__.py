"""
API to connet and interact with twitter.
"""

import pickle

import twitter

from .api import Connection
from ..judge import utils
from .. import judge


def creds():
    """Return OAuth object based on credentials store locally"""
    with open('creds.secret') as pfile:
        return twitter.OAuth(pickle.load(pfile))


def manual(con, path, picker):
    for user, image in con.images():
        print('Checking image from {}'.format(user))
        fname = "{}/{}".format(path, user)
        con.fetch_image(image, fname)
        scores, images = judge.score(fname, picker, images=True)
        print(scores)
        utils.display_images(images)
        answer = input('Post to Twitter (y/n)?: ')
        if answer in ('y', 'Y'):
            text = scribe.scribe(score, user)
            fname2 = "{}/{}2".format(path, fname)
            con.post(text, fname, fname2)

