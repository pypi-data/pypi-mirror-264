"""
The DepthCryption.version file only contains current program version
information for public and internal program access, historical release
information contained in below in existing docstring. Format for
versioning is as follows:

A.B.C.D ->

A = Major versioning, this is only progressed when package changes
    are entirely non-backwards-compatible.

B = Minor versioning, this is only progressed when the package
    undergoes significant changes that may impact previous code
    that utilizes DepthCryption OR may impact previously encrypted
    objects during future decryption of those objects.

C = Micro versioning, this is only progressed when the package
    receives features, updates, and bug fixes that do not impact
    the code usage and are known/understood to not cause any
    backwards-compatibility issues.

D = Internal Micro versioning, this is only progressed for package
    developers and will be reset to zero (and +1 in A, B, or C)
    when the staged package changes are publicly released.

Release 0.0.1.0 in 2024.03:
    First program public beta release.

The following variables are publicly available:
--------------
__version__: current built of DepthCryption
__date__: release date of this build

"""

# current information
__version__ = '0.0.1.0'
__date__ = '2024.03'

# eof
