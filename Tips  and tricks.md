- [Tips and tricks](#tips-and-tricks)
  - [Importing & cleaning data](#importing--cleaning-data)
    - [Cleaning data](#cleaning-data)
      - [recode dtypes](#recode-dtypes)
      - [Address out of range data](#address-out-of-range-data)
      - [deduplicate](#deduplicate)
      - [Address Text and categorical problems](#address-text-and-categorical-problems)
  - [Pandas tricks](#pandas-tricks)
    - [Merging tables](#merging-tables)
      - [Merge a table to itself to itself](#merge-a-table-to-itself-to-itself)
    - [Filtering joins](#filtering-joins)
      - [semi-join](#semi-join)
      - [anti-join](#anti-join)

# Tips and tricks

## Importing & cleaning data

### Cleaning data

#### recode dtypes

- `df.info()`
- `df.describe()`
- `df['col'].astype('type')`, `pd.to_datetime()`
- `assert df['col'].dtype = 'type'`

#### Address out of range data

- drop if only a small # of observations
- change values to a hard limit such as max/min expected value
- set to missing and impute value

#### deduplicate

- identify duplicate rows with `.duplicated(keep=True)`
  - drop obvious duplicates with `.drop_duplicates()`
  - compare non-obvious columns with the other data

```python
# Drop complete duplicates from ride_sharing
ride_dup = ride_sharing.drop_duplicates()

# Create statistics dictionary for aggregation function
statistics = {'user_birth_year': 'min', 'duration': 'mean'}

# Group by ride_id and compute new statistics
ride_unique = ride_dup.groupby(by=['ride_id']).agg(statistics).reset_index()

# Find duplicated values again
duplicates = ride_unique.duplicated(subset = 'ride_id', keep = False)
duplicated_rides = ride_unique[duplicates == True]

# Assert duplicates are processed
assert duplicated_rides.shape[0] == 0
```

#### Address Text and categorical problems



## Pandas tricks

### Merging tables

#### Merge a table to itself to itself

You might need to merge a table to itself  

* when working with tables that have a hierarchical relationship, like employee and manager  
* sequential relationships such as logistic movements  
* Graph data, such as networks of friends

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
