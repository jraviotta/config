# Python and databases

- [Connecting to a database](#connecting-to-a-database)
- [Introduction to SQL queries](#introduction-to-sql-queries)
  - [ResultProxy vs ResultSet](#resultproxy-vs-resultset)
  - [SQL queries with SQLAlchemy](#sql-queries-with-sqlalchemy)
  - [Handling a ResultSet](#handling-a-resultset)
  - [Filtering and targeting data](#filtering-and-targeting-data)
    - [Limitig data with `fetch` methods](#limitig-data-with-fetch-methods)
    - [Filtering data with *Where clauses*](#filtering-data-with-where-clauses)
  - [Aggregation functions](#aggregation-functions)
    - [Handling ResultSets from functions](#handling-resultsets-from-functions)
    - [Using pandas for visualization](#using-pandas-for-visualization)
- [Advanced SQLAlchemy Queries](#advanced-sqlalchemy-queries)
- [Creating and manipulating databases](#creating-and-manipulating-databases)

## Connecting to a database

Use sqlalchemy to wrap database interactions

- Engine: common interface to the database from SQLAlchemy
- Connection string: All the details required to find the database (and login, if necessary)
- Reflection: reads databse and builds SQLAlchemy `Table` objects

```python
from sqlalchemy import create_engine
engine = create_engine('sqlite:///census_nyc.sqlite')
connection = engine.connect()

# list tables
print(engine.table_names())

# Reflection
from sqlalchemy import MetaData, Table
metadata = MetaData()
census = Table('census', metadata, autoload=True, autoload_with=engine)
# Print the column names
print(census.columns.keys())
# Print Table object
print(repr(census))
```

## Introduction to SQL queries

### ResultProxy vs ResultSet

- `ResultProxy`: object with query information
- `ResultSet`: the data requested by the `ResultProxy`

```python
from sqlalchemy import create_engine
# Create DB engine dialect+driver://username:password@host:port/database
engine = create_engine('sqlite:///census.sqlite')

# Create a connection on engine
connection = engine.connect()

# Build select statement for census table: stmt
stmt = 'SELECT * FROM census'               # <--- Standard SQL

# Execute the statement and fetch the results: results
result_proxy = connection.execute(stmt)
results = result_proxy.fetchall()

# Print results
print(results)
```

### SQL queries with SQLAlchemy

- `select([<table>])` == `SELECT * FROM <table>`
  - Requires a list of one or more Tables or Columns
  - Using a table will select all the columns in it

```python
from sqlalchemy import create_engine, Table, select, MetaData
# Create DB engine
engine = create_engine('sqlite:///census.sqlite')

# Create a connection on engine
connection = engine.connect()

# initialize metadata
metadata = MetaData()

# Reflect census table via engine: census
census = Table('census', metadata, autoload=True, autoload_with=engine)

# Build select statement for census table: stmt
stmt = select([census])                         # <--- SQLAlchemy select

# Print the emitted statement to see the SQL string
print(stmt)

# Execute the statement on connection and fetch 10 records: result
results = connection.execute(stmt).fetchmany(size=10)

# Execute the statement and print the results
print(results)
```

### Handling a ResultSet

Using Python list style indexes and column names to access data in a ResultSet.

```python
# Get the first row of the results by using an index: first_row
first_row = results[0]

# Print the first row of the results
print(first_row)

# Print the first column of the first row by accessing it by its index
print(first_row[0])

# Print the 'state' column of the first row by using its name
print(first_row['state'])
```

### Filtering and targeting data

#### Limitig data with `fetch` methods

Limit the number of records returned with:

- `.fetchall()`
- `.fetchmany()`
- `.first()`
- `.scalar()` returns the single value of a query that produces one row x one column

#### Filtering data with *Where clauses*

- Restrict data returned by a query based on Boolean conditions
- Compare a column against a value or another column
- Often use comparisons ==, <=, >=, or !=
- Provide more complex conditions with *expressions*
  - E.g. `in_()`, `like()`, `between()`
  - many more in [documentation](https://docs.sqlalchemy.org/en/14/core/sqlelement.html#module-sqlalchemy.sql.expression)
  - Available as a method on a `Column`

```python
# create engine, metadata, and reflect the table
# <ABOVE>

# Select table
stmt = select([census])

# Append a where clause
stmt = stmt.where(census.columns.state.startswith('New'))

# Iterate over ResutProxy and print values
for result in connection.execute(stmt):     # <--- Don't need fetch method when
    print(result.state, result.pop2000)     #      using ResultProxy as an iterator
```

- Conjunctions provide syntax to include multiple criteria in a where clause
  - E.g. `and_()`, `or_()`, `not_()`
  - Includes trailing underscore to prevent confusion with python operators

```python
# create engine, metadata, and reflect the table
# <ABOVE>

# import or_()
from sqlalchemy import or_

# Create a query for census table: stmt
stmt = select([census])

# Append a where clause
stmt = stmt.where(
        or_(
            census.columns.state == 'California',
            census.columns.state == 'New York'
            )
        )

# Loop over the ResultProxy and print the values
for result in connection.execute(stmt):
    print(result.state, result.sex)
```

- Order data with `.order_by()` method
  - reverse sort on a column by wrapping with `desc()`
  - order by multiple columns by proving columns as argument

```python
# create engine, metadata, and reflect the table
# <ABOVE>

# Import desc
from sqlalchemy import desc

# Build a query to select the state and sex columns: stmt
stmt = select([census.columns.state, census.columns.sex])

# Order stmt by state in descending order: rev_stmt
rev_stmt = stmt.order_by(census.columns.state, desc(census.columns.sex))

# Execute the query and store the results: rev_results
rev_results = connection.execute(rev_stmt).fetchall()

# Print the first 10 rev_results
print(rev_results[:10])
```

### Aggregation functions

Functions that provide counting, summing and grouping of data

- E.g. `COUNT`, `SUM`
- from `sqlalchemy` module `func`
- more efficient than processing in Python
- Aggregate multiple records into one

```python
# create engine, metadata, and reflect the table
# <ABOVE>

# import func module
from sqlalchemy import func         #<--- do not import fuctions directly

# Put the column wrapped by func.sum in the select statement
stmt = select([func.sum(census.columns.pop2008)])   # <--- call with func.<method>

# Use the scalar fetch method to get back just a value and print it
results = connection.execute(stmt).scalar()         # <--- Returns a single value
print(results)
```

- Aggregate results by another column with `group_by()`
  - Accepts multiple columns and will group within the groups from left to right.
  - Every column in the select statement must in the group_by clause or
  wrapped in a function such as sum or count.

```python
# create engine, metadata, and reflect the table
# <ABOVE>

# Select the sex column and the func.sum of the pop2008 column
stmt = select([census.columns.sex,
                func.sum(census.columns.pop2008)])

# Append a group by clause that targets the sex column 
stmt = stmt.group_by(census.columns.sex)

# Execute the query and get the results
# The data is summed by the sex value of each record 
results = connection.execute(stmt).fetchall()
print(results)
```

- Group by multiple by including the additional columns in both the select
  and the group_by clause
  - Every column in the select statement must in the group_by clause or
        wrapped in a function such as sum or count.

```python
# create engine, metadata, and reflect the table
# <ABOVE>

# Select the sex column and the func.sum of the pop2008 column
stmt = select([census.columns.sex, census.columns.age,
                func.sum(census.columns.pop2008)])

# Append a group by clause that targets the sex column 
stmt = stmt.group_by(census.columns.sex, census.columns.age)

# Execute the query and get the results
# The data is summed by the sex and age value of each record 
results = connection.execute(stmt).fetchall()
print(results)
```

#### Handling ResultSets from functions

When using a function such as sum or count, the column name that represents the function in the results is set to a placeholder. The column names are often `<func>_#`. E.g. `count_1`

- Use the `label()` method on a function to give the output column a specific name

```python
# create engine, metadata, and reflect the table
# <ABOVE>

# Build an expression to calculate the sum of pop2008 labeled as population
pop2008_sum = func.sum(census.columns.pop2008).label('population')

# Build a query to select the state and sum of pop2008: stmt
stmt = select([census.columns.state, pop2008_sum])

# Group stmt by state
stmt = stmt.group_by(census.columns.state)

# Execute the statement and store all the records: results
results = connection.execute(stmt).fetchall()

# Print results
print(results)

# Print the keys/column names of the results returned
print(results[0].keys())    # <--- Returns ['state', 'population']
```

- Use `func.count` to call the column with `.distinct()` to count unique values

```python
# create engine, metadata, and reflect the table
# <ABOVE>

# Build a query to count the distinct states values: stmt
stmt = select([func.count(census.columns.state.distinct())])

# Execute the query and store the scalar result: distinct_state_count
distinct_state_count = connection.execute(stmt).scalar()

# Print the distinct_state_count
print(distinct_state_count)
```

#### Using pandas for visualization

## Advanced SQLAlchemy Queries

## Creating and manipulating databases
