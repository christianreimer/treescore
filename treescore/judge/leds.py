"""
Produces a uniformity score (- - 100) based on the uniformity of the lights
on a Christmas tree. Higher score is better.

Algorithm:
1. Identify the lights by applying a threshold to fine the brightest parts of
   of the image
2. Identify the (x, y) coordinates of each led by taking the center of each
   bright region
3. For each locations of a light, find the 3 nearest lights
4. Take the mean of those distances and add to a list
5. Take the stddev of all the means
6. Reward trees with more lights
7. Returns a consistency score as 100

* Validation Neeed:
    - Must have at least 6 lights
"""

import cv2
import numpy as np
import math
from . import utils


def extract_bright_regions(img):
    """Extracts brightest part of the image under the assumptions those are
    the led lights"""
    (_, max_val, _, _) = cv2.minMaxLoc(img)
    margin = 0.9
    t_value = int(max_val * margin)
    _, thresh_img = cv2.threshold(img, t_value, 255, cv2.THRESH_BINARY)
    return thresh_img


def contours(image):
    """Returns the countours given the threshold image"""
    _, cnt, _ = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return cnt


def contour_positions(img):
    """Returns a list of (x, y) pairs corresponding to the centers of the
    contours found from the threshold image"""
    cnt_lst = contours(img)
    pos_lst = []
    for cnt in cnt_lst:
        mnt = cv2.moments(cnt)
        try:
            cx = int(mnt['m10']/mnt['m00'])
            cy = int(mnt['m01']/mnt['m00'])
        except ZeroDivisionError:
            pass
        else:
            pos_lst.append((cx, cy))
    return pos_lst


def distances(pair_lst, num=3):
    """Returns a list of distances between all positions from a list of (x, y)
    coordinates"""
    while pair_lst:
        x, y = pair_lst.pop()
        for x1, y1 in pair_lst:
            yield math.sqrt(math.pow((x1-x), 2) + math.pow((y1-y), 2))

def dist(pos1, pos2):
    """Returns the distance between pos1 and pos2"""
    x1, y1 = pos1
    x2, y2 = pos2
    return math.sqrt(math.pow(x1-x2, 2) + math.pow(y1-y2, 2))


def closest_neighbors(orig, neighbor_lst, num=3):
    """Returns the num closest neighbors"""
    dist_lst = [dist(orig, pos) for pos in neighbor_lst]
    dist_lst.sort()
    return dist_lst[:num]


def uniformity(pos_lst):
    """Return the nuiformity score based on the stddev of the mean distance
    between each point in the list and its closest neighbors"""
    mean_lst = []
    while len(pos_lst) > 2:
        orig = pos_lst.pop()
        mean_lst.append(np.array(closest_neighbors(orig, pos_lst)).mean())
    log_len = math.log(len(mean_lst))
    std_dev = np.array(mean_lst).std()
    return 100 - log_len * math.sqrt(std_dev)
    # return 100 - ((3 / log_len) * std_dev)


def avg_dist_friends(dist_lst, num=3):
    """Returns the average distance between the closest ::num pairs"""
    dist_lst.sort()
    small_std = np.array(dist[:num]).std()
    large_std = np.array(dist[-num:]).std()
    return small_std, large_std


def score(img):
    """Returns the led uniformity score for the image providede"""
    gray = utils.to_gray(img)
    cnt_img = extract_bright_regions(gray)
    pos_lst = contour_positions(cnt_img)
    return uniformity(pos_lst[:]), pos_lst

