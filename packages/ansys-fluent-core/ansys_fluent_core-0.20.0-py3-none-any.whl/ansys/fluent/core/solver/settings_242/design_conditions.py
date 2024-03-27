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

from .definition_3 import definition as definition_cls
from .selection_1 import selection as selection_cls
class design_conditions(Group):
    """
    Design conditions menu.
    """

    fluent_name = "design-conditions"

    child_names = \
        ['definition', 'selection']

    _child_classes = dict(
        definition=definition_cls,
        selection=selection_cls,
    )

