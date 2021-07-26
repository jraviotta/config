# Minimally Sufficient Pandas Cheat Sheet

See also, [Minimally Sufficient Pandas.](https://www.dunderdata.com/post/minimally-sufficient-pandas-cheat-sheet)  
See also, [Conda Cheat Sheet](https://kapeli.com/cheat_sheets/Conda.docset/Contents/Resources/Documents/index)  
See also, [Pandas User Guide](https://pandas.pydata.org/pandas-docs/stable/user_guide/index.html)  

## Selecting Data

Use brackets to select a single column of data because the dot notation cannot column names with spaces, those that collide with DataFrame methods and when the column name is a variable.

```python
df[‘colname’] # do this
df.colname    # not that
```

* Selection with `at` and `iat`  
Use NumPy arrays if your application relies on performance for selecting a single cell of data and not `at` or `iat`. The `at` and `iat` indexers only give a small increase in performance when selecting a single DataFrame cell.

* The deprecated `ix` indexer  
Every trace of `ix` should be removed and replaced with the explicit `loc` or `iloc` indexers.

## read_csv vs read_table

Use `read_csv` for all cases. The only difference between these two functions is the default delimiter.

## Data cleaning

[About pandas dtypes](https://pandas.pydata.org/pandas-docs/stable/user_guide/basics.)  
Use `dtype` argument in `pd.read_csv` when possible to assign dtypes to columns  
Cast integers to `Int64`, a nullable dtype in pandas  
Use `convert_dtypes()` to convert to new dtypes with `pd.NA`  
Use `replace()` to normalize strings  
Drop unncesessary columns with `df.drop(['col1', 'col2', ...], inplace=True, axis=1)`  
Examine dtypes with `df.info()`  
Examine basic statistics with `df.describe(include='all')`.  
Examine counts of values with `df['col'].value_counts()`.  
Examine subsets of data with DataFrame indexing, `.loc`, or `.query`  
Select subsets of data using string methods. EG `nba[nba["fran_id"].str.endswith("ers")]`  
Combining criteria requires parenthases. EG `nba[(nba["pts"] > 100) &(nba["opp_pts"] > 100)]`  

## Missing data

[About pandas nan](https://pandas.pydata.org/pandas-docs/stable/user_guide/missing_data.html)  
Use `isna` and `notna` as they end with ‘na’ like the other missing value methods `fillna` and `dropna`.  
Replace missing values with `pd.NA` when possible.
Fill na values with `.fillna()`  
Fill na values with a pandas object `df.fillna(df.mean()["B":"C"])`  
Drop na values with `.dropna()` (requires axis arg)  
Approximate na values with `.interpolate()` (use `method` argument for more control)  

## Arithmetic and Comparison Operators vs Methods

Use the operators`( +, *, >, <=, etc..)` and not their corresponding methods `( add, mul, gt, le, etc…)` in all cases except when absolutely necessary such as when you need to change the direction of the alignment.

## Builtin Python functions vs Pandas methods with the same name

Use the Pandas method over any built-in Python function with the same name.

## Aggregation

* Use `df.groupby('grouping column').agg({'aggregating column': 'aggregating function'})` as it can handle more complex cases.  
* Use `gropuby` when you want to continue an analysis and `pivot_table` when you want to compare groups. A `groupby` aggregation and a `pivot_table` produce the same exact data with a different shape.  
* Only use `crosstab` when finding the relative frequency. The `pivot_table` method and the `crosstab` function are very similar.  
* Only use `pivot_table` and not `pivot`. The `pivot` method pivots data without aggregating. It is possible to duplicate its functionality with `pivot_table` by selecting an aggregation function.  
* Use `pivot_table` over `pivot` or `unstack`. `pivot_table` can handle all cases that `pivot` can, and `pivot` and `unstack` reshape data similarly.  
* Use `melt` over `stack` because it allows you to rename columns and it avoids a MultiIndex.

## Handling a MultiIndex

Flatten DataFrames after a call to `groupbyby` renaming columns and resetting the index. A DataFrame with a MultiIndex offers little benefit over one with a single-level index.

```python
df.reset_index()
# Flatten columns
df.columns = ['_'.join(col).rstrip('_') for col in df.columns.values]
```

## Setting with copy warning

https://www.dataquest.io/blog/settingwithcopywarning/

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

* Use `merge` method to join tables horizontally  
  * use `validate` argument to verify integrity
* Use `pd.merge_ordered()` to merge ordered or timeseries data
  * Use `fill_method` argument rather than `.fillna()` when appropriate
* Use `pd.merge_asof()` to merge **sorted** ordered or timeseries date that has close but not identical `on` columns
* Use `pd.concat()` to join tables vertically
  * use `verify_integrity` argument to verify integrity
  * use `ignore_index=True` when appropriate to reset the index

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

### Joining Data

```python
concat
merge
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
