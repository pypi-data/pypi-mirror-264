"""
Python bindings for the XAD comprehensive library for automatic differentiation
"""
from __future__ import annotations
from xad_autodiff._xad_autodiff import adj_1st
from xad_autodiff._xad_autodiff import fwd_1st
from . import _xad_autodiff
__all__: list = ['value', 'derivative']
def derivative(x: typing.Union[xad_autodiff._xad_autodiff.adj_1st.Real, xad_autodiff._xad_autodiff.fwd_1st.Real]) -> float:
    """
    Get the derivative of an XAD active type - forward or adjoint mode
    
        Args:
            x (Real): Argument to extract the derivative information from
    
        Returns:
            float: The derivative
        
    """
def value(x: typing.Union[xad_autodiff._xad_autodiff.adj_1st.Real, xad_autodiff._xad_autodiff.fwd_1st.Real, typing.Any]) -> float:
    """
    Get the value of an XAD active type - or return the value itself otherwise
    
        Args:
            x (Real | any): Argument to get the value of
    
        Returns:
            float: The value stored in the variable
        
    """
