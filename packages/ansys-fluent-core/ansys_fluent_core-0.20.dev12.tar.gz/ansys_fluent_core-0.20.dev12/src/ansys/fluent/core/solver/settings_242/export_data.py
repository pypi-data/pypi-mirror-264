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

from .filename_7 import filename as filename_cls
class export_data(Command):
    """
    Export training data to file.
    
    Parameters
    ----------
        filename : str
            Training data file name.
    
    """

    fluent_name = "export-data"

    argument_names = \
        ['filename']

    _child_classes = dict(
        filename=filename_cls,
    )

