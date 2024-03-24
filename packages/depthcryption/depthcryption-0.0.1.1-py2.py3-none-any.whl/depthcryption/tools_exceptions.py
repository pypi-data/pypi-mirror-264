"""
The DepthCryption.tools_exceptions  module houses all the program
exceptions and is responsible for arranging their calls within the
program. All DepthCryption exceptions are inherited from the
ProgramException class. Their exact behaviours and intentions
are described within the current docstring below.

The following classes and functions are publicly available:
--------------
ProgramException: Exception parent class for entire package.

The following classes and functions are internally available to the program:
--------------
InternalException: Developer caused issue.
UserException: User caused issue.
EncryptionException: Encountered when attempting Encryption incorrectly.
DecryptionException: Encountered when attempting Decryption incorrectly.
InterpreterException: Encountered when using an unsupported python version.

"""


class ProgramException(Exception):
    """
    Base exception class for whole DepthCryption package.
    """

    def __init__(self,
                 *args: str,
                 ) -> None:
        # Call the base class constructor with the parameters it needs
        super().__init__('(DepthCryption): ' + ', '.join(args))
        self._args = args

    def __call__(self,
                 ) -> None:
        raise Exception(f'{self.__class__.__name__}: {self._args}')


class InternalException(ProgramException):
    """
    Exception class for if something malfunctions inside the source code,
    due to a developer issue.
    """

    pass


class UserException(ProgramException):
    """
    Exception class for if something malfunctions inside the source code,
    due to a user issue
    """

    pass


class EncryptionException(ProgramException):
    """
    Exception class for malfunctions when user is trying to encrypt,
    cause could be originating from both users and developers.
    """

    pass


class DecryptionException(ProgramException):
    """
    Exception class for malfunctions when user is trying to decrypt,
    cause could be originating from both users and developers.
    """

    pass


class InterpreterException(ProgramException):
    """
    Exception class for when user is not using a supported interpreter.
    """

    pass

# eof
