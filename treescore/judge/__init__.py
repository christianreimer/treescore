"""
Runs the Treescore judging process

- Load the image and resize it down
- Run the outline process to create a binary mask
- Apply mask to find tree
- Extract the color ratios from the tree
- Calculate the light uniformity score
- Calculate the shape from the mask
"""

from . import utils
from . import leds
from . import shape
from . import colors
# import cv2

from .colors import ColorPicker


def judge(fname, picker, width=500):
    """Runs the judging process on the image"""
    img = utils.resize(utils.open_img(fname), width=500)
    contour = shape.tree_contours(shape.tree_mask(img, picker))
    tree_img, mask_img = shape.extract_tree(img, contour)
    corners = shape.corners(img, contour)
    shape_score = shape.score(corners)
    contour_img = draw.draw_contour(img.shape, contour)
    outline_img = draw.draw_shape(img.shape, corners)
    led_score, point_lst = leds.score(img)
    led_img = draw.draw_dots(img.shape, point_lst)
    all_img = draw.draw_all(contour_img.copy(), point_lst, corners)

    return img, tree_img, mask_img, led_img, outline_img, contour_img, all_img, shape_score, led_score


