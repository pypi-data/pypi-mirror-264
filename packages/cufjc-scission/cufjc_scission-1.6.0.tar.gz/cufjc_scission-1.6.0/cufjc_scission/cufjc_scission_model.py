"""The module for the cuFJC single chain scission model."""

# Import external modules
from __future__ import division

# Import internal modules
from .rate_dependence_scission import (
    RateIndependentScission, RateDependentScission
)
from .scission_model import AnalyticalScissioncuFJC


class RateIndependentScissioncuFJC(
        RateIndependentScission, AnalyticalScissioncuFJC):
    """The cuFJC single chain model class with rate-independent
    stochastic scission.
    
    This class is a representation of the cuFJC single chain model with
    rate-independent stochastic scission; an instance of this class is a
    cuFJC single chain model instance with rate-independent stochastic
    scission. It inherits all attributes and methods from the
    ``RateIndependentScission`` class. It also inherits all attributes
    and methods from the ``AnalyticalScissioncuFJC`` class, which
    inherits all attributes and methods from the ``cuFJC`` class.
    """
    def __init__(self, **kwargs):
        """
        Initializes the ``RateIndependentScissioncuFJC`` class,
        producing a cuFJC single chain model instance with
        rate-independent stochastic scission.
        
        Initialize and inherit all attributes and methods from the
        ``RateIndependentScission`` class instance and the
        ``AnalyticalScissioncuFJC`` class instance.
        """
        RateIndependentScission.__init__(self)
        AnalyticalScissioncuFJC.__init__(self, **kwargs)


class RateDependentScissioncuFJC(
        RateDependentScission, AnalyticalScissioncuFJC):
    """The cuFJC single chain model class with rate-dependent
    stochastic scission.
    
    This class is a representation of the cuFJC single chain model with
    rate-dependent stochastic scission; an instance of this class is a
    cuFJC single chain model instance with rate-dependent stochastic
    scission. It also inherits all attributes and methods from the
    ``RateDependentScission`` class. It also inherits all attributes and
    methods from the ``AnalyticalScissioncuFJC`` class, which inherits
    all attributes and methods from the ``cuFJC`` class.
    """
    def __init__(self, **kwargs):
        """
        Initializes the ``RateDependentScissioncuFJC`` class, producing
        a cuFJC single chain model instance with rate-dependent
        stochastic scission.
        
        Initialize and inherit all attributes and methods from the
        ``RateDependentScission`` class instance and the
        ``AnalyticalScissioncuFJC`` class instance.
        """
        RateDependentScission.__init__(self, **kwargs)
        AnalyticalScissioncuFJC.__init__(self, **kwargs)