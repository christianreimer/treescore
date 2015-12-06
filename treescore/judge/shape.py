from . import utils
from . import colors
import cv2
from collections import namedtuple
import math
import numpy as np

def tree_mask(img, picker):
    """Returns a threshold mask of the tree"""
    mask = colors.apply_color_mask(img, 'green', picker)
    mask = utils.blur(utils.to_gray(mask), (11, 11))
    _, t_img = cv2.threshold(mask, 1, 200, cv2.THRESH_BINARY)
    return t_img


def extract_tree(img, contour):
    """Returns the tree masked out from the rest of the image"""
    mask = np.zeros_like(img)
    white = (255, 255, 255)
    mask = cv2.drawContours(mask, [contour], -1, white, -1)
    tree = np.zeros_like(img)
    tree[mask == white] = img[mask == white]
    return tree, mask


def tree_contours(mask):
    """Returns the contours of the tree"""
    #edged = cv2.Canny(mask, 75, 200)
    _, cnts, _ = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    return sorted(cnts, key=cv2.contourArea, reverse=True)[0]
    return cnts


def find_bounds(countour_lst):
    """Finds the right, left, top, and bottom most points in the countour"""
    right, left, top, bottom, point = 0, 999, 999, 0, (None, None)
    for contour in contour_lst:
        for point in utils.points(contour):
            if y < top:
                point = (x, y)
            right = max(x, right)
            left = min(x, left)
            top = min(y, top)
            bottom = max(y, bottom)

    Bounds = namedtuple('Bounds', 'right left top bottom point')
    return Bounds(right, left, top, bottom, point)


def height_width_ratio(corners):
    """Determines the ration between the height and width of the tree based on
    the corners of the tree"""
    width = corners.bottom_right[0] - corners.bottom_left[0]
    height = corners.bottom_mid[1] - corners.top[1]
    return height / width


def angle(corners):
    """Returns the angular skew of the tree, 0 is perfectly vertical"""
    left_x, left_y = corners.bottom_left
    right_x, right_y = corners.bottom_right
    top_x, top_y = corners.top

    theo_x = (right_x - left_x) / 2 + left_x
    offset = abs(theo_x - top_x)
    height = round(abs(left_y + right_x) / 2) - top_y
    return math.degrees(math.atan(offset / height))


def corners(img, contour):
    """Returns the three corners of the tree based on the points of the
    countour list passed in"""
    height, width, _ = img.shape
    bottom_right_dist = dist_calc(width, height)
    bottom_left_dist = dist_calc(0, height)

    # distancs to bottom_let, bottom_right, top
    dr, dl, dt = 9999, 9999, 9999

    # points for best guess for bottom_right, bottom_left, top corners
    br, bl, tp_lst = (None, None), (None, None), []

    for point in utils.points(contour):
        dst = bottom_right_dist(*point)
        if dst < dr:
            dr = dst
            br = point
        dst = bottom_left_dist(*point)
        if dst < dl:
            dl = dst
            bl = point
        if point[1] < dt:
            tp_lst = [point]
        elif point[1] == dt:
            tp_lst.append(point)

    # If there are multiple top points, then we use the average value for the
    # x and y coordinate
    top_x = int(round(sum([x for (x, y) in tp_lst]) / len(tp_lst)))
    top_y = int(round(sum([y for (x, y) in tp_lst]) / len(tp_lst)))

    # Calculate the bottom middle point
    bottom_mid_x = int(round(br[0] - bl[0]) / 2) + bl[0]
    bottom_mid_y = int(round(abs(br[1] - bl[1]) / 2)) + min(br[1], bl[1])

    Corners = namedtuple('Corners', 'bottom_left, bottom_right, bottom_mid, top')
    return Corners(bl, br, (bottom_mid_x, bottom_mid_y), (top_x, top_y))


def dist_calc(x, y):
    """Returns a distance calcultion fuction from a static (x, y)"""
    def func(x1, y1):
        return math.sqrt(math.pow(x1-x, 2) + math.pow(y1-y, 2))
    return func


def score(corners):
    ideal_ratio = 4
    ratio = height_width_ratio(corners)
    ang_degrees = angle(corners)
    return 100 - abs(ideal_ratio - ratio) * ang_degrees

