"""
This file contains all the necessary root information, utilities, classes
to ensure the operation of each filter.
"""

from routes.processors import CommandProcessor
from data import DataBase
from utils import (
    Informer,
    Converter
)


informer = Informer()
database = DataBase()
converter = Converter()
com_processor = CommandProcessor()
