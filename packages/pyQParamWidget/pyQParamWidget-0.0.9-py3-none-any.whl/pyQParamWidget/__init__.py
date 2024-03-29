"""pyQParamWidget package"""

__package__ = "pyQParamWidget"

from .param_editor import *  # noqa
from .param_item import *  # noqa
from .param_tree import *  # noqa
from .qpw_widgets import *  # noqa

try:
    from setuptools_scm import get_version

    __version__ = get_version(root="..", relative_to=__file__)
    del get_version
except (LookupError, ModuleNotFoundError):
    from importlib.metadata import version

    __version__ = version(__package__)
    del version

# -----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2024, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
