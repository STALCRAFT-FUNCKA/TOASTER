"""
Initialization file for the local processors module
"""

from .command import CommandProcessor
from .reference import ReferenceProcessor
from .information import InformationProcessor
from .fun import FunProcessor

__all__ = (
    "CommandProcessor",
    "InformationProcessor",
    "ReferenceProcessor",
    "FunProcessor"
)
