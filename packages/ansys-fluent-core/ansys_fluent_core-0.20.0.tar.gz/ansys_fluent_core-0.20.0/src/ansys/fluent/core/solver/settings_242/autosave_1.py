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

from .filename_9 import filename as filename_cls
from .save_files import save_files as save_files_cls
from .save_optimal import save_optimal as save_optimal_cls
from .export_stl_1 import export_stl as export_stl_cls
class autosave(Group):
    """
    Optimizer reporting menu.
    """

    fluent_name = "autosave"

    child_names = \
        ['filename', 'save_files', 'save_optimal', 'export_stl']

    _child_classes = dict(
        filename=filename_cls,
        save_files=save_files_cls,
        save_optimal=save_optimal_cls,
        export_stl=export_stl_cls,
    )

