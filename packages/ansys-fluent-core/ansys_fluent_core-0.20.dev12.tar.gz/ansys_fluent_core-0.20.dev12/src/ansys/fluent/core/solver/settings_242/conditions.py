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

from .x_7 import x as x_cls
from .y_7 import y as y_cls
from .z_7 import z as z_cls
from .theta_1 import theta as theta_cls
from .radial_1 import radial as radial_cls
from .axial import axial as axial_cls
from .boundary_continuity import boundary_continuity as boundary_continuity_cls
class conditions(Group):
    """
    Region conditions.
    """

    fluent_name = "conditions"

    child_names = \
        ['x', 'y', 'z', 'theta', 'radial', 'axial', 'boundary_continuity']

    _child_classes = dict(
        x=x_cls,
        y=y_cls,
        z=z_cls,
        theta=theta_cls,
        radial=radial_cls,
        axial=axial_cls,
        boundary_continuity=boundary_continuity_cls,
    )

