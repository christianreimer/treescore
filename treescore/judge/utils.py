"""
Utilities to help work with opencv
"""

import cv2
from collections import Counter


def open_img(img_name):
    """Returns an image read from a file on disk"""
    return cv2.imread(img_name)


def save_images(img_tup, prefix):
    """Save images to disc"""
    for i, name in enumerate(img_tup._fields):
        cv2.imwrite('{}_{}.png'.format(prefix,name), img_tup[i])


def to_gray(img):
    """Converts an image to grayscale"""
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def to_hsv(img):
    """Converts an image to HSV format"""
    return cv2.cvtColor(img, cv2.COLOR_BGR2HSV)


def to_bgr(img):
    """Converts an image to HSV format"""
    return cv2.cvtColor(img, cv2.COLOR_HSV2BGR)


def to_binary(img):
    """Returns a binary image"""
    return cv2.threshold(img, 10, 255, cv2.THRESH_BINARY)


def display_img(img, name='Image'):
    """Displays in image until a key is pressed"""
    cv2.imshow(name, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def display_images(img_lst):
    """Displays several images at ones"""
    for i, img in enumerate(img_lst):
        cv2.imshow('Image %s' % i, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def resize(img, width=None, height=None):
    """Resize a image to the specified width or height"""
    if width:
        ratio = width / img.shape[1]
        dim = (width, int(round(img.shape[0] * ratio)))
    elif height:
        ratio = height / img.shape[0]
        dim = (int(round(img.shape[1] * ratio)), height)
    else:
        raise ValueError('Must specify either width or height')
    return cv2.resize(img, dim, interpolation=cv2.INTER_AREA)


def blur(img, kernel):
    """Blur image as per the specified kernel"""
    return cv2.GaussianBlur(img, kernel, 0)


def extract_colors(img):
    """Extracts all the color combinations in the given image"""
    colors = Counter()
    for row in img:
        colors.update([tuple(t) for t in row])
    return colors


def get_all_colors(image_names):
    aggregate = Counter()
    for name in image_names:
        img = open_img(name)
        colors = extract_colors(img)

        if aggregate:
            aggregate = aggregate & colors
        else:
            aggregate = colors
    return aggregate


def points(cnt):
    """Return iterator that produces (x,y) coordinates from a countour array"""
    for c in cnt:
        yield tuple(c[0])


def tuples(img):
    """Return iterator that produdes (b,g,r) tuples from an image"""
    for row in img:
        for col in row:
            yield (col)  # tuple(col)


def filtered_tuples(lower, upper):
    """Return function that can be used to iterate over an image (an array
    of tuples) that will only return the tuples that fall between the lower
    and upper bounds"""
    def func(img):
        for row in img:
            for col in row:
                if sum(col) > lower and sum(col) < upper:
                    yield tuple(col)
    return func

