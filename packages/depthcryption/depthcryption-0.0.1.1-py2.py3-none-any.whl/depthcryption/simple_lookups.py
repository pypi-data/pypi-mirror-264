"""
The DepthCryption.simple_lookups module houses the calling
structure to the precompiled package code. It is responsible
for matching the current interpreter's version to that which
will work correctly with the precompiled module. Once the
respective code is imported into this module the simple lookup
functions and classes are made available to the rest of the
program.

"""
# standard
import sys

# local
from . import tools_exceptions as te

# extract runtime python version
_pyv = f'{sys.version_info.major}.{sys.version_info.minor}'

# import functions from simple lookups selector directory based on version
if _pyv == '3.9':
    from depthcryption.sls.simple_lookups_39 import *
elif _pyv == '3.10':
    from depthcryption.sls.simple_lookups_310 import *
elif _pyv == '3.11':
    from depthcryption.sls.simple_lookups_311 import *
elif _pyv == '3.12':
    from depthcryption.sls.simple_lookups_312 import *
# raise error if version is not currently supported
else:
    raise te.InterpreterException(f'DepthCryption is only supported on '
                                  f'python versions 3.9 - 3.12, '
                                  f'current python version is {_pyv}. '
                                  f'Please use a different python '
                                  f'interpreter.')

# eof
