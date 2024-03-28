"""
Data Preparation in Vantage with Views
============================
tdprepview (speak T-D-prep-view) is a package for fitting
and transforming re-usable data preparation pipelines that are
saved in view definitions. Hence, no other permanent database objects
are required.
"""

__author__ = """Martin Hillebrand"""
__email__ = 'martin.hillebrand@teradata.com'
__version__ = '1.3.2'

from .pipeline._pipeline import Pipeline
from .preprocessing import *
from . import preprocessing

__all__ = [
     'Pipeline'
] + preprocessing.__all__

