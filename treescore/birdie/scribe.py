"""
Contains functionality to create and format Twitter messages.
"""


def scribe(score, name):
    """Return a twitter blurb to go with a post"""
    return (
        'Hi @{}, nice #christmastree '
        'It has a #treescore of {} ('
        'lights:{} shape:{} color:{})'.format(
        name, score.overall, score.led, score.shape, score.color))


def post_to_twitter(score):
    """Determine if the score should be posted to twitter"""
    return all((score.overall > 50, score.area > 0.25))

