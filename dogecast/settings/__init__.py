"""
Settings module for Jaguar Social TV. Imports the appropriate level of settings into the app
"""
# Ignore "import all" warnings
#pylint: disable=W0401
import os

ENVIRONMENT = os.getenv("DOGECAST_ENVIRONMENT")

if ENVIRONMENT == "live":
    from .live import *
elif ENVIRONMENT == "staging":
    from .staging import *
else:
    try:
        from .local import *
    except ImportError:
        pass
