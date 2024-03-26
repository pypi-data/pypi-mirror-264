dramatic
========

[![PyPI - Version](https://img.shields.io/pypi/v/dramatic.svg?label=PyPI)](https://pypi.org/project/dramatic/)
[![License](https://img.shields.io/pypi/l/dramatic?label=License)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/treyhunner/dramatic/actions/workflows/test.yml/badge.svg "Tests")](https://github.com/treyhunner/dramatic/actions?workflow=test)
[![Codecov](https://codecov.io/gh/treyhunner/dramatic/graph/badge.svg?token=e2Ah1TKt3g&label=Codecov "Coverage")](https://codecov.io/gh/treyhunner/dramatic)

The `dramatic` module includes utilities to cause all text output to display character-by-character (it prints *dramatically*).

**Note**: This project is based on a [Python Morsels](https://www.pythonmorsels.com) exercise.
If you're working on that exercise right now, please don't look at the source code for this! 😉

<a href="https://www.pythonmorsels.com">
    <img src="https://raw.githubusercontent.com/treyhunner/dramatic/main/screenshots/python-morsels-logo.png" alt="an adorable snake taking a bite out of a cookie with the words Python Morsels next to it (Python Morsels logo)" width="250">
</a>


![dramatic printing within a terminal](https://raw.githubusercontent.com/treyhunner/dramatic/main/screenshots/repl.gif)


Usage
-----

The `dramatic` module is available on [PyPI][].
You can install it with `pip`:

```bash
$ python3 -m pip install dramatic
```

There are four primary ways to use the utilities in the `dramatic` module:

1. As a context manager that temporarily makes output display dramatically
2. As a decorator that temporarily makes output display dramatically
3. Using a `dramatic.start()` function that makes output display dramatically
4. Using a `dramatic.print` function to display specific text dramatically


Dramatic Context Manager
------------------------

The `dramatic.output` [context manager][] will temporarily cause all standard output and standard error to display dramatically:

```python
import dramatic

def main():
    print("This function prints")

with dramatic.output:
    main()
```

To change the printing speed from the default of 75 characters per second to another value (30 characters per second in this case) use the `at_speed` method:


```python
import dramatic

def main():
    print("This function prints")

with dramatic.output.at_speed(30):
    main()
```

Example context manager usage:

![dramatic.output context manager demo](https://raw.githubusercontent.com/treyhunner/dramatic/main/screenshots/context.gif)


Dramatic Decorator
------------------

The `dramatic.output` [decorator][] will cause all standard output and standard error to display dramatically while the decorated function is running:

```python
import dramatic

@dramatic.output
def main():
    print("This function prints")

main()
```

The `at_speed` method works as a decorator as well:


```python
import dramatic

@dramatic.output.at_speed(30)
def main():
    print("This function prints")

main()
```

Example decorator usage:

![dramatic.output decorator demo](https://raw.githubusercontent.com/treyhunner/dramatic/main/screenshots/decorator.gif)


Manually Starting and Stopping
------------------------------

Instead of enabling dramatic printing temporarily with a context manager or decorator, the `dramatic.start` function may be used to enable dramatic printing:

```python
import dramatic

def main():
    print("This function prints")

dramatic.start()
main()
```

The `speed` keyword argument may be used to change the printing speed (in characters per second):

```python
import dramatic

def main():
    print("This function prints")

dramatic.start(speed=30)
main()
```

To make *only* standard output dramatic (but not standard error) pass `stderr=False` to `start`:

```python
import dramatic

def main():
    print("This function prints")

dramatic.start(stderr=False)
main()
```

To disable dramatic printing, the `dramatic.stop` function may be used.
Here's an example [context manager][] that uses both `dramatic.start` and `dramatic.stop`:

```python
import dramatic


class CustomContextManager:
    def __enter__(self):
        print("Printing will become dramatic now")
        dramatic.start()
    def __exit__(self):
        dramatic.stop()
        print("Dramatic printing has stopped")
```

Example `start` and `stop` usage:

![dramatic.start decorator demo](https://raw.githubusercontent.com/treyhunner/dramatic/main/screenshots/start.gif)


Dramatic Print
--------------

The `dramatic.print` function acts just like the built-in `print` function, but it prints dramatically:

```python
import dramatic
dramatic.print("This will print some text dramatically")
```


Other Features
--------------

Pressing `Ctrl-C` while text is printing dramatically will cause the remaining text to print immediately.

To start a dramatic [Python REPL][]:

```bash
$ python3 -m dramatic
>>>
```

To dramatically run a Python module:

```bash
$ python3 -m dramatic -m this
```

To dramatically run a Python file:

```bash
$ python3 -m dramatic hello_world.py
```

The `dramatic` module also accepts a `--speed` argument to set the characters printed per second.
In this example we're increasing the speed from 75 characters-per-second to 120:

![dramatic module running demo](https://raw.githubusercontent.com/treyhunner/dramatic/main/screenshots/module.gif)


Dramatic By Default
-------------------

Want to make your Python interpreter dramatic *by default*?

Creating a Python startup file and setting [the `PYTHONSTARTUP` environment variable](https://docs.python.org/3/using/cmdline.html#envvar-PYTHONSTARTUP) to its filename will run some code each time the Python interpreter launches.
Add this code to your Python startup file to make your Python REPL dramatic by default:

```python
try:
    import dramatic, sys
    sys.__interactivehook__ = dramatic.start
    del dramatic, sys
except ImportError:
    pass
```

Want to make *every* Python program dramatic?
You'll need to make a `usercustomize.py` in your user site packages directory.
Find this directory with:

```bash
$ python -c "import site; print(site.getusersitepackages())"
```

And create a `usercustomize.py` file in that directory, with this in it:

```python
import dramatic, sys
dramatic.start()
del dramatic, sys
```

Note that the `dramatic` module will need to be installed *globally* for this to work.
To make Python dramatic within virtual environments you'll need to use a `sitecustomize.py` file in your virtual environments "site packages" directory instead.


Credits
-------

This package was inspired by [the **dramatic print** Python Morsels exercise][dramatic print], which was partially inspired by Brandon Rhodes' [adventure][] Python port (which displays its text at 1200 baud).


[pypi]: https://pypi.org/project/dramatic/
[context manager]: https://www.pythonmorsels.com/what-is-a-context-manager/
[decorator]: https://www.pythonmorsels.com/what-is-a-decorator/
[python repl]: https://www.pythonmorsels.com/using-the-python-repl/
[dramatic print]: https://www.pythonmorsels.com/exercises/57338fa2ecc342e3bad18afdbf12aacd/
[adventure]: https://pypi.org/project/adventure/
