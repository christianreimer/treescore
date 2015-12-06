# treescore
Score a Christmas Tree based on uniformity of lights, shape of tree, and colors used.

Additional information here: http://christianreimer.github.io/treescore/

```python
>>> import treescore
>>> fname = 'path/to/image/of/tree.png'
>>> picker = treescore.ColorPicker.from_file('color.data')
>>> scores, _ = treescore.judge.score(fname, picker)
>>> print(scores)
Scores(overall=92.33, led=84.74, shape=97.24, color=95.00)
```
