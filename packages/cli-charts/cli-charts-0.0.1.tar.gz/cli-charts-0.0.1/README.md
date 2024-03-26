# cli-charts

cli-charts is a simple Python package for visualizing graphs and charts directly in the CLI.

This library allows you to visualize graphs and charts straight in your CLI. Just provide the coordinates and see your chart in the command line interface.

## Usage

To start, simply initialize the library like so:

```python
from cli-charts import CHART

chart = CHART()
```

### Parameters:
    > granular(boolean) => To compress the chart to fit more space


To draw a graph:

```Python
chart.plot_graph([])
```

This prints out the graph of the values provided

### Parameters:
    > values(list) => A list of coordinates(should be a list of lists, each list containing two integers)


To draw a bar graph:

```Python
chart.draw_bar([], 7, 3)
```

This prints out the bar graph of the values provided, each bar having a width of seven characters with three spaces between them

### Parameters:
    > values(list) => A list of coordinates(should be a list of lists, each list containing a string and an integer)
    > barWidth(int) => The size of the bars(default is 10)
    > space(int) => The space between the bars(default is 5)


To draw a pictogram(also pictograph):

```Python
chart.draw_pict([], '&')
```

This prints out a pictograph of the values provided with value represented by '&'

### Parameters:
    > values(list) => A list of coordinates(should be a list of lists, each list containing a string and an integer)
    > symbol(str) => Symbol to be used(default is '|')