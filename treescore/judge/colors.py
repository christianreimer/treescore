"""
Implements a color picker which will guess whick color class a given (b, g, r)
tuple belongs to.
"""

from collections import namedtuple
from collections import Counter
from collections import defaultdict
import pickle
from . import utils


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (127, 255, 0)
BLUE = (255, 0, 0)
RED = (0, 0, 255)
YELLOW = (0, 255, 255)
CYAN = (255, 255, 0)


class ColorPicker(object):
    """comment"""
    def __init__(self, range_map=None):
        self.range_map = range_map or {}
        self.unknown = Counter({'other': 1})

    @classmethod
    def from_file(cls, fname):
        """Loads from disk"""
        with open(fname, 'rb') as pfile:
            range_map = pickle.load(pfile)
        return ColorPicker(range_map)

    def save(self, fname):
        """Saves the range_map to disk"""
        with open(fname, 'wb') as pfile:
            pickle.dump(self.range_map, pfile)

    def guess(self, tup):
        """Returns the name of the color with the highest ratio"""
        if sum(tup) < 5:
            return 'black'
        if sum(tup) > 750:
            return 'white'
        return self.range_map.get(tup, self.unknown).most_common(1)[0][0]

    def set_ratios(self, color, counter):
        """Updates the ratios for the given color. Since these are rations,
        this cannot be done incrementally for a given color"""
        for tup, ratio in counter.items():
            ratio_cnt = self.range_map.get(tup, Counter())
            ratio_cnt[color] = ratio
            self.range_map[tup] = ratio_cnt


def extract_colors(img, pbar):
    """Returns all color tuples from the image"""
    colors = Counter()
    for row in img:
        colors.update([tuple(t) for t in row if sum(t) > 5 and sum(t) < 750])
    return colors


def apply_color_mask(img, color, picker):
    """Removes all pixels from the image that is not part of the specified
    color"""
    mask = img.copy()
    for i, row in enumerate(img):
        for j, tup in enumerate(row):
            mask[i][j] = tup if picker.guess(tuple(tup)) == color else [0, 0, 0]
    return mask


def ratios(img, picker, ignore=None):
    ratios = {'green': 0, 'red': 0, 'gold': 0, 'white': 0, 'black': 0, 'other': 0}
    for color in utils.tuples(img):
        ratios[picker.guess(color)] += 1
    for color in ignore or []:
        ratios.pop(color, None)
    total = sum(ratios.values())
    return {c: round(v / total * 100) for (c, v) in ratios.items()}


def score(ratios):
    """Return the deviation between observed and ideal ratios"""
    ratios.pop('black', None)
    ratios.pop('other', None)
    s = sum(ratios.values())

    observed = {}
    for color in ratios:
        observed[color] = ratios[color] / s * 100

    ideal = {'green': 50.0,
             'red': 20.0,
             'gold': 20.0,
             'white': 10.0}

    raw_score = 100 - sum([abs(ideal[c] - observed[c]) for c in ideal])
    return max(int(round(raw_score)), 0)

