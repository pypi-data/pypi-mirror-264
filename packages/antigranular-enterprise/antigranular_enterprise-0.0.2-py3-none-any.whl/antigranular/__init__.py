"""
Antigranular client package
"""


from .client import login
from .client import read_config
from .client import write_config

# Package version dunder
__version__ = "0.0.2"

# Package author dunder
__author__ = "Oblivious Software Pvt. Ltd."

# Package * imports dunder
__all__ = ["login", "read_config", "write_config", "__version__", "__author__"]

"""
Raise an error if client in loaded in a non-Jupyter environment.
"""
from IPython.core.getipython import get_ipython

ipython = get_ipython()
if ipython is None:
    raise ValueError(
        "Please ensure antigranuler is loaded in a valid Jupyter environment."
    )
