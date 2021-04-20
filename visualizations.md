# Visualizations with MATPLOTLIB

## Introduction

`pyplot` is the major object-oriented interface  

* **Figure object** is a container that holds everything that you see on the page
* **Axes object** is the part of the page that holds the data. 

```python
import matplotlib.pyplot as plt 

fig, ax = plt.subplots()
ax.plot(seattle_weather['MONTH'], seattle_weather ['MLY-TAVG-NORMAL'])
ax.plot(austin_weather['MONTH'], austin_weather ['MLY-TAVG-NORMAL'])
plt.show()
```

### Customizing plots

* use [arguments](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.plot.html) to `ax.plot()` to customize how data is plotted
* set axis labels with the methods `ax.set_xlabel()` & `ax.set_ylabel()`  
  * Use sentence-case
* set title with `ax.set_title()` method  

### Small multiples

Multiple small plots that show similar data.

* Set grid with [`plt.subplots(nrows, ncols)`](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.subplots.html)
  * use `sharex`, `sharey` arguments to align x axes
* Access plots by indexing the axes object (`ax[2, 1]`)
  * single column grids can be accessed with row only (`ax[0]`)

## Timeseries data

* Set Dataframe index to timeseries column to make plotting by index easier

```python
# Create variable seventies with data from "1970-01-01" to "1979-12-31"
seventies = climate_change["1970-01-01": "1979-12-31"]

# Add the time-series for "co2" data from seventies to the plot
ax.plot(seventies.index, seventies["co2"])
```

* Plot differnt variables with differnt scales using the `twinx` method

```python
import matplotlib.pyplot as plt

# Initalize a Figure and Axes
fig, ax = plt.subplots()

# Plot the CO2 variable in blue
ax.plot(climate_change.index, climate_change['co2'], color='b')

# Create a twin Axes that shares the x-axis
ax2 = ax.twinx()

# Plot the relative temperature in red
ax2.plot(climate_change.index, climate_change['relative_temp'], color='red')

plt.show()
```

* Annotate plot elements with `annotate()` method  

```python
ax.annotate(">1 degree", xy=(pd.Timestamp('2015-10-06'), 1), xytext=(pd.Timestamp('2008-10-06'), -0.2),arrowprops={'arrowstyle': "->", "color":"gray"})
```

## Quantitative comparisons  

### Bar-charts  

[Bar-charts](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.bar.html) show the value of a variable in different conditions.  

```python
fig, ax = plt.subplots()

# Plot a bar-chart of gold medals as a function of country
ax.bar(medals.index, medals['Gold'])

# Set the x-axis tick labels to the country names
ax.set_xticklabels(medals.index, rotation=90)

# Set the y-axis label
ax.set_ylabel("Number of medals")
```

#### Stacked bar charts

* add a label to produce a legend
* Define stacks with key word `bottom`

```python
# Add bars for "Gold" with the label "Gold"
ax.bar(medals.index, medals['Gold'] , label='Gold')

# Stack bars for "Silver" on top with label "Silver"
ax.bar(medals.index, medals['Silver'], bottom=medals['Gold'], label='Silver')

# Stack bars for "Bronze" on top of that with label "Bronze"
ax.bar(medals.index, medals['Bronze'], bottom=medals['Gold'] + medals['Silver'], label='Bronze')
```

### Histograms

[Histograms](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.hist.html) show the distribution of values within a variable.  

* Labels are necessary. Use argument `label`

```python
fig, ax = plt.subplots()

# Plot a histogram of "Weight" for mens_rowing
ax.hist(mens_rowing['Weight'], label='Rowing', histtype='step', bins=5)

# Compare to histogram of "Weight" for mens_gymnastics
ax.hist(mens_gymnastics['Weight'], label='Gymnastics', histtype='step', bins=5)

ax.set_xlabel("Weight (kg)")
ax.set_ylabel("# of observations")

# Add the legend and show the Figure
ax.legend()
plt.show()
```

## Statistical plotting

Statistical plotting is a set of methods for using visualization to make comparisons.  

### Add error bars  

Error bars summarize the distribution of the data in one number, such as the standard deviation of the values.  

* For bar-charts use `xerr` & `yerr` keywords

```python
ax.bar('Rowing', mens_rowing['Height'].mean(), yerr=mens_rowing['Height'].std())
```

* For line plots use `ax.errorbar` method with `yerr` keyword set to the error series.

```python
ax.errorbar(seattle_weather['Month'], seattle_weather['MLY-TAVG-NORMAL'], yerr=seattle_weather['MLY-TAVG-STDDEV'])
```

### Boxplots

* Use `ax.boxplot` method. Labels are set with a list using `ax.set_xticklabels`

```python
ax.boxplot([mens_rowing['Height'], mens_gymnastics['Height']])
ax.set_xticklabels(['Rowing', 'Gymnastics'])
```

## Quantitative comarpisons  

Bi-variate comparison compares the values of two different variables.  

### Scatter plots

* For two variables, use `ax.scatter` method and set labels.  

```python
# Add data: "co2" on x-axis, "relative_temp" on y-axis
ax.scatter(climate_change['co2'], climate_change['relative_temp'])

# Set the x-axis label to "CO2 (ppm)"
ax.set_xlabel('CO2 (ppm)')

# Set the y-axis label to "Relative temperature (C)"
ax.set_ylabel('Relative temperature (C)')
```

* To plot a third, continuous variable, set it to the `c` argument

```python
ax.scatter(climate_change['co2'], climate_change['relative_temp'], c=climate_change.['date'])
```

## Sharing figures  

### Change style

* See https://matplotlib.org/stable/gallery/#style-sheets
* `plt.style.use(<style>)` changes the style for the session.  
* `plt.style.use('default')` resets the style to default.  

### Saving visualizations  

Replace `plt.show()` with `fig.savefig()`

* Control quality with the `quality` & `dpi` arguments  
* Control size with `fig.set_size_inches([5, 3])`  
