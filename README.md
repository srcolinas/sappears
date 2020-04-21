# sappears

This python library allows you to cound the ocurrences of a particular string python source files. This could used to estimate the effort of refactoring or changing a convention.

## Why we do this?

There are times when you need to refactore some modules or replace a convention used during the implementation of a particular functionality. Measuring the impact of such changes is sometimes time consuming as it may involve going through all modules, classes and functions of your package. 

## How it works?

The goal of this search process is to have a table as follows:

```
Ocurrences as of [name of interest]:

| namespace    | type     | location                     | ocurrences |
|--------------|----------|------------------------------|------------|
| module_one   | module   | package/module_1/__init__.py | 2          |
| ClassOne     | type     | package/module_1/ClassOne.py | 1          |
| function_one | function | package/module_1/__init__.py | 1          |
````

You can achieve that by runing:

```python
import mypackage # replace with the package you want to inspect.

import sappears

string = "import tensorflow as tf"

results = search_in_module(string, mypackage)
make_report(results)

```
where name of interest is the name of the variable, function, method, class or module you are interested in. Alternatively, you could just run it from the command line as follows:

`python -m sappears [string of interest] [mypacakge]`

## Contribute

Please feel free to add issues and make PRs!

### TODO

- Specify searches by type (function, class, module, docstring).
- Customize output (e.g. ignore location)
- Add tests