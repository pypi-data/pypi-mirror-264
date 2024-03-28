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

from .conditions_2 import conditions as conditions_cls
class add(Command):
    """
    Add conditions from compound condition.
    
    Parameters
    ----------
        conditions : typing.List[str]
            Conditions to add to compound condition. Order of input/clicking matters.
    
    """

    fluent_name = "add"

    argument_names = \
        ['conditions']

    _child_classes = dict(
        conditions=conditions_cls,
    )

