# FaStFig
FaStFig is a wrapper for matplotlib that provides a simple interface for fast and easy plotting.

Written by Fabian Stutzki, fast@fast-apps.de

licensed under MIT

## Usage
The package has to be imported:

```python
import fastfig
```

A very simple example is:

```python
fig = fastfig.Fig()
fig.plot()
fig.show()
```

FaStFig allows for more complex behavior with multiple subplots, legend, grid and saving to multiple files at once.

```python
fig = fastfig.Fig('PPT',nrows=2) # create figure
fig.plot([1,2,3,1,2,3,4,1,1]) # plot first data set
fig.title('First data set') # set title for subplot
fig.subplot() # set focus to next subplot/axis
fig.plot([0,1,2,3,4],[0,1,1,2,3],label="random") # plot second data set
fig.legend() # generate legend
fig.grid() # show translucent grid to highlight major ticks
fig.xlabel('Data') # create xlabel for second axis
fig.save('test_fig1.png','pdf') # save figure to png and pdf
```
