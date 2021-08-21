# Python notes

- [OOP - Classes](#oop---classes)
  - [Best practices](#best-practices)
  - [Instance-level data uses self to bind to an instance](#instance-level-data-uses-self-to-bind-to-an-instance)
  - [Class-level data is](#class-level-data-is)
  - ["Class methods"](#class-methods)
  - [Sub classes](#sub-classes)
  - [Customizing functionality](#customizing-functionality)
  - [Opeerator overloading](#opeerator-overloading)
    - [Comparison operators](#comparison-operators)
    - [String representation](#string-representation)
  - [Exceptions](#exceptions)
  - [Best practices of class design](#best-practices-of-class-design)
    - [Designing for inheritance and polymorphism](#designing-for-inheritance-and-polymorphism)
      - [Liskov substitution principle](#liskov-substitution-principle)
      - [Managing data access: private attributes](#managing-data-access-private-attributes)
- [Databases and python](#databases-and-python)
  - [Connecting to a database](#connecting-to-a-database)
  - [Introduction to SQL queries](#introduction-to-sql-queries)
    - [ResultProxy vs ResultSet](#resultproxy-vs-resultset)
    - [SQL queries with SQLAlchemy](#sql-queries-with-sqlalchemy)
    - [Handling a ResultSet](#handling-a-resultset)

## OOP - Classes

### Best practices

- Initialize attributes in `__init__()`
- Use CamelCase for class names and lower_snake_case for functions and attributes
- Always use "self" for `self`
- Always include docstrings

### Instance-level data uses self to bind to an instance

```python
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary
```

### Class-level data is

- defined in the class body
- shared with all instances
- accessed with class name
- often used for min/max values for attributes and commonly used values
  and constants
- are called with `Class.ATTRIBUTE` syntax

```python
class Employee:
    # Define a class attribute
    MIN_SALARY = 30000
    def __init__(self, name, salary):
        self.name = name
        # Use class name to access class attribute
        if salary >= Employee.MIN_SALARY:
            self.salary = salary
        else:
            self.salary = Employee.MIN_SALARY
```

### "Class methods"

- are declared with the `@classmethod` decorator
- cannot use instance-level data
- are called with `Class.method()` syntax
- are often used for alternative constructors

```python
class Employee:
    # Define a class attribute
    MIN_SALARY = 30000
    def __init__(self, name, salary=30000):
        self.name = name
        # Use class name to access class attribute
        if salary >= Employee.MIN_SALARY:
            self.salary = salary
        else:
            self.salary = Employee.MIN_SALARY

    @classmethod                        # <--Declare with decorator
    def from_file(cls, filename):       # <--Use cls not self
        with open(filename, 'r') as f:  # <--Cannot access anything with self.
            name = f.readline()
        return cls(name)                # <--Calls the class without __init__

# Create an employee without calling Employee()
emp = Employee.from_file("employee_data.txt")
```

### Sub classes

- are created by including the parent class as an argument to a new class
- Inherit all the features of the parent class
- are used to add or modify functionality of an existing class
- can access data from the parent class

```python
# Parent class
class BankAccount:
    def __init__(self, balance):
        self.balance = balance

    def withdraw(self, ammount):
        self.balance -= amount

# Inherited class
class SavingsAccount(BankAccount):
    # Constructor specifically for SavingsAccount
    def __init__(self,balance, interest_rate):  # <--- additional arg added
        # Call the parent's constructor using ClassName.__init__(self, args)
        # You do not have to call the parent's __init__ method
        # but you will probably want to
        BankAccount.__init__(self, balance)     # <--- self is a SavingsAccount
                                                #       and also a BankAccount
        # added functionality of child class
        self.interest_rate = interest_rate

    # added functionality of a new method
    def compute_interest(self, n_periods = 1):
        return self.balance * ((1 + self.interest_rate) ** n_periods -1)
```

### Customizing functionality

Child methods inherited from the parent class can be modified

1. Inherit parent class in a new class
2. Add a customized constructor that calls the parent's constructor
3. Add a method from the parent class with a new argument
4. Do something then call the parent's method to finish the task

```python
class CheckingAccount(BankAccount):             # <--- Child class
    def __init__(self, balance, limit):         # <--- New __init__ method
        BankAccount.__init__(self, content)     # <--- Calls parent's __init__
        self.limit = limit                      # <--- Adds new attribute

    def deposit(self, amount):                  # <--- Brand new method
        self.balance += amount

    def withdraw(self, amount, fee=0):          # <--- Overridden method
        if fee <= self.limit:                   # <--- New logic added
            BankAccount.withdraw(self, amount - fee)    # <--- Calls parent's method with
        else:                                           # <--- Class.method() syntax
            BankAccount.withdraw(self, amount - self.limit) # <--- include 'self' arg in
                                                            # <--- in calls to parent

# Create a BankAccount object
bank_acct = BankAccount(1000)

# Calling 'withdraw' executes the method for the caller's class
# Since the caller is a BankAccount, that withdraw method is used
bank_acct.withdraw(200)

# Create an instance of the CheckingAccount class
# This new class inherits from BankAccount
check_acct = CheckingAccount(1000, 25)

# Since the caller is a CheckingAccount, the logic in CheckingAccount runs
# This keeps the interface consistent for child objects
# The object type determines which method to execute
check_acct.withdraw(200)
```

This pattern (aka polymorphism) keeps the interface consistent by letting the object type determine which methods to apply
Add additional consistency by passing arguments with `*args, **kwargs`. This insures compatability with parent classes

```python
# Import pandas as pd
import pandas as pd

# Define LoggedDF inherited from pd.DataFrame and add the constructor
class LoggedDF(pd.DataFrame):
  
  def __init__(self, *args, **kwargs):
    pd.DataFrame.__init__(self, *args, **kwargs)
    self.created_at = datetime.today()
    
  def to_csv(self, *args, **kwargs):
    # Copy self to a temporary DataFrame
    temp = self.copy()
    
    # Create a new column filled with self.created_at
    temp["created_at"] = self.created_at
    
    # Call pd.DataFrame.to_csv on temp, passing in *args and **kwargs
    pd.DataFrame.to_csv(temp, *args, **kwargs)
```

### Opeerator overloading

#### Comparison operators

When comparing two classes, python compares the object pointers to memory.
To redefine how python compares objects for equality, override the
`__eq__` method. Be sure to check the class `type()` for equality also.

Other comparison operators

```python
==  __eq__()
!=  __ne__()
>=  __ge__()
<=  __le__()
>   __gt__()
<   __lt__()
    __hash__()  # <--- To use objects as dictionary keys and in sets
```

```python
class Customer:
    def __init__(self, id, name):
        self.id, self.name= id, name

    # Overridden equality (==) method
    def __eq__(self, other):                # <--- Called with == and 2 args self and other
        if (type(self) == type(other)) and \
            (self.id == other.id) and \
            (self.name == other.name):      # <--- Redefines equality to mean 
            return True                     # <--- Classes are the same and all
        else:                               # <--- attribues are equal.
            return False                    # <--- Returns a Boolean
                                            
```

When comparing an object with it's child class, the child's comparison methods
are called.

```python
p = Parent()
c = Child()

p == c 
# Child's __eq__() called
# ReturnsTrue
```

#### String representation

Objects have two string representations:

- `__str__()`
  - **str**ing representation
  - informal - for end user
  - `print(obj)`
    - `print(np.array([1,2,3]))` returns `[1 2 3]`
  - `str(obj)`
    - `str(np.array([1, 2,3]))` returns `[1 2 3]`

```python
class Customer:
    def __init__(self, name, balance):
        self.name, self.balance = name, balance

    def __str__(self):
        cust_str = """
                    Customer: 
                        name: {name}
                        balance: {balance}
                    """.format(name = self.name, \
                                balance = self.balance)
        return cust_str

cust = Customer("Maryam Azar", 3000)
print(cust)

Customer: 
    name: Maryam Azar
    balance: 3000
```

- `__repr__()`
  - **repr**oducible **repr**esentation
  - formal - for developer
  - returns a string that can reproduce the object
  - `repr(obj)`
    - `repr(np.array([1,2,3]))` returns `array([1, 2, 3])`
  - printing in console
  - fallback for `print()`

```python
class Customer:
    def __init__(self, name, balance):
        self.name, self.balance = name, balance

    # Because no string method is defined, __repr__() is the fallback

    def __repr__(self):
        return f"Customer('{self.name}', '{self.balance}')" # <--- Needs a return
                                                            # <--- not a print()
                                                            # <--- Note the quotes


cust = Customer("Maryam Azar", 3000)
cust  # <--- Implicitly calls __repr__()
# ---> Customer('Maryam Azar", '3000')

print(cust)
# ---> Customer('Maryam Azar", '3000')
```

### Exceptions

Exceptions shoud follow try, except, finally pattern.

```python
try
    # try some code
except ExceptionNameHere:
    # Run this code if ExceptionNameHere happens
finally:        # <--- Optional
    # Run this code no matter what
    # Useful for clean up
```

Call exceptions with `raise`
Define custom exceptions classes by inheriting from `BaseException` or `Exception`
Define exception hierarcy by inheriting from custom classes
It's better to include an except block for a child exception before the block for a parent exception, otherwise the child exceptions will be always be caught in the parent block, and the except block for the child will never be executed.

```python
class SalaryError(ValueError): pass
class BonusError(SalaryError): pass

class Employee:
  MIN_SALARY = 30000
  MAX_BONUS = 5000

  def __init__(self, name, salary = 30000):
    self.name = name    
    if salary < Employee.MIN_SALARY:
      raise SalaryError("Salary is too low!")      
    self.salary = salary
    
  def give_bonus(self, amount):
    if amount > Employee.MAX_BONUS:
       raise BonusError("The bonus amount is too high!") # <--- Child class first
        
    elif self.salary + amount <  Employee.MIN_SALARY:
       raise SalaryError("The salary after bonus is too low!")
      
    else:  
      self.salary += amount
```

### Best practices of class design

#### Designing for inheritance and polymorphism

Using a unified interface to operate on objects of different classes

Consider the following; `batch_withdraw()` doesn't need to check the object to
know which withdraw() to call

```python
# Withdraw amount from each of accounts in list_of_accounts
def batch_withdraw(list_of_accounts, amount):
    for acct in list_of_accounts:
        acct.withdraw(amount)
b, c, s = BankAccount(1000), CheckingAccount(2000), SavingsAccount(3000)
batch_withdraw([b,c,s]) # <--- Will use BankAccount.withdraw(),
                        #       then CheckingAccount.withdraw(),
                        #       then SavingsAccount.withdraw()

# Liskov substitution principle - Wherever BankAccount works, CheckingAccount
# should work as well
```

##### Liskov substitution principle

Base class should be interchangeable with any of its subclasses without altering any properties of the program.

- Syntacticcally - Function signatures are compatible
  - arguments, returned values
  - EG: `BankAccount.withdraw()` requires 1 parameter, but `CheckingAccount.withdraw()` requires 2. Fix: add same parameter to parent class with a default value
- Semantically - The state of the object and the program remains consistent
  - Sublcass method doesn't strengthen input conditions
    - EG: `BankAccout.withdraw()` accepts any amount, but `CheckingAccount.withdraw()` assumes that the amount is limited.
  - Subclass method doesn't weaken output conditions
    - Eg: `BankAccount.withdraw()` can only leave a positive balance or cause an error
    - Eg: `CheckingAccount.withdraw()` can leave balane negative
- no additional exceptions
- If class hierarchy violates LSP, then do not use inheritance because the program will behave in unpredictable ways.

##### Managing data access: private attributes

All class data is public. Restrict access with:

- Naming conventions
  - Preceding single underscore
    - `obj._att_name`, `obj._method_name()`
    - use to identify attributes that are not part of the public API
    - use for internal implementation details and helper functions
  - Double underscore - pseudoprivate attributes
    - `__attr_name`, `obj.__method_name()`
    - Not inherited directly
    - Inherited with name mangling - `obj.__attr_name` is interpreted as obj._MyClass__attr_name`
    - Use to prevent name clashes in inherited classes
    - Use to protect attributes and methods from being overriden
- `@property` for restricted and read-only attributes
  - without a setter method the attribute is read-only
  - `@attr.getter` is used to run code when a property is retrieved
  - `@attr.deleter` is used to run code when a property is deleted with `del`
- Overriding `__getattr__()` and `__setattr__()`

```python
class Employer:
    def __init_(self, name, new_salary):
        self._salary = new_salary       # <--- Use "protected" attribute to 
                                        #       to store data

    @property                           # <--- Use @property on a method whose 
    def salary(self):                   #       name is exactly the name of the
        return self._salary             #       restricted attribute but
                                        #       return the internal attribute

    @salary.setter                      # <--- Use @attr.setter on a method 
    def salary(self, new_salary):       #       that will be called on
        if new_salary < 0:              #       obj.attr = value
            raise ValueError("Invalid salary")
        self._salary = new_salary       # <--- The value to assign is passed
                                        #       as arg
```

## Databases and python

### Connecting to a database

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

### Introduction to SQL queries

#### ResultProxy vs ResultSet

- `ResultProxy`: object with query information
- `ResultSet`: the data requested by the `ResultProxy`

```python
from sqlalchemy import create_engine
# Create DB engine
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

#### SQL queries with SQLAlchemy

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

#### Handling a ResultSet

Once we have a ResultSet, we can use Python to access all the data within it
by column name and by list style indexes.

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
