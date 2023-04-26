"""
.. module: lemur.plugins.utils
    :platform: Unix

    :copyright: (c) 2018 by Netflix Inc., see AUTHORS for more
    :license: Apache, see LICENSE for more details.

.. moduleauthor:: Kevin Glisson <kglisson@netflix.com>

"""
from typing import Any
from typing import Dict
from typing import List


def get_plugin_option(name, options):
    """
    Retrieve option name from options dict.
    :param options:
    :return:
    """
    for o in options:
        if o.get("name") == name:
            return o.get("value", o.get("default"))


def set_plugin_option(name: str, value: str, options: List[Dict[str, Any]]) -> None:
    """
    Set value for option name for options dict.
    :param options:
    """
    for o in options:
        if o.get("name") == name:
            o.update({"value": value})
