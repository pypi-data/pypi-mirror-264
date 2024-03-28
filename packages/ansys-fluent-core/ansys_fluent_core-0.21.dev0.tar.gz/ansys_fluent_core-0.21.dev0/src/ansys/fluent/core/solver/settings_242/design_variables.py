#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import (
    _ChildNamedObjectAccessorMixin,
    _CreatableNamedObjectMixin,
    _NonCreatableNamedObjectMixin,
    _HasAllowedValuesMixin,
    _InputFile,
    _OutputFile,
    _InOutFile,
)

from .variables_1 import variables as variables_cls
from .model_4 import model as model_cls
from .default_7 import default as default_cls
from .unhook_model import unhook_model as unhook_model_cls
class design_variables(Group):
    """
    Model management menu.
    """

    fluent_name = "design-variables"

    child_names = \
        ['variables', 'model']

    command_names = \
        ['default', 'unhook_model']

    _child_classes = dict(
        variables=variables_cls,
        model=model_cls,
        default=default_cls,
        unhook_model=unhook_model_cls,
    )

