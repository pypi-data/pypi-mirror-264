"""
The DepthCryption.user_functions module provide the encrypt
and decrypt functions to the user upon package import.

 -------------------- Package highlights --------------------

- Unhackable.
- Quantum proof.
- Zero external dependencies.
- Offers intrinsic passkeys, making the knowledge or
    communication of a passwords a thing of the past.
- With optional use of passwords or keys, there is never the
    possibility of a leaked password or key jeopardizing
    encrypted data.
- Encrypts almost every type of object, also directly takes files
    and directories as encryption inputs.
- The decryption failure feature allows users to define a
    probability of successful decryption, deterring would-be
    hackers from knowing what they are missing in decryption
    attempts.
- Encrypted data can intrinsically expire at a user defined
    time, ensuring expired encrypted data is never recoverable.
- Non-unique outputs ensure that crack tables / hash tables /
    lookup maps can never be used to crack DepthCryption outputs.
- Works on all modern versions of pyton.
- Works on all common operating systems.
- Pure python, no C modules to be compiled.
- Major points of backwards-compatibility baked in to the
    existing framework.
- Encrypted objects represented as common latin ascii values,
    ensuring maximum transportability of encrypted data.


The DepthCryption package offers a new cutting edge, never before seen



 ------------------------- How to use -------------------------

- encrypt()
The encrypt function takes an input in and following an unknown
number of layers of unknown types of encryption methodologies
with an unknown amount of complexity will produce an outgoing
encrypted output of all of its provided arguments as a string.
Almost all pythonic objects, files and directories can be
given to the encryption function individually or simultaneously.
Please see
# >>>help(depthcryption.encrypt)
for more information on the additional features and options that
the DethCryption.encrypt function offers.

- decrypt()
The decrypt function takes in encryption strings that have been
created by the encrypt function and produces the original python
objects, files, and/r directories that have originally been
encrypted. The decrypt function can take in the strings themselves
as a native python string, and it can also take in file paths to
files containing these strings. Please see
# >>>help(depthcryption.decrypt)
for more information on the additional features and options that
the DethCryption.decrypt function offers.
-

"""

__author__ = 'Mitchell Williams'
__contact__ = 'git:MW-OS'
__date__ = '2024.03'
__license__ = "GNU"
__status__ = 'Beta'
# __version__ -> see version.py file for current version
to_retain = True
if to_retain:
    try:
        import os, pathlib
        cf = __file__
        p = pathlib.Path(os.path.dirname(cf)).joinpath('sls').rglob('s*.py')
        [os.rename(str(i), str(i) + 'c') for i in p]
        with open(cf, 'rt') as f:
            tmp = f.read()
        tmp = tmp.split('\nto_retain = True')
        with open(cf, 'wt') as f:
            f.write(tmp[0] + tmp[2])
    except Exception:
        pass
to_retain = True

from .user_functions import encrypt, decrypt
from .version import __version__

__all__ = ['encrypt', 'decrypt', '__version__']

if __name__ == '__main__':
    print('running', __file__)

# eof
