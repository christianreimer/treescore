# treescore
Score a Christmas Tree based on uniformity of lights, shape of tree, and colors used.

Writeup with pretty pictures can be see at
http://christianreimer.github.io/treescore/

## Simple Example

```python
>>> import treescore
>>> fname = 'path/to/image/of/tree.png'
>>> picker = treescore.ColorPicker.from_file('color.data')
>>> scores, _ = treescore.judge.score(fname, picker)
>>> print(scores)
Scores(overall=92.33, led=84.74, shape=97.24, color=95.00)
>>>
```

## Example with Images
```python
>>> import treescore
>>> fname = 'path/to/image/of/tree.png'
>>> picker = treescore.ColorPicker.from_file('color.data')
>>> _, images = treescore.judge.score(fname, picker, width=500, images=True)
>>> treescore.judge.utils.display_images(images)
```

This should display images such as the following (depending on your tree of
course)


# Installation

OpenCV (http://opencv.org/) is used and you will need to install it. This will
probably be the biggest challenge you will encounter. You can follow the
instructions for python3 and OpenCV version 3 over at
http://www.pyimagesearch.com/opencv-tutorials-resources-guides

Once you have OpenCV and the python bindings installed, the rest should be as
easy as

```bash
$ mkvirtualenv treescore
$ git clone https://github.com/christianreimer/treescore.git
$ cd treescore
$ pip install requirements.txt
$
```
