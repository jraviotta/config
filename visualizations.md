# Visualizations

## Seaborn

### Using pandas with seaborn

* Requires "tidy data"
* pass DataFrame to `data` argument
* use column name for arguments such as `x`, `y` & `hue`

### Visualizing two quantitative variables  

Many questions in data science are centered around describing the relationship between two quantitative variables. Seaborn calls plots that visualize this relationship "relational plots".  

#### Scatterplots

Use when each point is assumed to be an independent observation.

* Visualize subgroups in a simple relational plot with `hue`
* Plot subgroups as small multiples with `sns.relplot()`  
  * ["relplot()"](https://seaborn.pydata.org/generated/seaborn.relplot.html) plots quantitative data using scatterplots or lineplots
* Add additional dimensions with `row` & `col` arguments

```python
sns.relplot(x="G1", y="G3", 
            data=student_data,
            kind="scatter", 
            col="schoolsup",
            col_order=["yes", "no"],
            row='famsup', row_order=['yes','no'])
```

* Customize point size, style & hue to highlight categories

```python
sns.relplot(x="horsepower", y="mpg", data=mpg, 
            kind="scatter", size='cylinders', hue="cylinders")
sns.relplot(x='acceleration', y='mpg', data=mpg, 
            kind='scatter', style='origin', hue='origin')
```

* Customize transparancy to make clusters of points more visible
  
```python
sns.relplot(x='total_bill', y='tip', data=tips, 
            kind='scatter', alpha=0.4)
```

#### Lineplots

Use when tracking the same variable over time.  

* Lineplots with multiple observations per x-value aggregate using mean and show a confidence interval
  * Alter behavior with arguments
* Customize point style & hue to highlight categories  

```python
sns.relplot(x='hour', y='NO_2_mean', data=df, kind='line',
            style='location', hue='location')

# add markers to show datapoints
sns.relplot(x='hour', y='NO_2_mean', data=df, kind='line',
            style='location', hue='location', markers=True)

# turn off linestyle variations and keep marker variations
sns.relplot(x='hour', y='NO_2_mean', data=df, kind='line',
            style='location', hue='location', 
            markers=True, dashes=False)
```

#### Regression plots

Shows data and a regression model

* [`lmplot()`](https://seaborn.pydata.org/generated/seaborn.lmplot.html) combines regplot() and FacetGrid. It is intended as a convenient interface to fit regression models across conditional subsets of a dataset.

```python
sns.lmplot(x='quality', y='alcohol', data=df, col='type')
```

### Visualizing a categorical and a quantitative variable

Categorical plots involve a categorical variable, which is a variable that consists of a fixed, typically small number of possible values, or categories. These types of plots are commonly used when we want to make comparisons between different groups. `catplot()` is analagous to `relplot()`

#### Count plots and bar plots

**Count plots** show the sum of observations by categories.
**Bar plots** show the mean of a quantitative variable among observations in each category.

* To change the order of the categories, create a list of category values in the order that you want them to appear, and then use the "order" parameter.  
* change the orientation of the bars in bar plots and count plots by switching the x and y parameters.

```python
cat_order = ["<2 hours", 
            "2 to 5 hours", 
            "5 to 10 hours", 
            ">10 hours"]
sns.catplot(x="study_time", y="G3", data=student_data,
            kind="bar", order=cat_order)
```

#### Histograms, Box plots & Violin plots

* [Histograms](https://seaborn.pydata.org/generated/seaborn.displot.html#seaborn.displot), [box plots](https://seaborn.pydata.org/generated/seaborn.boxplot.html) & [violin plots](https://seaborn.pydata.org/generated/seaborn.violinplot.html) all show the distribution of quantitative data
* Box plots are compact and do not show the shape of the distribution
* Violin plots show the shape of the distribution
* Histograms allow binning

```python
# box plot
sns.catplot(x="romantic", y="G3",
            data=student_data,
            kind="box")

# violin plot
sns.catplot(kind='violin', y ='monthly_claims', x='dead', data=data, cut=0)

# histogram
sns.displot(data, x='last_day', hue='dead', element='step')
```

#### Point plots

Point plots show the mean of a quantitative variable for the observations in each category, plotted as a single point.

* Shows same informtion as bar plots
* Use point plots to directly compare subgroups among categories

```python
sns.catplot(x="famrel", y="absences",
            data=student_data,
            kind="point",
            capsize=0.2, join=False)

# use median instead of mean
from numpy import median
sns.catplot(x="famrel", y="absences",
            data=student_data,
            kind="point",
            capsize=0.2, join=False,
            estimator=median)
```

### Customizing seaborn plots

#### Customizing figure style

* Change figure style for the session using `sns.set_style()`
* Reset figure style with `sns.set_style('white')`
* "white", "dark", "whitegrid", "darkgrid", and "ticks"
* Use "grid" variants to highlight the specific values of plotted points instead of the overall plot
* "ticks" adds tick marks to x and y axes
* Remove spines with `sns.despine(top=True, right=True)`

#### Customizing palette

* Change plot colors globally with `sns.set_palette()`
* Use matplotlib color codes with `sns.set(color_codes=True)`
* **Circular palettes** are good if data is not ordered
  * 'paired'
* **Diverging palettes** are good to use if your visualization deals with a scale where the two ends of the scale are opposites and there is a neutral midpoint.  
  * "RdBu", "PRGn", "RdBu_r", "PRGn_r"
* **Sequential palettes** are good for emphasizing a variable on a continuous scale.
  * "Greys", "Blues", "PuRd", "GnBu"
* Create custom palettes by passing in a list of color names or hex codes.

```python
# Create and display a sequential palatte with 8 tones
p = sns.color_palette('Purples', 8)
sns.palplot(p)
plt.show()
```

#### Displaying palettes

```python
# display a palette
sns.palplot()

# return current palette
sns.color_palette()

# show seaborn palettes
for p in sns.palettes.SEABORN_PALETTES:
  sns.set_palette(p)
  sns.palplot(sns.color_palette())
  plt.show()
```

#### Customizing size

* Change the scale of your plot by using `sns.set_context()`.
* Default scale is "paper"
* The scale options from smallest to largest are "paper", "notebook", "talk", and "poster".  

#### Adding titles and labels

* Seaborn plots create two different types of objects: `FacetGrid` and `AxesSubplot`
* "relplot()" and "catplot()" both support making subplots and return `FacetGrid` objects. 
* Single-type plot functions like `scatterplot()` and `countplot()` return a single `AxesSubplot` object.
* Find type by assigning plot to a variable and then `type()` the variable

##### `FacetGrid` titles and labels

```python
g = sns.catplot(<stuff>)
g.fig.suptitle("Title")

# Move title up
g.fig.suptitle('Title', y=1.03)

# Alter subplot titles
g.set_titles("This is {col_name}")

# Add axis labels
g.set(xlabel="New X label", ylabel="New Y label")

# change tick labels
g.set(xticklabels=['new', 'new2'], yticklabel=['new', 'new2'])

# Rotate x-axis tick labels
plt.xticks(rotation=90)

# Wrap long text
text = "\n".join(textwrap.wrap('Really long text', 50))

# Replace text in subtitles
subs = {'race_title': 'race'}
for k,v in subs.items():
  for ax in g.fig.axes:
    title = ax.title.get_text()
    i.set_title(title.replace(k,v))
```

##### `FacetGrid` legends

```python
def update_legend(g: sns.FacetGrid, title:str=None, labels:list=None, ax_scale:float=1):
    """Alters a sns.FacetGrid legend title, values, and/or position.

    Args:
        g (sns.FacetGrid): seborn FacetGrid object
        title (str, optional): Legend title. Defaults to None.
        labels (list, optional): Legend labels. Defaults to None.
        ax_scale (float, optional): Value to re-scale axes to make room for legend labels. Defaults to 1.
    """
    # check axes and find which have legend
    for ax in g.axes.flat:
        leg = g.axes.flat[0].get_legend()
        # Scale ax to make room for legend
        box = ax.get_position()
        ax.set_position([box.x0,box.y0,box.width*ax_scale,box.height])
        if not leg is None: break
    # or legend may be on a figure
    if leg is None: leg = g._legend

    # change legend texts
    leg.set_title(title)
    for t, l in zip(leg.texts, labels): t.set_text(l)
```

##### `AxesSubplot` titles and labels

```python
g = sns.boxplot(<stuff>)
g.set_title('title', y=1.03)

# Add axis labels
g.set(xlabel="New X label", ylabel="New Y label")

# Rotate x-axis tick labels
plt.xticks(rotation=90)
```

## MATPLOTLIB - Introduction

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

### Timeseries data

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

### Quantitative comparisons  

#### Bar-charts  

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

##### Stacked bar charts

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

#### Histograms

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

### Statistical plotting

Statistical plotting is a set of methods for using visualization to make comparisons.  

#### Add error bars  

Error bars summarize the distribution of the data in one number, such as the standard deviation of the values.  

* For bar-charts use `xerr` & `yerr` keywords

```python
ax.bar('Rowing', mens_rowing['Height'].mean(), yerr=mens_rowing['Height'].std())
```

* For line plots use `ax.errorbar` method with `yerr` keyword set to the error series.

```python
ax.errorbar(seattle_weather['Month'], seattle_weather['MLY-TAVG-NORMAL'], yerr=seattle_weather['MLY-TAVG-STDDEV'])
```

#### Boxplots

* Use `ax.boxplot` method. Labels are set with a list using `ax.set_xticklabels`

```python
ax.boxplot([mens_rowing['Height'], mens_gymnastics['Height']])
ax.set_xticklabels(['Rowing', 'Gymnastics'])
```

### Quantitative comarpisons  

Bi-variate comparison compares the values of two different variables.  

#### Scatter plots

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

### Sharing figures  

#### Change style

* See https://matplotlib.org/stable/gallery/#style-sheets
* `plt.style.use(<style>)` changes the style for the session.  
* `plt.style.use('default')` resets the style to default.  

#### Saving visualizations  

Replace `plt.show()` with `fig.savefig()`

* Control quality with the `quality` & `dpi` arguments  
* Control size with `fig.set_size_inches([5, 3])`  
