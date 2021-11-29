# Python notes

- [Docstrings](#docstrings)
  - [Module docstring](#module-docstring)
  - [Module-level function](#module-level-function)
  - [Generators](#generators)
  - [Exceptions](#exceptions)
  - [Classes](#classes)
- [Calling shell commands](#calling-shell-commands)
  - [Prefer `subprocess.run()` or `subprocess.check_call()`](#prefer-subprocessrun-or-subprocesscheck_call)
  - [High-level API vs `subprocess.Popen()`](#high-level-api-vs-subprocesspopen)
  - [Avoid os.system() and os.popen()](#avoid-ossystem-and-ospopen)
  - [Understand and usually use `check=True`](#understand-and-usually-use-checktrue)
  - [Understand and probably use `text=True` aka `universal_newlines=True`](#understand-and-probably-use-texttrue-aka-universal_newlinestrue)
  - [Understand shell=True vs shell=False](#understand-shelltrue-vs-shellfalse)
    - [Refactoring Example](#refactoring-example)
    - [Common Shell Constructs](#common-shell-constructs)
  - [Understand differences between sh and Bash](#understand-differences-between-sh-and-bash)
  - [A subprocess is separate from its parent, and cannot change it](#a-subprocess-is-separate-from-its-parent-and-cannot-change-it)
  - [Don't run Python from Python](#dont-run-python-from-python)

## Docstrings

Use [Google's style guide](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings).  

### Module docstring

```python
"""Example Google style docstrings.

This module demonstrates documentation as specified by the `Google Python
Style Guide`_. Docstrings may extend over multiple lines. Sections are created
with a section header and a colon followed by a block of indented text.

Example:
    Examples can be given using either the ``Example`` or ``Examples``
    sections. Sections support any reStructuredText formatting, including
    literal blocks::

        $ python example_google.py

Section breaks are created by resuming unindented text. Section breaks
are also implicitly created anytime a new section starts.

Attributes:
    module_level_variable1 (int): Module level variables may be documented in
        either the ``Attributes`` section of the module docstring, or in an
        inline docstring immediately following the variable.

        Either form is acceptable, but the two should not be mixed. Choose
        one convention to document module level variables and be consistent
        with it.

Todo:
    * For module TODOs
    * You have to also use ``sphinx.ext.todo`` extension

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""

module_level_variable1 = 12345

module_level_variable2 = 98765
"""int: Module level variable documented inline.

The docstring may span multiple lines. The type may optionally be specified
on the first line, separated by a colon.
"""
```

### Module-level function

```python
def module_level_function(param1, param2=None, *args, **kwargs):
    """This is an example of a module level function.

    Function parameters should be documented in the ``Args`` section. The name
    of each parameter is required. The type and description of each parameter
    is optional, but should be included if not obvious.

    If \*args or \*\*kwargs are accepted,
    they should be listed as ``*args`` and ``**kwargs``.

    The format for a parameter is::

        name (type): description
            The description may span multiple lines. Following
            lines should be indented. The "(type)" is optional.

            Multiple paragraphs are supported in parameter
            descriptions.

    Args:
        param1 (int): The first parameter.
        param2 (:obj:`str`, optional): The second parameter. Defaults to None.
            Second line of description should be indented.
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.

    Returns:
        bool: True if successful, False otherwise.

        The return type is optional and may be specified at the beginning of
        the ``Returns`` section followed by a colon.

        The ``Returns`` section may span multiple lines and paragraphs.
        Following lines should be indented to match the first line.

        The ``Returns`` section supports any reStructuredText formatting,
        including literal blocks::

            {
                'param1': param1,
                'param2': param2
            }

    Raises:
        AttributeError: The ``Raises`` section is a list of all exceptions
            that are relevant to the interface.
        ValueError: If `param2` is equal to `param1`.

    """
    if param1 == param2:
        raise ValueError('param1 may not be equal to param2')
    return True
```

### Generators

```python
def example_generator(n):
    """Generators have a ``Yields`` section instead of a ``Returns`` section.

    Args:
        n (int): The upper limit of the range to generate, from 0 to `n` - 1.

    Yields:
        int: The next number in the range of 0 to `n` - 1.

    Examples:
        Examples should be written in doctest format, and should illustrate how
        to use the function.

        >>> print([i for i in example_generator(4)])
        [0, 1, 2, 3]

    """
    for i in range(n):
        yield i
```

### Exceptions

```python
class ExampleError(Exception):
    """Exceptions are documented in the same way as classes.

    The __init__ method may be documented in either the class level
    docstring, or as a docstring on the __init__ method itself.

    Either form is acceptable, but the two should not be mixed. Choose one
    convention to document the __init__ method and be consistent with it.

    Note:
        Do not include the `self` parameter in the ``Args`` section.

    Args:
        msg (str): Human readable string describing the exception.
        code (:obj:`int`, optional): Error code.

    Attributes:
        msg (str): Human readable string describing the exception.
        code (int): Exception error code.

    """

    def __init__(self, msg, code):
        self.msg = msg
        self.code = code
```

### Classes

```python
class ExampleClass(object):
    """The summary line for a class docstring should fit on one line.

    If the class has public attributes, they may be documented here
    in an ``Attributes`` section and follow the same formatting as a
    function's ``Args`` section. Alternatively, attributes may be documented
    inline with the attribute's declaration (see __init__ method below).

    Properties created with the ``@property`` decorator should be documented
    in the property's getter method.

    Attributes:
        attr1 (str): Description of `attr1`.
        attr2 (:obj:`int`, optional): Description of `attr2`.

    """

    def __init__(self, param1, param2, param3):
        """Example of docstring on the __init__ method.

        The __init__ method may be documented in either the class level
        docstring, or as a docstring on the __init__ method itself.

        Either form is acceptable, but the two should not be mixed. Choose one
        convention to document the __init__ method and be consistent with it.

        Note:
            Do not include the `self` parameter in the ``Args`` section.

        Args:
            param1 (str): Description of `param1`.
            param2 (:obj:`int`, optional): Description of `param2`. Multiple
                lines are supported.
            param3 (:obj:`list` of :obj:`str`): Description of `param3`.

        """
        self.attr1 = param1
        self.attr2 = param2
        self.attr3 = param3  #: Doc comment *inline* with attribute

        #: list of str: Doc comment *before* attribute, with type specified
        self.attr4 = ['attr4']

        self.attr5 = None
        """str: Docstring *after* attribute, with type specified."""

    @property
    def readonly_property(self):
        """str: Properties should be documented in their getter method."""
        return 'readonly_property'

    @property
    def readwrite_property(self):
        """:obj:`list` of :obj:`str`: Properties with both a getter and setter
        should only be documented in their getter method.

        If the setter method contains notable behavior, it should be
        mentioned here.
        """
        return ['readwrite_property']

    @readwrite_property.setter
    def readwrite_property(self, value):
        value

    def example_method(self, param1, param2):
        """Class methods are similar to regular functions.

        Note:
            Do not include the `self` parameter in the ``Args`` section.

        Args:
            param1: The first parameter.
            param2: The second parameter.

        Returns:
            True if successful, False otherwise.

        """
        return True

    def __special__(self):
        """By default special members with docstrings are not included.

        Special members are any methods or attributes that start with and
        end with a double underscore. Any special member with a docstring
        will be included in the output, if
        ``napoleon_include_special_with_doc`` is set to True.

        This behavior can be enabled by changing the following setting in
        Sphinx's conf.py::

            napoleon_include_special_with_doc = True

        """
        pass

    def __special_without_docstring__(self):
        pass

    def _private(self):
        """By default private members are not included.

        Private members are any methods or attributes that start with an
        underscore and are *not* special. By default they are not included
        in the output.

        This behavior can be changed such that private members *are* included
        by changing the following setting in Sphinx's conf.py::

            napoleon_include_private_with_doc = True

        """
        pass

    def _private_without_docstring(self):
        pass
```

## Calling shell commands

from <https://stackoverflow.com/questions/4256107/running-bash-commands-in-python/51950538>

### Prefer `subprocess.run()` or `subprocess.check_call()`

The `subprocess.Popen()` function is a low-level workhorse but it is tricky to use correctly and you end up copy/pasting multiple lines of code ... which conveniently already exist in the standard library as a set of higher-level wrapper functions for various purposes, which are presented in more detail in the following.

Here's a paragraph from the documentation:

> The recommended approach to invoking subprocesses is to use the run() function for all use cases it can handle. For more advanced use cases, the underlying Popen interface can be used directly.

Unfortunately, the availability of these wrapper functions differs between Python versions.

- `subprocess.run()` was officially introduced in Python 3.5. It is meant to replace all of the following.
- `subprocess.check_output()` was introduced in Python 2.7 / 3.1. It is basically equivalent to `subprocess.run(..., check=True, stdout=subprocess.PIPE).stdout`
- `subprocess.check_call()` was introduced in Python 2.5. It is basically equivalent to subprocess.run(..., check=True)
- 1 was introduced in Python 2.4 in the original - subprocess module (PEP-324). It is basically equivalent to subprocess.run(...).returncode

### High-level API vs `subprocess.Popen()`

The refactored and extended subprocess.run() is more logical and more versatile than the older legacy functions it replaces. It returns a CompletedProcess object which has various methods which allow you to retrieve the exit status, the standard output, and a few other results and status indicators from the finished subprocess.

`subprocessrun() is the way to go if you simply need a program to run and return control to Python. For more involved scenarios (background processes, perhaps with interactive I/O with the Python parent program) you still need to use`subprocessPopen() and take care of all the plumbing yourself. This requires a fairly intricate understanding of all the moving parts and should not be undertaken lightly. The simpler Popen object represents the (possibly still-running) process which needs to be managed from your code for the remainder of the lifetime of the subprocess.

It should perhaps be emphasized that just `subprocessPopen() merely creates a process. If you leave it at that, you have a subprocess running concurrently alongside with Python, so a "background" process. If it doesn't need to do input or output or otherwise coordinate with you, it can do useful work in parallel with your Python program.

### Avoid os.system() and os.popen()

Since time eternal (well, since Python 2.5) the os module documentation has contained the recommendation to prefer subprocess over `os.system()`:

> The subprocess module provides more powerful facilities for spawning new processes and retrieving their results; using that module is preferable to using this function.

The problems with `system()` are that it's obviously system-dependent and doesn't offer ways to interact with the subprocess. It simply runs, with standard output and standard error outside of Python's reach. The only information Python receives back is the exit status of the command (zero means success, though the meaning of non-zero values is also somewhat system-dependent).

PEP-324 (which was already mentioned above) contains a more detailed rationale for why os.system is problematic and how subprocess attempts to solve those issues.

`os.popen()` used to be even more strongly discouraged:

 > Deprecated since version 2.6: This function is obsolete. Use the subprocess module.

However, since sometime in Python 3, it has been reimplemented to simply use subprocess, and redirects to the `subprocess.Popen()` documentation for details.

### Understand and usually use `check=True`

You'll also notice that `subprocess.call()` has many of the same limitations as `os.system()`. In regular use, you should generally check whether the process finished successfully, which `subprocess.check_call()` and `subprocess.check_output()` do (where the latter also returns the standard output of the finished subprocess). Similarly, you should usually use `check=True` with `subprocess.run()` unless you specifically need to allow the subprocess to return an error status.

In practice, with `check=True` or `subprocess.check_*`, Python will throw a CalledProcessError exception if the subprocess returns a nonzero exit status.

A common error with `subprocess.run()` is to omit `check=True` and be surprised when downstream code fails if the subprocess failed.

On the other hand, a common problem with `check_call()` and `check_output()` was that users who blindly used these functions were surprised when the exception was raised e.g. when grep did not find a match. (You should probably replace grep with native Python code anyway, as outlined below.)

All things counted, you need to understand how shell commands return an exit code, and under what conditions they will return a non-zero (error) exit code, and make a conscious decision how exactly it should be handled.

### Understand and probably use `text=True` aka `universal_newlines=True`

Since Python 3, strings internal to Python are Unicode strings. But there is no guarantee that a subprocess generates Unicode output, or strings at all.

(If the differences are not immediately obvious, Ned Batchelder's Pragmatic Unicode is recommended, if not outright obligatory, reading. There is a 36-minute video presentation behind the link if you prefer, though reading the page yourself will probably take significantly less time.)

Deep down, Python has to fetch a bytes buffer and interpret it somehow. If it contains a blob of binary data, it shouldn't be decoded into a Unicode string, because that's error-prone and bug-inducing behavior - precisely the sort of pesky behavior which riddled many Python 2 scripts, before there was a way to properly distinguish between encoded text and binary data.

With `text=True`, you tell Python that you, in fact, expect back textual data in the system's default encoding, and that it should be decoded into a Python (Unicode) string to the best of Python's ability (usually UTF-8 on any moderately up to date system, except perhaps Windows?)

If that's not what you request back, Python will just give you bytes strings in the stdout and stderr strings. Maybe at some later point you do know that they were text strings after all, and you know their encoding. Then, you can decode them.

```python
normal = subprocess.run([external, arg],
    stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    check=True,
    text=True)
print(normal.stdout)

convoluted = subprocess.run([external, arg],
    stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    check=True)

# You have to know (or guess) the encoding

print(convoluted.stdout.decode('utf-8'))
```

Python 3.7 introduced the shorter and more descriptive and understandable alias text for the keyword argument which was previously somewhat misleadingly called `universal_newlines`.

### Understand shell=True vs shell=False

With `shell=True` you pass a single string to your shell, and the shell takes it from there.

With `shell=False` you pass a list of arguments to the OS, bypassing the shell.

When you don't have a shell, you save a process and get rid of a fairly substantial amount of hidden complexity, which may or may not harbor bugs or even security problems.

On the other hand, when you don't have a shell, you don't have redirection, wildcard expansion, job control, and a large number of other shell features.

A common mistake is to use shell=True and then still pass Python a list of tokens, or vice versa. This happens to work in some cases, but is really ill-defined and could break in interesting ways.

```python
# XXX AVOID THIS BUG
buggy = subprocess.run('dig +short stackoverflow.com')

# XXX AVOID THIS BUG TOO
broken = subprocess.run(['dig', '+short', 'stackoverflow.com'],
    shell=True)

# XXX DEFINITELY AVOID THIS
pathological = subprocess.run(['dig +short stackoverflow.com'],
    shell=True)

correct = subprocess.run(['dig', '+short', 'stackoverflow.com'],
    # Probably don't forget these, too
    check=True, text=True)

# XXX Probably better avoid shell=True
# but this is nominally correct
fixed_but_fugly = subprocess.run('dig +short stackoverflow.com',
    shell=True,
    # Probably don't forget these, too
    check=True, text=True)
```

The common retort "but it works for me" is not a useful rebuttal unless you understand exactly under what circumstances it could stop working.

#### Refactoring Example

Very often, the features of the shell can be replaced with native Python code. Simple Awk or sed scripts should probably simply be translated to Python instead.

To partially illustrate this, here is a typical but slightly silly example which involves many shell features.

```python
cmd = '''while read -r x;
   do ping -c 3 "$x" | grep 'round-trip min/avg/max'
   done <hosts.txt'''

# Trivial but horrible
results = subprocess.run(
    cmd, shell=True, universal_newlines=True, check=True)
print(results.stdout)

# Reimplement with shell=False
with open('hosts.txt') as hosts:
    for host in hosts:
        host = host.rstrip('\n')  # drop newline
        ping = subprocess.run(
             ['ping', '-c', '3', host],
             text=True,
             stdout=subprocess.PIPE,
             check=True)
        for line in ping.stdout.split('\n'):
             if 'round-trip min/avg/max' in line:
                 print('{}: {}'.format(host, line))
```

Some things to note here:

- With `shell=False` you don't need the quoting that the shell requires around strings. Putting quotes anyway is probably an error.
- It often makes sense to run as little code as possible in a subprocess. This gives you more control over execution from within your Python code.
- Having said that, complex shell pipelines are tedious and sometimes challenging to reimplement in Python.

The refactored code also illustrates just how much the shell really does for you with a very terse syntax -- for better or for worse. Python says explicit is better than implicit but the Python code is rather verbose and arguably looks more complex than this really is. On the other hand, it offers a number of points where you can grab control in the middle of something else, as trivially exemplified by the enhancement that we can easily include the host name along with the shell command output. (This is by no means challenging to do in the shell, either, but at the expense of yet another diversion and perhaps another process.)

#### Common Shell Constructs

For completeness, here are brief explanations of some of these shell features, and some notes on how they can perhaps be replaced with native Python facilities.

-Globbing aka wildcard expansion can be replaced with `glob.glob()` or very often with simple Python string comparisons like `for file in : if not file.endswith('.png'): continue`. Bash has various other expansion facilities like `.{png,jpg}` brace expansion and `{1..100}` as well as tilde expansion (~ expands to your home directory, and more generally ~account to the home directory of another user)

- Shell variables like `$SHELL` or `$my_exported_var` can sometimes simply be replaced with Python variables. Exported shell variables are available as e.g. `os.environ['SHELL']` (the meaning of `export` is to make the variable available to subprocesses -- a variable which is not available to subprocesses will obviously not be available to Python running as a subprocess of the shell, or vice versa. The `env=` keyword argument to subprocess methods allows you to define the environment of the subprocess as a dictionary, so that's one way to make a Python variable visible to a subprocess). With `shell=False` you will need to understand how to remove any quotes; for example, cd `"$HOME"` is equivalent to `os.chdir(os.environ['HOME'])` without quotes around the directory name. (Very often cd is not useful or necessary anyway, and many beginners omit the double quotes around the variable and get away with it until one day ...)
- Redirection allows you to read from a file as your standard input, and write your standard output to a file. `grep 'foo' <inputfile >outputfile` opens `outputfile` for writing and `inputfile` for reading, and passes its contents as standard input to `grep`, whose standard output then lands in outputfile. This is not generally hard to replace with native Python code.
- Pipelines are a form of redirection. `echo foo | nl` runs two subprocesses, where the standard output of echo is the standard input of nl (on the OS level, in Unix-like systems, this is a single file handle). If you cannot replace one or both ends of the pipeline with native Python code, perhaps think about using a shell after all, especially if the pipeline has more than two or three processes (though look at the pipes module in the Python standard library or a number of more modern and versatile third-party competitors).
- Job control lets you interrupt jobs, run them in the background, return them to the foreground, etc. The basic Unix signals to stop and continue a process are of course available from Python, too. But jobs are a higher-level abstraction in the shell which involve process groups etc which you have to understand if you want to do something like this from Python.
- Quoting in the shell is potentially confusing until you understand that everything is basically a string. So `ls -l /` is equivalent to '`ls' '-l' '/'` but the quoting around literals is completely optional. Unquoted strings which contain shell metacharacters undergo parameter expansion, whitespace tokenization and wildcard expansion; double quotes prevent whitespace tokenization and wildcard expansion but allow parameter expansions (variable substitution, command substitution, and backslash processing). This is simple in theory but can get bewildering, especially when there are several layers of interpretation (a remote shell command, for example).

### Understand differences between sh and Bash

subprocess runs your shell commands with `/bin/sh` unless you specifically request otherwise (except of course on Windows, where it uses the value of the `COMSPEC` variable). This means that various Bash-only features like arrays, `[[` etc are not available.

If you need to use Bash-only syntax, you can pass in the path to the shell as `executable='/bin/bash'` (where of course if your Bash is installed somewhere else, you need to adjust the path).

```python
subprocess.run('''
    # This for loop syntax is Bash only
    for((i=1;i<=$#;i++)); do
        # Arrays are Bash-only
        array[i]+=123
    done''',
    shell=True, check=True,
    executable='/bin/bash')
```

### A subprocess is separate from its parent, and cannot change it

A somewhat common mistake is doing something like

`subprocess.run('cd /tmp', shell=True)`
`subprocess.run('pwd', shell=True)  # Oops, doesn't print /tmp`

The same thing will happen if the first subprocess tries to set an environment variable, which of course will have disappeared when you run another subprocess, etc.

A child process runs completely separate from Python, and when it finishes, Python has no idea what it did (apart from the vague indicators that it can infer from the exit status and output from the child process). A child generally cannot change the parent's environment; it cannot set a variable, change the working directory, or, in so many words, communicate with its parent without cooperation from the parent.

The immediate fix in this particular case is to run both commands in a single subprocess;

```python
subprocess.run('cd /tmp; pwd', shell=True)
```

though obviously this particular use case isn't very useful; instead, use the cwd keyword argument, or simply os.chdir() before running the subprocess. Similarly, for setting a variable, you can manipulate the environment of the current process (and thus also its children) via

```python
os.environ['foo'] = 'bar'
```

or pass an environment setting to a child process with

```python
subprocess.run('echo "$foo"', shell=True, env={'foo': 'bar'})
```

(not to mention the obvious refactoring `subprocess.run(['echo', 'bar'])`; but echo is a poor example of something to run in a subprocess in the first place, of course).

### Don't run Python from Python

This is slightly dubious advice; there are certainly situations where it does make sense or is even an absolute requirement to run the Python interpreter as a subprocess from a Python script. But very frequently, the correct approach is simply to import the other Python module into your calling script and call its functions directly.

If the other Python script is under your control, and it isn't a module, consider turning it into one. (This answer is too long already so I will not delve into details here.)

If you need parallelism, you can run Python functions in subprocesses with the multiprocessing module. There is also threading which runs multiple tasks in a single process (which is more lightweight and gives you more control, but also more constrained in that threads within a process are tightly coupled, and bound to a single GIL.)
