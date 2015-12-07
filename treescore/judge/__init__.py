"""
Runs the Treescore judging process
"""

from . import utils
from . import leds
from . import shape
from . import colors
from . import draw

from collections import namedtuple

Scores = namedtuple('Scores', 'overall led shape color')
Images = namedtuple('Images', 'original leds contour sketched')


def score(fname, picker, width=500, images=False):
    """Run the treescoring process on an image.

    Usage::

    >>> import treescore.judge as judge
    >>> scores = judge.score(fname, picker)
    >>> scores, images = judge.score(fname, picker, images=True)

    :param fname: A string, the full path to the image file
    :param picker: A :class:`ColorPicker`
    :param width: An int, the width to resize the image to
    :param images: A boolean, should outputimages be produced
    :returns: A namedtuple, containing the scores
    :returns: A namedtuple, containing the generated images
    """
    img_original = utils.resize(utils.open_img(fname), width=width)
    contour = shape.tree_contours(shape.tree_mask(img_original, picker))
    img_tree, img_mask = shape.extract_tree(img_original, contour)
    corners = shape.corners(img_original, contour)
    score_shape = shape.score(corners)
    img_contour = draw.contour(img_original.shape, contour)
    score_led, point_lst = leds.score(img_original)

    ratios = colors.ratios(img_original, picker)
    score_color = colors.score(ratios)

    score_overall = int(round(sum([score_led, score_shape, score_color]) / 3))
    score_tup = Scores(score_overall, score_led, score_shape, score_color)
    img_tup = None

    if images:
        img_leds = draw.leds(img_original.shape, point_lst)
        img_sketched = draw.sketch(img_contour.copy(), point_lst, corners)
        img_tup = Images(img_original, img_leds, img_contour, img_sketched)

    return score_tup, img_tup

