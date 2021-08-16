# Minimally Sufficient Pandas Cheat Sheet

See also, [Minimally Sufficient Pandas.](https://www.dunderdata.com/post/minimally-sufficient-pandas-cheat-sheet)  
See also, [Conda Cheat Sheet](https://kapeli.com/cheat_sheets/Conda.docset/Contents/Resources/Documents/index)  
See also, [Pandas User Guide](https://pandas.pydata.org/pandas-docs/stable/user_guide/index.html)  

- [Reading data](#reading-data)
- [Data inspection](#data-inspection)
- [Data cleaning](#data-cleaning)
- [Missing data](#missing-data)
- [Selecting Data](#selecting-data)
- [Arithmetic and Comparison Operators vs Methods](#arithmetic-and-comparison-operators-vs-methods)
- [Builtin Python functions vs Pandas methods with the same name](#builtin-python-functions-vs-pandas-methods-with-the-same-name)
- [Aggregation](#aggregation)
- [Handling a MultiIndex](#handling-a-multiindex)
- [Setting with copy warning](#setting-with-copy-warning)
  - [Using `iloc` to avoid chained assignments](#using-iloc-to-avoid-chained-assignments)
  - [Using `.copy()` to leave underlying data untouched](#using-copy-to-leave-underlying-data-untouched)
- [Joining tables](#joining-tables)
  - [Merge a table to itself](#merge-a-table-to-itself)
  - [Filtering joins](#filtering-joins)
    - [semi-join](#semi-join)
    - [anti-join](#anti-join)
  - [Setting a colum based on other columns](#setting-a-colum-based-on-other-columns)
- [Best of the DataFrame API](#best-of-the-dataframe-api)
  - [Attributes](#attributes)
  - [Aggregation Methods](#aggregation-methods)
  - [Non-Aggretaion Statistical Methods](#non-aggretaion-statistical-methods)
  - [Missing Value Handling](#missing-value-handling)
  - [Grouping](#grouping)
  - [Other](#other)
  - [Functions](#functions)

## Reading data

Use `read_csv` for all cases. Do not use `read_table`. The only difference between these two functions is the default delimiter.
Use `dtype` argument in `pd.read_csv` when possible to assign dtypes to columns  

## Data inspection

Drop unncesessary columns with `df.drop(['col1', 'col2', ...], inplace=True, axis=1)`  
Examine [dtypes](https://pandas.pydata.org/pandas-docs/stable/user_guide/basics.) with `df.info()`  
Examine basic statistics with `df.describe(include='all')`.  
Examine counts of values with `df['col'].value_counts()`.  
Examine counts of unique values in a dataframe with `df.unique()`.
Examine subsets of data with DataFrame indexing, `.loc`, or `.query`  

## Data cleaning  

Use `convert_dtypes()` to convert to new dtypes with `pd.NA`  
Use `replace()` to normalize strings  

## Missing data

[About pandas nan](https://pandas.pydata.org/pandas-docs/stable/user_guide/missing_data.html)  
Use `isna` and `notna` as they end with ‘na’ like the other missing value methods `fillna` and `dropna`.  
Replace missing values with `pd.NA` when possible.
Fill na values with `.fillna()`  
Fill na values with a pandas object `df.fillna(df.mean()["B":"C"])`  
Drop na values with `.dropna()` (requires axis arg)  
Approximate na values with `.interpolate()` (use `method` argument for more control)  

## Selecting Data

Use brackets to select a single column of data because the dot notation cannot column names with spaces, those that collide with DataFrame methods and when the column name is a variable.

```python
df[‘colname’] # do this
df.colname    # not that
```

- Select subsets of data using string methods. EG `nba[nba["fran_id"].str.endswith("ers")]`  
- Combining criteria requires parenthases. EG `nba[(nba["pts"] > 100) &(nba["opp_pts"] > 100)]`  
- Selection with `at` and `iat`  
Use NumPy arrays if your application relies on performance for selecting a single cell of data and not `at` or `iat`. The `at` and `iat` indexers only give a small increase in performance when selecting a single DataFrame cell.

- The deprecated `ix` indexer  
Every trace of `ix` should be removed and replaced with the explicit `loc` or `iloc` indexers.

## Arithmetic and Comparison Operators vs Methods

Use the operators`( +, *, >, <=, etc..)` and not their corresponding methods `( add, mul, gt, le, etc…)` in all cases except when absolutely necessary such as when you need to change the direction of the alignment.

## Builtin Python functions vs Pandas methods with the same name

Use the Pandas method over any built-in Python function with the same name.

## Aggregation

- Use `df.groupby('grouping column').agg({'aggregating column': 'aggregating function'})` as it can handle more complex cases.  
- Use `gropuby` when you want to continue an analysis and `pivot_table` when you want to compare groups. A `groupby` aggregation and a `pivot_table` produce the same exact data with a different shape.  
- Only use `crosstab` when finding the relative frequency. The `pivot_table` method and the `crosstab` function are very similar.  
- Only use `pivot_table` and not `pivot`. The `pivot` method pivots data without aggregating. It is possible to duplicate its functionality with `pivot_table` by selecting an aggregation function.  
- Use `pivot_table` over `pivot` or `unstack`. `pivot_table` can handle all cases that `pivot` can, and `pivot` and `unstack` reshape data similarly.  
- Use `melt` over `stack` because it allows you to rename columns and it avoids a MultiIndex.

## Handling a MultiIndex

Flatten DataFrames after a call to `groupbyby` renaming columns and resetting the index. A DataFrame with a MultiIndex offers little benefit over one with a single-level index.

```python
df.reset_index()
# Flatten columns
df.columns = ['_'.join(col).rstrip('_') for col in df.columns.values]
```

## Setting with copy warning

<https://www.dataquest.io/blog/settingwithcopywarning/>

### Using `iloc` to avoid chained assignments  

No

```python
data[data['bidder'] == 'parakeet2004']['bidderrate'] = 100
```

Yes

```python
data.loc[data.['bidder'] == 'parakeet2004', 'bidderrate'] = 100
```

### Using `.copy()` to leave underlying data untouched  

```python
winners = data.loc[data['bid'] == data['price']].copy()
winners.loc[304, 'bidder'] = 'therealname'
```

```python
print(winners.loc[304, 'bidder'])
therealname
print(data.loc[304, 'bidder'])
nan
```

## Joining tables  

- Use `merge` method to join tables horizontally  
  - use `validate` argument to verify integrity
- Use `pd.merge_ordered()` to merge ordered or timeseries data
  - Use `fill_method` argument rather than `.fillna()` when appropriate
- Use `pd.merge_asof()` to merge **sorted** ordered or timeseries date that has close but not identical `on` columns
- Use `pd.concat()` to join tables vertically
  - use `verify_integrity` argument to verify integrity
  - use `ignore_index=True` when appropriate to reset the index

### Merge a table to itself

- when working with tables that have a hierarchical relationship, like employee and manager  
- sequential relationships such as logistic movements  
- Graph data, such as networks of friends

### Filtering joins

#### semi-join

A semi-join filters the left table down to those observations that have a match in the right table. It is similar to an inner join where only the intersection between the tables is returned, but unlike an inner join, only the columns from the left table are shown. Finally, no duplicate rows from the left table are returned, even if there is a one-to-many relationship.  

1. Merge the two tables with an inner join  
2. Create a filter for ids from the left table that are in the right table  
3. Apply filter to left table  

```python
genres_tracks = genres.merge(top_tracks, on='gid', how='inner')
filter = genres['gid'].isin(genres_tracks['gid'])
top_genres = genres[filter]
```

#### anti-join

An anti-join returns the observations in the left table that do not have a matching observation in the right table. It also only returns the columns from the left table.  

1. use a left join with an indicator to return all of the rows from the left table  
2. use the `.loc` accessor and `_merge` column to select the rows that only appeared in the left table and return only the id column from the right table.
3. use the `isin()` method to filter for the rows with ids in filtered list.

```python
genres_tracks = genres.merge(top_tracks, on='gid', how='left', indicator=True)
gid_list = genres_tracks.loc[genres_tracks['_merge'] == 'left_only', 'gid']
non_top_genres = genres[genres['gid'].isin(gid_list)]
```

### Setting a colum based on other columns

- Use `.loc` with condition in row selector and the target column name
in the columns selector.  
- Set the value after the `=`  

```python
condition = df['col_1']==df['col_2']
df.loc[condition,'new_col']=True
```

## Best of the DataFrame API

The minimum DataFrame attributes and methods that can accomplish nearly all data analysis tasks. It reduces the number from over 240 to less than 80.

### Attributes

```python
columns
dtypes
index
shape
T
values
```

### Aggregation Methods

```python
all
any
count
describe
idxmax
idxmin
max
mean
median
min
mode
nunique
sum
std
var
```

### Non-Aggretaion Statistical Methods

```python
abs
clip
corr
cov
cummax
cummin
cumsum
diff
nlargest
nsmallest
quantile
rank
round
Subset Selection
head
iloc
loc
tail
```

### Missing Value Handling

```python
dropna
fillna
interpolate
isna
notna
```

### Grouping

```python
groupby
pivot_table
resample
rolling
```

### Other

```python
asfreq
astype
copy
drop
drop_duplicates
equals
isin
melt
plot
rename
replace
reset_index
sample
select_dtypes
shift
sort_index
sort_values
to_csv
to_json
to_sql
```

### Functions

```python
pd.concat
pd.crosstab
pd.cut
pd.qcut
pd.read_csv
pd.read_json
pd.read_sql
pd.to_datetime
pd.to_timedelta
```
