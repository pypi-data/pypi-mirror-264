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

from .filename_8 import filename as filename_cls
class export_model(Command):
    """
    Write the model setting and coefficient to a file.
    
    Parameters
    ----------
        filename : str
            Model data file name.
    
    """

    fluent_name = "export-model"

    argument_names = \
        ['filename']

    _child_classes = dict(
        filename=filename_cls,
    )

