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

from .update_design_varaibles import update_design_varaibles as update_design_varaibles_cls
class apply_trained_model(Command):
    """
    Adopt the trained neural network for the turbulence modeling.
    
    Parameters
    ----------
        update_design_varaibles : bool
            Update design varaibles using the neural network model after applying the trained model.
    
    """

    fluent_name = "apply-trained-model"

    argument_names = \
        ['update_design_varaibles']

    _child_classes = dict(
        update_design_varaibles=update_design_varaibles_cls,
    )

