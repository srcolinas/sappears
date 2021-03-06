import inspect
import importlib
import os
import sys
from collections import namedtuple

import fire
from prettytable import PrettyTable


_BULITIN_MODULE_NAMES = set(sys.builtin_module_names)
_COLUMN_NAMES = ["namespace", "type", "location", "ocurrences"]
_SearchResult = namedtuple("SearchResult", _COLUMN_NAMES)


def make_report(results, ignore_zero_ocurrences=True):
    """Take a list of search results and prints them in a nice formated table."""
    table = PrettyTable()
    table.junction_char = "|"
    table.field_names = _COLUMN_NAMES
    for r in results:
        if ignore_zero_ocurrences and r.ocurrences == 0:
            continue
        table.add_row(r)
    print(table)


def list_all_modules(root):
    """List all submodules of the provided root.

    This function scans the whole hierarchical structure of the provided root.

    Args:
        root (module): The module for which you want a list of submodules.

    Returns:
        list: submodules of root.

    """
    queue = []

    def f(root):
        for _, child in list_modules(root):
            dirname_root = os.path.dirname(root.__file__)
            if child.__name__ not in _BULITIN_MODULE_NAMES:
                dirname_child = os.path.dirname(child.__file__)
                if dirname_root in dirname_child:
                    c = f(child)
                    queue.append(c)
        return root

    f(root)
    return queue


def list_modules(root):
    """List submodules of a module.

    This function does not scan the whole hierarchical structure, just the modules
    imported by the provided root. See `list_all_modules`.

    Args:
        root (module): The module for which you want a list of submodules.

    Returns:
        list: submodules of root.

    """
    return inspect.getmembers(root, lambda x: inspect.ismodule(x))


def search_in_module(string, package):
    """Inspect the package for the given string.

    Args:
        string : str
            Name to look for in the package. E.g. `read_csv`.
        package : module
            Package in which to search for the given query.
    Returns:
        list : a series of InspectionResult objects.

    """
    results = []
    for module in list_all_modules(package):
        _append_search_result(results, string, module, module)
    return results


def _append_search_result(results, string, obj, module):
    try:
        sourcecode = inspect.getsource(obj)
    except OSError:
        sourcecode = ""
    ocurrences = sourcecode.count(string)
    results.append(
        _SearchResult(
            obj.__name__, type(module), _get_module_relative_path(module), ocurrences
        )
    )


def _get_module_relative_path(module):
    main_package_name = module.__package__.split(".")[0]
    index_in_file = module.__file__.find(main_package_name)
    return module.__file__[index_in_file:]


def _main(string, package):
    """Search string in package.

    Args:
        string (str): string of interest.
        package (module): module or package for which to search for string occurences.

    """
    package = importlib.import_module(package)
    results = search_in_module(string, package)
    make_report(results)


if __name__ == "__main__":
    fire.Fire(_main)
