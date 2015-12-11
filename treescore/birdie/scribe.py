"""
Contains functionality to create and format Twitter messages.
"""


def scripe(score, name):
    """Return a twitter blurb to go with a post"""
    return (
        'Hi @{}, that is a nice #christmastree you have there! '
        'It gets an overall #treescore of {}. '
        '{} for lights, {} for shape, and {} for color'.format(
        name, score.overall, score.led, score.shape, score.color))


def post_to_twitter(score):
    """Determine if the score should be posted to twitter"""
    return score.overall > 70 and min(score) > 30

