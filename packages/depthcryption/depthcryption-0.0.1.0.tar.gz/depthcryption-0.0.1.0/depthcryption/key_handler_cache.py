"""
The Depthcryption.key_handler_cache module houses the required
approaches for handling user specified and user provided keys. This
module is responsible for orchestrating how the entire program
handles and caches all the user provided and specified keys for
both encryption (whose operations are housed in the internally
available KeyHandlerForward class) and encryption (whose
operations are housed in the internally available
KeyHandlerBackward class). Having these internal class for key
handling ensures that all encryption and decryption keys are
centralized in a single location for the whole program to
access. The Caching of the user specified and provided keys allows
the program to only retrieve them a single time and then reuse
them when they occur again. This is especially beneficial if the
retrieval of these keys takes a long time to achieve (I.E.
retrieving webpage data for a key 100 times, with a slow
internet connection). There is currently little to no distinction
between the KeyHandlerForward and KeyHandlerBackward classes,
they are currently implemented separately for future development.

The following classes and functions are publicly available:
--------------
None

The following classes and functions are internally available to the program:
--------------
KeyHandlerForward: Key handling and caching for encryption calls.
KeyHandlerBackward: Key handling and caching for decryption calls.

The following classes and functions are private:
--------------
KeyHandlerBase: Base key handler and key cache class.

"""

import typing

# local
from . import tools_exceptions as te


class KeyHandlerBase:
    """
    Handles the intake and distribution of encryption and decryption keys.

    Public Methods
    --------------
    __call__: Calling on an instance deploys a desired key.
    set_all_keys: Initializes the program_keys dict with provided values.
    key_get: Retrieves specified key.
    key_hhasher: Overwrite current hashing approach.

    Public Attributes
    --------------
    program_keys: A dict of known cryption keys.

    """

    __slots__ = ("program_keys",
                 'retriever',
                 "key_hhasher",
                 "direction",
                 "_args",
                 "_kwargs")

    def __init__(self,
                 *args: typing.Union[int, float, list, str,],
                 retriever=None,
                 direction=None,
                 key_hhasher=None,
                 **kwargs: typing.Union[bool, int, float, str,],
                 ) -> None:

        # receive inputs if any inputs that are handed into the instance
        self._args = args
        self._kwargs = kwargs
        self.retriever = retriever
        self.direction = direction
        self.key_hhasher = key_hhasher
        self.program_keys = {}

        # initiate the KeyHandler with the keys provided at the outset
        if None not in [key_hhasher, retriever, direction]:
            self.set_all_keys(**kwargs)

    def __call__(self,
                 *args: typing.Union[int, float, list, str,],
                 **kwargs: typing.Union[int, float, list, str,],
                 ) -> typing.Union[int, float, list, str,]:
        """
        Calling on the instance deploys a key.

        :param args: Values required for hand off to set/get functions.
        :param kwargs: Keyword match values for key discovery.
        :returns: An existing key.
        """

        return self.key_get(*args, **kwargs)

    def set_all_keys(self,
                     **kwargs: typing.Union[int, float, list, str,],
                     ) -> None:
        """
        Full intake of all keys that the user has specified.

        :param kwargs: Keyword match values to set as keys.
        """

        # attempt to set each of the keys individually
        for i in kwargs.items():
            self.key_set(i[1],
                         direction=self.direction,
                         get_item='func',
                         key_id=i[0])

        # collect all the exceptions that were raised during setting
        exception_list = list(filter(
            lambda x: isinstance(x, te.ProgramException),
            self.program_keys.values()))

        # notify user of all exceptions that occurred with their keys
        if len(exception_list) > 0:
            if len(exception_list) == 1:
                raise exception_list[0]
            else:
                # convert list of exceptions to one big string
                exception_list_str = (
                    '\n\n'.join(
                        str(i[0]+1) + ': \n' + i[1].args[0]
                        for i in enumerate(exception_list)))
                exception_str = (f'Multiple exceptions have occurred: \n'
                                 f'{exception_list_str}')
                # notify user of all key setting problems
                raise te.UserException('\n\n' + exception_str)

    def key_set(self,
                *args: typing.Union[int, float, list, str,],
                **kwargs: typing.Union[int, float, list, str,],
                ) -> typing.Union[int, float, list, str,]:
        """
        Reads in a single source key and inputs it into program_keys dict.

        :param args: Values required for hand off to internal setters.
        :param kwargs: Keyword match values for key discovery.
        :returns: A newly existing key.
        """

        # get base function and invoke a key
        base_f = self.retriever('k', **kwargs)(**kwargs)
        key_in = base_f(*args)
        # do not hhash errors
        if isinstance(key_in, te.ProgramException):
            self.program_keys[kwargs['key_id']] = key_in
        else:
            self.program_keys[kwargs['key_id']] = self.key_hhasher(key_in)

        # return the object as well, so it can be used as it is
        return self.program_keys[kwargs['key_id']]

    def key_get(self,
                *args: typing.Union[int, float, list, str,],
                **kwargs: typing.Union[int, float, list, str,],
                ) -> typing.Union[int, float, list, str,]:
        """
        Reads in a single source key and inputs it into program_keys dict.

        :param args: Values required for hand off to internal setters.
        :param kwargs: Keyword match values for key discovery.
        :returns: A newly existing key.
        """

        # attempt to get an existing key or set it if it doesn't already exist
        if kwargs['key_id'] in self.program_keys.keys():
            return self.program_keys[kwargs['key_id']]
        else:
            return self.key_set(*args, **kwargs)


class KeyHandlerForward(KeyHandlerBase):
    """
    Forward call of key handling for encryption keys.

    Public Methods
    --------------
    __call__: Calling on an instance deploys a desired key.
    set_all_keys: Initializes the program_keys dict with provided values.
    key_get: Retrieves specified key.
    key_hhasher: Overwrite current hashing approach.

    Public Attributes
    --------------
    program_keys: A dict of known cryption keys.

    """

    __slots__ = ("program_keys",
                 'retriever',
                 "key_hhasher",
                 "_args",
                 "_kwargs")

    def __init__(self,
                 *args: object,
                 retriever=None,
                 key_hhasher=None,
                 **kwargs: typing.Union[bool, int, float, str, object,],
                 ) -> None:

        # receive inputs if any inputs that are handed into the instance
        super().__init__(*args,
                         retriever=retriever,
                         key_hhasher=key_hhasher,
                         **kwargs)


class KeyHandlerBackward(KeyHandlerBase):
    """
    Backward call of key handling for decryption keys.

    Public Methods
    --------------
    __call__: Calling on an instance deploys a desired key.
    set_all_keys: Initializes the program_keys dict with provided values.
    key_get: Retrieves specified key.
    key_hhasher: Overwrite current hashing approach.

    Public Attributes
    --------------
    program_keys: A dict of known cryption keys.

    """

    __slots__ = ("program_keys",
                 'retriever',
                 "key_hhasher",
                 "_args",
                 "_kwargs")

    def __init__(self,
                 *args: object,
                 retriever=None,
                 key_hhasher=None,
                 **kwargs: typing.Union[bool, int, float, str, object,],
                 ) -> None:

        # receive inputs if any inputs that are handed into the instance
        super().__init__(*args,
                         retriever=retriever,
                         key_hhasher=key_hhasher,
                         **kwargs)

# eof
