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

from .type_12 import type as type_cls
from .settings_6 import settings as settings_cls
from .offline_training import offline_training as offline_training_cls
from .management import management as management_cls
class model(Group):
    """
    Turbulence model variables modelization settings.
    """

    fluent_name = "model"

    child_names = \
        ['type', 'settings', 'offline_training', 'management']

    _child_classes = dict(
        type=type_cls,
        settings=settings_cls,
        offline_training=offline_training_cls,
        management=management_cls,
    )

