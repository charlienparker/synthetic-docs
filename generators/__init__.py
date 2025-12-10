"""
Document generators package
"""

from .w2.generator import W2Generator
from .paystub.generator import PaystubGenerator
from .other.generator import OtherGenerator

__all__ = ['W2Generator', 'PaystubGenerator', 'OtherGenerator']