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

from .conditions_3 import conditions as conditions_cls
class delete(CommandWithPositionalArgs):
    """
    Delete conditions from compound condition.
    
    Parameters
    ----------
        conditions : typing.List[str]
            Conditions to be deleted from compound condition.
    
    """

    fluent_name = "delete"

    argument_names = \
        ['conditions']

    _child_classes = dict(
        conditions=conditions_cls,
    )

