"""
The DepthCryption.user_functions module houses the encryption function
(called encrypt) and the decryption function (called decrypt) that
users access from the DepthCryption package. This file also
houses the internal support classes for these functions, respectively
named __Encrypt and __Decrypt. The support classes connect the publicly
facing functions to the internal program architecture, while providing
data cleaning, data preparation, and data type checking before the data
reaches the internal code components.

The following classes and functions are publicly available:
--------------
encrypt: Main DepthCryption encryption function.
decrypt: Main DepthCryption decryption function.

The following classes and functions are private:
--------------
__Encrypt: Support class for encryption call.
__Decrypt: Support class for decryption call.

"""

__author__ = 'Mitchell Williams'
__contact__ = 'git:MW-OS'
__date__ = '2024.03'
__license__ = "GNU"
__status__ = 'Beta'
# __version__ -> see version.py file for current version

# standard
import datetime
import os
import pathlib
import pickle
import secrets
import ssl
import time
import typing
import urllib.request
import warnings

# local
from . import step_manager as sm
from . import tools_exceptions as te
from . import tools_utils as tu
warnings.formatwarning = lambda m, *a, **k: f'{m}\n'

# -------- Forward call --------


def encrypt(*args: object,
            **kwargs: object,
            ) -> str:
    """
    The DepthCryption encrypt function is the main encryption function API.


    ----------------------- example usage -----------------------

    >>> original_obj_ = ['test list', 1, {2}, 3.0]
    >>> encrypted_obj_ = encrypt(original_obj_)
    >>> print(f"Encrypting {original_obj_} has resulted in {encrypted_obj_}")


    ---------------------- long description ----------------------

    The encrypt function takes an input in and following an unknown
    number of layers of unknown types of encryption methodologies
    with an unknown amount of complexity will produce an outgoing
    encrypted output of all of its provided arguments as a string.
    Almost all pythonic objects, files and directories can be
    given to the encryption function individually or simultaneously.


    ---------------------- function inputs ----------------------

    --------- target encryption objects ---------

    :param args: Any number of objects to encrypt can be entered
        as positional arguments into the encrypt function.
        All inputs must either be pickleable OR file paths to
        either files or directories to encrypt. If an incoming
        argument is a pathlib object or a string, DepthCryption
        will check to see if that file or directory exists.
        If the string or pathlib object does exist then its
        contents are read into the program.

    :type args: object

    -------------- program features --------------

    :param compression: An optional integer/string ('lzma',
        'zip') keyword argument that specifies what compression
        technique DepthCryption uses to internally compress
        data.

    :type compression: str or int

    :param decryption_complexity: An optional integer/string
        ('low', 'medium', 'high', 'extreme') keyword argument
        that specifies how difficult it is for DepthCryption
        to evaluate this object for decryption. Higher values
        are more secure, but demand more resources at runtime.

    :type decryption_complexity: str or int

    :param encryption_complexity: An optional integer/string
        ('low', 'medium', 'high', 'extreme') keyword argument
        that specifies how "encrypted" a DepthCryption output
        is. Higher values are more secure, but demand more
        resources at runtime.

    :type encryption_complexity: str or int

    :param probability: An optional integer keyword argument
        input for the probability of successful decryption.
        If this is set to 2, there is a 1/2 probability that
        decryption will be successful each time it is attempted;
        if this is set to 7, there is a 1/7 probability that
        decryption will be successful each time it is attempted.

    :type probability: int

    :param save_file: An optional string or pathlib object
        keyword argument that specifies the file that the
        resulting encrypted data is saved to.

    :type save_file: str or pathlib.PurePath

    -------------- encryption keys --------------

    :param key_files: An optional string or a pathlib object
        keyword argument input (of either a directory or file)
         that will use the data of the specified files/file
         structure as an encryption key.

    :type key_files: str or pathlib.PurePath

    :param key_ip: An optional boolean keyword argument
        input that will use the public ip of this current device
        as an encryption key, only IPv4 supported at this time.
        --> NOTE: A public IP address may change over time,
        --> depending on: your internet provider, connecting device,
        --> vpn configurations, if your device has a dynamic IP
        --> setting, or any other number network
        --> settings/configurations.

    :type key_ip: bool

    :param key_os: An optional boolean keyword argument
        input that will use the operating system identifier of
        this current device as an encryption key.

    :type key_os: bool

    :param key_py: An optional boolean keyword argument
        input that will use the python version metadata of this
        current interpreter as an encryption key.

    :type key_py: bool

    :param key_time: An optional keyword argument input of
        when the encrypted object can no longer be decrypted,
        trying to decrypt an object after the time of
        expiry will cause failure. Can either be specified
        as a unix timestamp or as a list of local dates/times
        in [yyyy, MM, dd, hh, mm, ss] format,
        e.g. [2015, 10, 21, 7, 28, 0], or [1985, 10, 26],
        or [1955, 11], ect... Expiration occurs at the
        first millisecond after the specified key_time.

    :type key_time: float or int or list[int] or list[float] or
        list[int or float] or datetime.datetime

    :param key_url: An optional string or list
         keyword argument input (list containing url strings)
         that will scrape the data on provided website's page
         and us it as an encryption key.
         --> NOTE: Webpages can change at any time for any
         --> reason; even webpages that appear the same
         --> to the eye may have small changes in their data,
         --> metadata, or how that data is delivered, and this
         --> will cause decryption to fail in the case that
         --> the scraped data is not exactly identical.
         --> Use cautiously.

    :type key_url: str or list[str] or tuple[str] or set[str]

    :param user_key: An optional keyword argument input where
        the user can specify their own key or password for
        DepthCryption to use. All python objects are acceptable,
        so long as they are pickleable.
        --> NOTE: The user MUST provide this identical value
        --> again EVERY single time that this object is decrypted.
        --> If this value is not reproduced identically at the
        --> time of decryption, decryption cannot occur.

    :type user_key: object

    -------------------------- raises --------------------------

    :raises AssertionError: Strong type checking failure. One of
        the inputs (also described in the corresponding
        exception message) is not of the supported input types
        of the corresponding function input (also described in
        the exception message). Checking that the correct types
        of input(s) remediates this exception.

    :raises EncryptionException: User provided an input of the
        correct type, and that the program can access, but for
        various reasons (also described in the exception
        message) the program cannot pass along the user
        provided input. Reviewing the exception message to
        understand why the program cannot use the input can
        help remediate this exception.

    :raises InterpreterException: The current runtime interpreter
        is currently using a version of python that the package
        is not able to run from.

    :raises UserException: User provided an input of the correct
        type, but for various reasons (also described in the
        exception message) the program cannot access the
        provided input. Using the exception message to determine
        the access issue and its causes, this exception can be
        remediated.


    ------------------------- returns -------------------------

    :returns: An encrypted object as a string. If multiple objects
        are given to the encryption function positional arguements
        in a single functional call then they are all encrypted
        together and wholly represented in the outgoing string.
        Optionally saves an outgoing encrypted object if the
        save_file input is specified.

    :rtype: str

    """

    # verify that only the currently supported kwargs are entered
    _valid_kwargs = ('compression',
                     'decryption_complexity',
                     'encryption_complexity',
                     'save_file',
                     'key_os',
                     'key_ip',
                     'key_py',
                     'key_files',
                     'key_url',
                     'key_time',
                     'user_key',
                     'probability',
                     )

    # evaluate if there are any invalid kwargs
    _invalid_kwargs = list(filter(lambda x: x not in _valid_kwargs, kwargs))

    # notify of invalid kwargs to user
    assert not _invalid_kwargs, \
        (f'These provided keyword arguments are not supported '
         f'by the DepthCryption encrypt function at this time: \n'
         f'{", ".join(_invalid_kwargs)}\n'
         f'Please select from the currently supported keyword '
         f'arguments (all optional): \n{", ".join(_valid_kwargs)}')

    # verify args exist, raise to user if not
    assert args, \
        ('At least one input must be provided for encryption, '
         'in the DepthCryption encrypt function. \n'
         'More than one object may be provided at the same time, '
         'in which case they will be indexed in the respective '
         'ordered positions they are received.')

    # initialize the inputs
    base_encryption = __Encrypt(*args, **kwargs)

    # perform forward call and return results
    return base_encryption()

# -------- Backward call --------


def decrypt(*args: typing.Union[str, pathlib.PurePath],
            **kwargs: object,
            ) -> object:
    """
    The DepthCryption decrypt function is the main decryption function API.


    ----------------------- example usage -----------------------

    >>> original_obj_ = ['test list', 1, {2}, 3.0]
    >>> encrypted_obj_ = encrypt(original_obj_)
    >>> decrypted_obj_ = decrypt(encrypted_obj_)
    >>> print(f"Objects match: {original_obj_==decrypted_obj_}")


    ---------------------- long description ----------------------

    The decrypt function takes in encryption strings that have been
    created by the encrypt function and produces the original python
    objects, files, and/r directories that have originally been
    encrypted. The decrypt function can take in the strings themselves
    as a native python string, and it can also take in file paths to
    files containing these strings.


    ---------------------- function inputs ----------------------

    --------- target decryption objects ---------

    :param args: Any number of objects to decrypt can be entered
        as positional arguments into the decrypt function.
        All inputs must either be previously encrypted strings OR
        file paths that contain previously encrypted strings.
        If an incoming argument is a pathlib object or a string,
        DepthCryption will check to see if that file or directory
        exists. If the string or pathlib object does exist then its
        contents are read into the program.

    :type args: str or pathlib.PurePath

    -------------- program features --------------

    :param return_paths: An optional bool keyword argument that
        specifies if the file paths to the decrypted objects
        are also returned with the objects. If True, the paths
        will be returned in a separate list in the same
        respective order as the decrypted items.

    :type return_paths: Strings or path objects.

    :param save_dir: An optional string or pathlib object
        keyword argument that specifies where to save decrypted
        items. The specified directory must exist. If the
        decrypted object is a previously encrypted directory
        the directory will be placed into here. If the decrypted
        object is an encrypted object that was not an encrypted
        file or directory, it will be converted to a string with
        a unique file name created just for it.

    :type save_dir: str or pathlib.PurePath

    -------------- encryption keys --------------

    :param key_files: If the key_files key was used to encrypt
        data, but that path does not currently exist on the
        decrypting device then the provided path can be
        overwritten using key_files at the time of decryption.
        If only a single file was used when encrypting with
        key_files then that file must be placed alone into the
        updated key_files directory currently being used for
        decryption.

    :type key_files:  str or pathlib.PurePath

    :param user_key: An optional keyword argument input where
        the user can specify their own key or password for
        DepthCryption to use. If there was a user specified
        password/key object that was used to encrypt the
        current input it must be supplied here.

    :type user_key: object


    -------------------------- raises --------------------------

    :raises AssertionError: Strong type checking failure. One of
        the inputs (also described in the corresponding
        exception message) is not of the supported input types
        of the corresponding function input (also described in
        the exception message). Checking that the correct types
        of input(s) remediates this exception.

    :raises InterpreterException: The current runtime interpreter
        is currently using a version of python that the package
        is not able to run from.

    :raises DecryptionException: User provided an input of the
        correct type, and that the program can access, but for
        various reasons (also described in the exception
        message) the program cannot pass along the user
        provided input. Reviewing the exception message to
        understand why the program cannot use the input can
        help remediate this exception.

    :raises UserException: User provided an input of the correct
        type, but for various reasons (also described in the
        exception message) the program cannot access the
        provided input. Using the exception message to determine
        the access issue and its causes, this exception can be
        remediated.


    ------------------------- returns -------------------------

    :returns: The decrypted object(s). If return_paths is set
        to True, the associated file paths are also returned
        if the decrypted object(s) are written to disk. Objects
        that were encrypted directly from files are automatically
        written back out to their original locations or where
        ever is specified in the save_dir variable. If neither
        of these are viable DepthCryption attempts to make a new
        folder on the desktop and save the respective files there

    :rtype: object or list[object] or object and list[str] or
        list[object] and list[str]

    """

    # verify that only the currently supported kwargs are entered
    _valid_kwargs = ('save_dir',
                     'return_paths',
                     'key_files',
                     'user_key',
                     )
    # evaluate if there are any invalid kwargs
    _invalid_kwargs = list(filter(lambda x: x not in _valid_kwargs, kwargs))
    # notify of invalid kwargs to user
    assert not _invalid_kwargs, \
        (f'These provided keyword arguments are not supported '
         f'by the DepthCryption decrypt function at this time: \n'
         f'{", ".join(_invalid_kwargs)}\n'
         f'Please select from the currently supported keyword '
         f'arguments (all optional): \n{", ".join(_valid_kwargs)}')

    # verify args exist
    assert args, \
        ('At least one input must be provided for decryption, '
         'in the DepthCryption decrypt function. \n'
         'More than one object may be provided at the same time, '
         'in which case they will be indexed in the respective '
         'ordered positions they are received.')

    if len(args) == 1:
        # for a single incoming object to decrypt
        return __Decrypt(*args, **kwargs)()
    else:
        # for a multiple incoming objects to decrypt
        return list(map(lambda x: __Decrypt(x, **kwargs)(), args))

# ---------------- Internal APIs ----------------

# -------- Base Class --------


class __BaseCrypt:
    """
    Base class for __Encrypt and __Decrypt, houses common methods, can be
    extended in the future as features/specifications grow.

    Public Methods
    --------------
    None

    Public Attributes
    --------------
    None

    """
    __slots__ = ()

    def _validate(self,
                  key_in: str,
                  type_in: typing.Union[type, tuple]
                  ) -> bool:
        """
        The _validate method enforces strong type checking of user inputs.

        :param key_in: The kwarg key to validate.
        :param type_in: The allowable types for the provided kwarg.
        :returns: True if present and passes, False if absent.
            An exception is raised if present and fails.

        """

        # return True if present and correct type,
        # return False if not present,
        # raise exception if present and type match fail
        if key_in in self._kwargs.keys():

            assert isinstance(self._kwargs[key_in], type_in), \
                (f'{key_in} was provided as an DepthCryption '
                 f'input, but it must be of type {str(type_in)}. '
                 f'However, the provided argument is of type '
                 f'{type(self._kwargs[key_in])} for provided '
                 f'input: \n{self._kwargs[key_in]}')

            return True

        else:
            return False

# -------- Forward Class --------


class __Encrypt(__BaseCrypt):
    """
    The DepthCryption encrypt function internal __Encrypt class acts as
    an internal API caller for the publicly available encrypt function to
    connect with the internal package functioning. This class also performs
    both strong type checking and validating of incoming values, and
    raises appropriate exceptions if these are violated.

    Public Methods
    --------------
    __call__: Calling on an instance performs a full forward call,
        that is amenable to all user feature requests.

    Public Attributes
    --------------
    None

    """

    __slots__ = ('_args',
                 '_kwargs',
                 'internal_kwargs')

    def __init__(self,
                 *args: object,
                 **kwargs: typing.Union[object, int, str, float, bool]
                 ) -> None:

        # receive inputs if any inputs that are handed into the instance
        self._args = args
        self._kwargs = kwargs

        # prepare inputs, keys, and parameters, for running
        self._prepare_args()
        self.internal_kwargs = self._prepare_kwargs()

    def __call__(self
                 ) -> str:
        """
        Run the forward API and return results, save results if specified.

        :returns: An encrypted object string.

        """

        # perform forward call
        self._args = (
            sm.StepManagerForward(
                obj_=self._args,
                keys_dict=self.internal_kwargs[0],
                direction=True,
                **self.internal_kwargs[1])())

        # save file, if specified
        if self._validate('save_file', str):
            tu.write_out_file(
                self._kwargs["save_file"],
                str(self._args))

        # return the encrypted object string
        return str(self._args)

    def _prepare_args(self
                      ) -> None:
        """
        Internal method to prepare and validate incoming encryption objects.

        """

        # initiate the list of rejected objects that cannot be
        # encrypted, and the outgoing list that is fed into the
        # internal program calls
        rejected_objects = []
        outgoing_objects = []

        # loop through all objects and evaluate them by pickling and
        # converting that output to a string
        for i in self._args:
            try:
                # see if object is valid path,
                # files are loaded into a specific data structure to
                # avoid confusion when decrypting. The paths and binary
                # data is stored in dict keys and values respectively,
                # this dict is placed into a nested tuple with a set
                # which only contains an identifying string.
                if (isinstance(i, (str, pathlib.PurePath))
                        and os.path.exists(i)):
                    # if object is directory, load in
                    if os.path.isdir(i):
                        _filedir = tu.read_in_directory(i)
                    # else it is a file
                    elif os.path.isfile(i):
                        _filedir = {i: tu.read_in_file(i)}
                    else:
                        raise te.UserException(
                            f'File object can not be determined for: '
                            f'{str(i)}. Please review this path to '
                            f'ensure that it is a recognizable file or '
                            f'directory.')
                    # attempt to append filedir object in
                    outgoing_objects.append(
                        {'filedir_path': pickle.dumps(_filedir)})
                # if it is an object as it is, just do it
                else:
                    outgoing_objects.append(pickle.dumps(i))
            # append failed objects to rejected_objects list
            except pickle.PickleError:
                rejected_objects.append(i)

        # raise Exception with the rejected values, or return
        # outgoing values if there are no rejected values
        if rejected_objects:
            rejected_str = str(
                '\n\n'.join(str(i) + '\n- of type ' + str(type(i))
                            for i in rejected_objects))
            raise te.EncryptionException(
                f"Only objects that can be pickled can be encrypted. "
                f"The following objects were given to encrypt, but"
                f"cannot be pickled: \n {rejected_str} \n"
                f"Please verify that incoming objects for encryption"
                f"can be pickled and try again.")

        # if there are no rejected objects then return all as
        # just a single byte object
        self._args = pickle.dumps(outgoing_objects)

    def _prepare_kwargs(self
                        ) -> typing.List[typing.Dict[str, object]]:
        """
        Internal method to prepare and validate incoming encryption kwargs.

        """

        # init the incoming keys and parameters dicts
        _keys = {}
        _parameters = {}

        # -- initialize the _keys dict first --
        # operating system id hand off
        if self._validate('key_os', bool) and self._kwargs['key_os']:
            _keys['key_os_id'] = self._kwargs['key_os']

        # public ip address hand off
        if self._validate('key_ip', bool) and self._kwargs['key_ip']:
            _keys['key_public_ip'] = self._kwargs['key_ip']

        # python version hand off
        if self._validate('key_py', bool) and self._kwargs['key_py']:
            _keys['key_python_version'] = self._kwargs['key_py']

        # files/directory hand off
        if self._validate('key_files', str):
            if os.path.exists(self._kwargs['key_files']):
                _keys['key_filedir'] = self._kwargs['key_files']
            else:
                raise te.UserException(
                    f'The following path was provided to the key_files '
                    f'argument but it does not exist: '
                    f'{self._kwargs["key_files"]}\n'
                    f'In either case where this is a file or directory, '
                    f'it must exist and the current user must have read '
                    f'access to the file/directory.')

        # url hand off
        if self._validate('key_url', (str, list, tuple, set)):
            # since there are so many permutations of acceptable urls
            # with constantly evolving standards this can just naturally
            # fail if it is not a currently valid url
            if isinstance(self._kwargs['key_url'], str):
                self._kwargs['key_url'] = [self._kwargs['key_url']]
            # check that the urls respond before running
            _url_errors = []
            ssl._create_default_https_context = (
                ssl._create_unverified_context)
            for i in self._kwargs['key_url']:
                try:
                    urllib.request.urlopen(i)
                except Exception as e:
                    _url_errors += [
                        f'DepthCryption could not establish a '
                        f'connection to --> {i} <-- \n Please '
                        f'review the following error message '
                        f'for more information: \n{e}']
            if _url_errors:
                _all_errors = " \n".join(_url_errors)
                raise te.UserException(
                    f'Issue connecting to the provided url(s): \n'
                    f'{_all_errors}')

            _keys['key_url_request'] = list(self._kwargs['key_url'])

        # timing hand off
        if self._validate('key_time',
                          (list, tuple, datetime.datetime)):
            _keys['key_timing'] = self._kwargs['key_time']

        # user key/pass hand off
        if self._validate('user_key', object):
            try:
                _keys['key_custom'] = pickle.dumps(self._kwargs['user_key'])
            except Exception as e:
                raise te.EncryptionException(
                    f'The user_key variable must be pickleable, but '
                    f'the following errors were encountered when '
                    f'pickling was attempted: \n{e}')

        # probability hand off/establishment
        if self._validate('probability', int):
            if 1 <= self._kwargs['probability'] <= 614124:
                _keys['key_default'] = self._kwargs['probability']
                # inform user that failure is expected if over 1
                if self._kwargs['probability'] > 1:
                    warnings.warn(
                        f"\nProbability is not set to 1, user set "
                        f"to -> {self._kwargs['probability']} \n"
                        f"To have a 99% chance of a successful "
                        f"decryption, decryption must be attempted "
                        f"{tu.ex_prob(self._kwargs['probability'], 0.99)} "
                        f"times. \nTo have a 99.99% chance of a successful "
                        f"decryption, decryption must be attempted "
                        f"{tu.ex_prob(self._kwargs['probability'], 0.9999)}"
                        f" times. \n"
                        f" - Program continues on from this notification "
                        f"- ",
                        UserWarning,
                        stacklevel=2)
            else:
                raise te.UserException(
                    f'The probability argument must be a number '
                    f'between 1 and 614124. The provided probability '
                    f'number is {self._kwargs["probability"]}.')

        # if probability is not provided then initialize it to 1
        else:
            _keys['key_default'] = 1

        # -- initialize the _parameters dict next --
        # compression hand off/establishment
        if self._validate('compression', (str, int)):
            if self._kwargs['compression'] in (0, 'lzma'):
                _parameters['compression'] = 0
            elif self._kwargs['compression'] in (1, 'zip'):
                _parameters['compression'] = 1
            else:
                raise te.UserException(
                    f'The compression argument currently only '
                    f'supports "lzma" and "zip" as valid arguments '
                    f'but was provided with '
                    f'{self._kwargs["compression"]}.')
        # if compression is not in kwargs then set it to 1
        else:
            _parameters['compression'] = 1

        # thread count hand off/establishment
        if self._validate('thread_count', int):
            if 1 <= self._kwargs['thread_count'] <= 1:
                _parameters['thread_count'] = self._kwargs['thread_count']
            else:
                raise te.UserException(
                    f'The thread_count argument must be a number '
                    f'between 1 and 1. The provided thread_count '
                    f'number is {self._kwargs["thread_count"]}.')
        # if thread_count is not in kwargs then set it to 1
        else:
            _parameters['thread_count'] = 1

        # decryption_complexity hand off/establishment
        if self._validate('decryption_complexity', (int, str)):
            if isinstance(self._kwargs["decryption_complexity"], int):
                if 1 <= self._kwargs['decryption_complexity'] <= 10:
                    _parameters['decryption_complexity'] = \
                        self._kwargs['decryption_complexity']
                else:
                    raise te.UserException(
                        f'The decryption_complexity argument must '
                        f'be a number between 1 and 10. The provided '
                        f'decryption_complexity number is '
                        f'{self._kwargs["decryption_complexity"]}.')

            # else it is of string type
            else:
                if self._kwargs['decryption_complexity'] == 'low':
                    _parameters['decryption_complexity'] = 2

                elif self._kwargs['decryption_complexity'] == 'medium':
                    _parameters['decryption_complexity'] = \
                        4 + secrets.randbelow(2)

                elif self._kwargs['decryption_complexity'] == 'high':
                    _parameters['decryption_complexity'] = \
                        6 + secrets.randbelow(4)

                elif self._kwargs['decryption_complexity'] == 'extreme':
                    _parameters['decryption_complexity'] = \
                        10 + secrets.randbelow(5)
                # if not strings match
                else:
                    raise te.UserException(
                        f'The decryption_complexity argument '
                        f'currently only supports "low", "medium", '
                        f'"high", and "extreme" as valid arguments '
                        f'but was provided with '
                        f'{self._kwargs["decryption_complexity"]}.')

        # if decryption_complexity is not in kwargs then set it to 'low'
        else:
            _parameters['decryption_complexity'] = 2

        # encryption_complexity hand off/establishment
        if self._validate('encryption_complexity', (int, str)):

            # count the existing keys, each needs at least one depth
            key_count = len(_keys.keys())

            # limit upper bound to 1e3
            if isinstance(self._kwargs["encryption_complexity"], int):
                if key_count < self._kwargs['encryption_complexity'] <= 1e3:
                    _parameters['depth'] = \
                        int(self._kwargs['encryption_complexity'])
                else:
                    raise te.UserException(
                        f'The encryption_complexity argument must be a '
                        f'number between {key_count} and 1000. '
                        f'However, the provided encryption_complexity '
                        f'number is '
                        f'{self._kwargs["encryption_complexity"]}.')

            # else it is of string type
            else:
                if self._kwargs['encryption_complexity'] == 'low':
                    _parameters['depth'] = \
                        key_count + 5**0 + secrets.randbelow(3)

                elif self._kwargs['encryption_complexity'] == 'medium':
                    _parameters['depth'] = \
                        key_count + 5**1 + secrets.randbelow(6)

                elif self._kwargs['encryption_complexity'] == 'high':
                    _parameters['depth'] = \
                        key_count + 5**2 + secrets.randbelow(12)

                elif self._kwargs['encryption_complexity'] == 'extreme':
                    _parameters['depth'] = \
                        key_count + 5**3 + secrets.randbelow(24)

                # if no string match
                else:
                    raise te.UserException(
                        f'The encryption_complexity argument '
                        f'currently only supports "low", "medium", '
                        f'"high", and "extreme" as valid arguments '
                        f'but was provided with '
                        f'{self._kwargs["encryption_complexity"]}.')
        # if encryption_complexity is not in kwargs then set it to 'low'
        else:
            _parameters['depth'] = (len(_keys.keys()) +
                                    1 +
                                    secrets.randbelow(3))

        # try writing to the desired save file, to ensure that this
        # file is writable before running any encryption operations
        if self._validate('save_file', (str, pathlib.PurePath)):
            try:
                tu.write_out_file(self._kwargs["save_file"], '\n')
            # inform user if there is a problem writing to the
            # specified file
            except Exception as e:
                raise te.UserException(
                    f'The save_file argument contains a file'
                    f'that is currently having issues being written '
                    f'to. For the provided path '
                    f'{self._kwargs["save_file"]}; please review '
                    f'the following error and try again: \n'
                    f'{e}')

        # set arranged program dicts
        return [_keys, _parameters]

# -------- Backward Class --------


class __Decrypt(__BaseCrypt):
    """
    The DepthCryption decrypt function internal __Decrypt class acts as
    an internal API caller for the publicly available encrypt function to
    connect with the internal package functioning. This class also performs
    both strong type checking and validating of incoming values, and raises
    appropriate exceptions if these are violated.

    """

    __slots__ = ('obj_',
                 '_kwargs',
                 'internal_kwargs')

    def __init__(self,
                 obj_: typing.Union[str, pathlib.PurePath],
                 **kwargs: typing.Union[object, int, str, float, bool]
                 ) -> None:

        # receive inputs if any inputs that are handed into the instance
        self.obj_ = obj_
        self._kwargs = kwargs

        # prepare inputs, keys, and parameters, for running
        self._prepare_obj()
        self.internal_kwargs = self._prepare_kwargs()

    def __call__(self
                 ) -> typing.Union[object, tuple[object, list]]:
        """
        Run backward API and return results, save results if specified.

        :returns: A decrypted object.

        """

        # perform backward call
        self.obj_ = sm.StepManagerBackward(
            obj_=self.obj_,
            direction=False,
            **self.internal_kwargs[0])()

        # process the backward call outputs into their initial objects
        paths_out = self._prepare_outputs()

        # if only a single element is returned then pop it from list
        if len(self.obj_) == 1:
            self.obj_ = self.obj_[0]

        # return the decrypted object(s)
        # return_paths returns the save locations of the decrypted
        # objects along with the decrypted objects themselves
        if ('return_paths' in self.internal_kwargs[1].keys() and
                self.internal_kwargs[1]['return_paths'] is True):
            return self.obj_, paths_out
        # only return the decrypted objects
        else:
            return self.obj_

    def _prepare_obj(self
                     ) -> None:
        """
        Internal method to prepare and validate incoming decryption object.

        """

        # check that incoming thing is a string or a pathlib object
        # check if string or pathlib is an existing file.
        # check if something looks like a file type string
        if not isinstance(self.obj_, (str, pathlib.PurePath)):
            # this will catch if it was not entered
            raise te.UserException(
                f'The decryption_object argument must either be a valid '
                f'string, string filepath, or pathlib file path.')
        # read in provided filepath if it is a file
        if os.path.isfile(self.obj_):
            self.obj_ = tu.read_in_file(self.obj_, is_str=True)

    def _prepare_kwargs(self
                        ) -> typing.List[typing.Dict[str, object]]:
        """
        Internal method to prepare and validate incoming decryption kwargs.

        """

        # init the incoming keys and parameters dicts
        _keys = {}
        _parameters = {}

        # hand off of saving file location
        if self._validate('save_dir', (str, pathlib.PurePath)):
            if not os.path.isdir(self._kwargs['save_dir']):
                raise te.UserException(
                    f'save_dir must be an existing directory, the '
                    f'following directory was provided but cannot be '
                    f'found: \n{self._kwargs["save_dir"]}')
            _parameters['save_dir'] = self._kwargs['save_dir']

        # hand off of the return_paths bool
        if self._validate('return_paths', bool):
            _parameters['return_paths'] = self._kwargs['return_paths']

        # hand off of the user key/pass
        if self._validate('user_key', object):
            try:
                _keys['key_custom'] = (
                    pickle.dumps(self._kwargs['user_key']))
            except Exception as e:
                raise te.DecryptionException(
                    f'The user_key variable must be pickleable, but '
                    f'the following errors were encountered when '
                    f'pickling was attempted: \n{e}')

        # hand off of updated key_files path, must exist
        if self._validate('key_files', (str, pathlib.PurePath)):
            if not os.path.isdir(self._kwargs['key_files']):
                raise te.UserException(
                    f'key_files must be an existing directory, the '
                    f'following directory was provided but cannot be '
                    f'found: \n{self._kwargs["key_files"]}')
            _keys['key_path_update'] = self._kwargs['key_files']

        return [_keys, _parameters]

    def _prepare_outputs(self
                         ) -> list:
        """
        Internal method to prepare decrypted object(s) that have gone
        through the programs internal decryption actions.

        """

        # perform initial unpickling
        self.obj_ = pickle.loads(self.obj_)

        # init a list of decrypted objects saved filepaths
        _paths_out = []

        # loop through all outputs
        for i in enumerate(self.obj_):
            # check if a decrypted object is to be written directly
            if (isinstance(i[1], dict) and
                len(i[1].keys()) == 1 and
                    'filedir_path' in i[1].keys()):
                # unpickle outer dict
                self.obj_[i[0]] = pickle.loads(i[1]['filedir_path'])

                # remove the longest common path (_lcp) when handing off
                if len(list(self.obj_[i[0]].keys())) > 1:
                    # if there is more than one path
                    _lcp = os.path.commonpath(self.obj_[i[0]].keys())
                else:
                    # else if there is only one path then
                    # _lcp is entire path
                    _lcp = os.path.split(list(
                        self.obj_[i[0]].keys()
                    )[0])[0]

                # unpickle objects and unpack them into dict where
                # the key is the path without the _lcp
                self.obj_[i[0]] = {k: v for k, v in zip(
                    [j.replace(_lcp, '')
                     for j in self.obj_[i[0]].keys()],
                    list(self.obj_[i[0]].values()))}

                # establish directory to write files into
                if 'save_dir' in self._kwargs:
                    # if the user provided a directory to save into
                    _save_dir = self.internal_kwargs[1]['save_dir']
                elif os.path.exists(os.path.commonpath(
                        self.obj_[i[0]].keys()
                )):
                    # else see if the paths that the objects were saved
                    # with exists in current system
                    _save_dir = ''.join(_lcp)
                else:
                    # if no provided path and existing path does not exist,
                    # try to find the Desktop, else the Home dir, else pwd
                    _save_dir = str(self._search_for_desktop())

                # sleep for 2 microseconds to ensure that there is a
                # unique folder name
                time.sleep(2e-6)
                # create unique directory for outputs
                _save_dir += \
                    f'/DepthCryption_decrypted_{tu.get_ts_formatted()}/'

                # go about writing the contents to their files
                for j in self.obj_[i[0]].items():
                    # path to save current file
                    _save_file = _save_dir + j[0]
                    # create directory hierarchy if needed
                    pathlib.Path(
                        os.path.split(_save_file)[0]
                    ).mkdir(mode=0o777, parents=True, exist_ok=True)
                    tu.write_out_file(_save_file, j[1])
                    # alert user of a saved file and append the location
                    # of the saved file to the outgoing paths
                    print(f'DepthCryption: decrypted file saved: \n'
                          f'{_save_file}\n')
                    _paths_out += [_save_file]

            # see if objects are desired to be saved now, but
            # were not specified to be when encrypted
            elif 'save_dir' in self._kwargs:
                # initial unpickling
                self.obj_[i[0]] = pickle.loads(i[1])
                # establish new path;
                # sleep for 2 microseconds to ensure that there is a
                # unique file name
                time.sleep(2e-6)
                _save_file = (f'{self._kwargs["save_dir"]}/'
                              f'DepthCryption_decrypted_'
                              f'{tu.get_ts_formatted()}.txt')
                tu.write_out_file(_save_file, str(self.obj_[i[0]]))
                # alert user of a saved file and append the location
                # of the saved file to the outgoing paths
                print(f'DepthCryption: decrypted file saved: {_save_file}')
                _paths_out += [_save_file]

            # else no saving, just pure hand off
            else:
                self.obj_[i[0]] = pickle.loads(i[1])

        # return the outgoing paths where objects were saved, if any
        return _paths_out

    @staticmethod
    def _search_for_desktop() -> typing.Union[str, pathlib.PurePath]:
        """
        Find a valid directory to save files to.

        The _search_for_desktop method searches for the
        path to a users desktop, if no desktop can be found the
        user's home directory is returned, if the home directory
        cannot be found the current working directory is returned.
        This method is only invoked if files are request to be saved
        but the directory to save them to cannot readily be
        established.

        :returns: A valid directory path.

        """

        # initiate the home directory str
        home_dir = ''

        # establish the function calls that will be attempted to find home
        home_search_func = [
            lambda: pathlib.Path.home(),
            lambda: os.path.expanduser("~"),
            lambda: os.environ['HOMEDRIVE'] + os.environ['HOMEPATH'],
            lambda: os.environ['HOME']]

        # try looping through all of them
        for i in home_search_func:
            # if home_dir is an empty string continue trying
            if not home_dir:
                # try next function
                try:
                    home_dir = i()
                except:
                    pass
            # if home_dir is established then exit the loop
            else:
                break

        # if the home directory is found then pathlib it
        if home_dir:
            home_dir = pathlib.Path(home_dir).resolve()
        # if none of the functions return home dir then return pwd
        else:
            return pathlib.Path().resolve()

        # now that the home directory is found try to locate the desktop,
        # establish names of desktops in a few languages
        desktop_languages = {'en/de': 'desktop',
                             'es': 'escritorio',
                             'fr': 'bureau',
                             'zh': '桌面',
                             'ar': 'سطح المكتب',
                             'ru': 'Рабочий стол',
                             'pt': 'Área de Trabalho'}

        # lowercase desktop values for matching
        _l_desktop = [i.lower() for i in desktop_languages.values()]

        # look for desktop in multiple languages, wherever home is
        desktop_list = list(filter(
            lambda x: x.lower() in _l_desktop,
            os.listdir(home_dir)))

        # if any results came up then return the desktop path
        if desktop_list:
            # get the first one
            return home_dir.joinpath(desktop_list[0])
        # else return home dir
        else:
            return home_dir

#
# if __name__ == '__main__':
#     print('running', __file__)
#     # additional unit/integration/systems tests can be initiated below.

# eof
