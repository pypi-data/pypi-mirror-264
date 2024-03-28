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

from .method_18 import method as method_cls
from .layers import layers as layers_cls
from .distance_2 import distance as distance_cls
from .applied_moving_conditions import applied_moving_conditions as applied_moving_conditions_cls
from .update_2 import update as update_cls
from .display_9 import display as display_cls
class fix_surfaces(Group):
    """
    Fix surfaces in the morphing region and away from applied moving conditions.
    """

    fluent_name = "fix-surfaces"

    child_names = \
        ['method', 'layers', 'distance', 'applied_moving_conditions']

    command_names = \
        ['update', 'display']

    _child_classes = dict(
        method=method_cls,
        layers=layers_cls,
        distance=distance_cls,
        applied_moving_conditions=applied_moving_conditions_cls,
        update=update_cls,
        display=display_cls,
    )

