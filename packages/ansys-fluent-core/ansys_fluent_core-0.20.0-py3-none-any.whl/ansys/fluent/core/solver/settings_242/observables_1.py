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

from .selection_2 import selection as selection_cls
from .evaluation import evaluation as evaluation_cls
class observables(Group):
    """
    Optimizer observables.
    """

    fluent_name = "observables"

    child_names = \
        ['selection', 'evaluation']

    _child_classes = dict(
        selection=selection_cls,
        evaluation=evaluation_cls,
    )

