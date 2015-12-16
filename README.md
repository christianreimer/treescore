# treescore
Score a Christmas Tree based on uniformity of lights, shape of tree, and colors used.

Writeup with pretty pictures can be see at
http://christianreimer.github.io/treescore/

## Simple Example

```python
>>> import treescore
>>> fname = 'path/to/image/of/tree.png'
>>> picker = treescore.RegressionColorPicker.from_file('model.data')
>>> scores, images, composite = treescore.judge.score(fname, picker, images=True)
>>> print(scores)
Scores(overall=65, led=85, shape=97, color=12, area=0.290468)
>>> treescore.judge.utils.display_img(composite)
>>>
```

This should display an image such as the following (depending on your tree of
course)
![original image](../readme/composite.png)


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
$ pip install -r requirements.txt
$ ./judge --help
$
```

# Todo

There is still a lot of work to do to accurately detect colors and hence mask
out the tree itself.


