"""
The DepthCryption.step_manager module houses the internal operations
to progress all encryption and decryption operations. At a high level
the contents of this file are responsible for all the internal
orchestrations needed to perform a beginning to end encryption (this
is internally referred to as a forward call) and to perform a beginning
to end decryption (this is internally referred to as a backward call).
The contents of this file are internally called from the
user_functions module.

The following classes and functions are publicly available:
--------------
None

The following classes and functions are internally available to the program:
--------------
StepManagerForward: Encryption orchestration.
StepManagerBackward: Decryption orchestration.

The following classes and functions are private:
--------------
StepManagerBase: Parent class of StepManagerForward and StepManagerBackward.

"""

# standard
import ast
import base64
import functools
import os
import pathlib
import secrets
import typing
import warnings
# local
# import simple lookups first for version checking
from . import simple_lookups as sl
from . import cryptors_cryptors as cc
from . import cryptors_tools as ct
from . import key_handler_cache as khc
from . import tools_exceptions as te
from . import tools_utils as tu
from .version import __version__ as _dcv
warnings.formatwarning = lambda m, *a, **k: f'\n{m}\n'


class StepManagerBase:
    """
    Step Manager Base class, if parental behavior is needs. Class
    currently houses joint methods for forwards and backwards cases,
    can be expanded flexibly if future use cases require.

    """

    __slots__ = ()

    @staticmethod
    def _get_demarker_bytes(_version: list[int,],
                            ) -> bytes:
        """
        Internal signaling of separation between elements.

        :param _version: Version of program that the marker refers to.
        :return: The marker bytes.
        """

        if (_version[0] == 0 and
            _version[1] == 0 and
                _version[2] == 1):
            marker = b''.join(bytes(
                chr(i if i % 2 == 0 else int(1.111e6) - i),
                'utf-8') for i in range(9))

        else:
            raise te.DecryptionException(
                 f'demarker specifications do not '
                 f'yet exist for specified version '
                 f'{".".join(str(i) for i in _version)}')

        return marker


class StepManagerForward(StepManagerBase):
    """
    The forward step manager takes in an incoming forward inputs with
    its instructions and organizes forward stepping through all the
    cryptors and keys.

    Public Methods
    --------------
    __call__: Calling on an instance performs a forward call.

    Public Attributes
    --------------
    None

    """


    __slots__ = ('obj_',
                 'step_plan',
                 '_args',
                 '_kwargs',
                 'key_handler',
                 'retriever')

    def __init__(self,
                 obj_: typing.Union[bytes, list[bytes,],],
                 keys_dict: dict[str,
                                 typing.Union[
                                     bool, int, float, list, object, str,],],
                 *args: typing.Union[bool, int, float, list, str,],
                 **kwargs: typing.Union[bool, int, float, list, str,],
                 ) -> None:

        # receive inputs if any inputs that are handed into the instance
        self.obj_ = obj_
        self._args = args
        self._kwargs = kwargs

        # establish key and cryptor handling mechanisms
        _hhash_init = sl.HashContainer(hc_set_hf=True)(**keys_dict, **kwargs)
        self.retriever = sl.StepAssignRetriever(direction=True)
        # init the key handler with existing retriever and hhash
        self.key_handler = khc.KeyHandlerForward(
            retriever=self.retriever,
            direction=True,
            key_hhasher=functools.partial(
                ct.hhash,
                hash_select=_hhash_init,
                mode='plain',
                layers=0),
            **keys_dict)

        # establish plan for forward stepping
        self.step_plan = self.forward_step_plan(keys_dict=keys_dict)
        self.step_plan['hhash_int'] = _hhash_init
        self.step_plan['thread_count'] = kwargs['thread_count']

    def __call__(self,
                 *args: typing.Union[bool, int, float, list, str,],
                 **kwargs: typing.Union[bool, int, float, list, str,],
                 ) -> typing.Union[bytes, list[bytes,],]:
        """
        Calling instance moves through all forward steps.

        :param args: Not consumed at this time, held for flexibility.
        :param kwargs: Not consumed at this time, held for flexibility.
        :return: An encrypted string.
        """
        self._forward_first_step()
        self._forward_middle_step()
        self._forward_final_step()
        return self.obj_

    # -------- ENCRYPTION --------

    def forward_step_plan(self,
                          keys_dict: dict[str, typing.Union[
                              dict, bool, int, float, list, str,],],
                          ) -> [
        str, any, typing.Union[
            list, int, bool, float, list, str,
            dict[str,
                 typing.Union[dict, bool, int, float, list, str,],
                 bytes,
                 any,],],]:

        """
        Planning all the steps for forward call, establishing metadata.

        :param keys_dict: User defined keys for the program to use.
        :return: Dict of runtime step plan metadata.
        """

        # load in user provided keys and all cryptors
        if not keys_dict:
            raise te.InternalException('keys_dict is missing from input, '
                                       'please select from available'
                                       'keys and rerun.')
        key_cryptor_zip = list(zip(
            tu.random_sample_full(list(self.key_handler.program_keys.keys()),
                                  self._kwargs['depth']),
            tu.random_sample(self.retriever('c', get_all_cryptors=True),
                             self._kwargs['depth'])
        ))

        # make a list of the additional keys data that may need to be
        # inserted into obj_, these should only be added to the final
        # call to these since they are filo. init with the key names
        key_parameters = list(list(zip(*key_cryptor_zip))[0])
        tmp_key_set = set()
        for i in range(self._kwargs['depth']-1, 0-1, -1):
            # loop backwards through key parameters,
            # if in set then set to None
            if key_parameters[i] in tmp_key_set:
                key_parameters[i] = None

            else:
                # put in set if it doesn't exist
                tmp_key_set.add(key_parameters[i])

                # handle key timing
                if key_parameters[i] == 'key_timing':
                    key_parameters[i] = (
                        sl.key_timing().key_timing_set(
                            keys_dict[key_parameters[i]]))

                # handle other insertion elements
                elif (key_parameters[i] != 'key_default' and
                      key_parameters[i] != 'key_custom' and
                      not isinstance(keys_dict[key_parameters[i]], bool)):
                    key_parameters[i] = keys_dict[key_parameters[i]]

                # key_default, key_custom, or of bool type --> None
                else:
                    key_parameters[i] = None

        # internally reestablish _decrypt_complexity if it is missing
        _decrypt_complexity = secrets.randbelow(10) if \
            ('decrypt_complexity' not in
             self._kwargs.keys() or not
             1 <= self._kwargs['decrypt_complexity'] <= 10) else (
            self._kwargs)['decrypt_complexity']
        # bump
        _decrypt_complexity += 2

        # return the zipped cryptor and key combos and other metadata
        return {'key_cryptor_zip': key_cryptor_zip,
                'byte_len_interior': 8,
                'byte_len_exterior': 0,
                'depth': self._kwargs['depth'],
                'decrypt_complexity': _decrypt_complexity,
                'version': int(_dcv.split('.')[0]),
                'subversion': int(_dcv.split('.')[1]),
                'subsubversion': int(_dcv.split('.')[2]),
                'keys_dict': keys_dict,
                'item_demarker': self._get_demarker_bytes(
                    [int(_dcv.split('.')[0]),
                     int(_dcv.split('.')[1]),
                     int(_dcv.split('.')[2])]),
                'key_parameters': key_parameters
                }

    def _forward_first_step(self,
                            ) -> None:
        """
        Performing all first forward stepping actions.

        :return: None.
        """

        # compress all the incoming objects
        # if there is more than one incoming object in args then
        # join it on a demarker
        if isinstance(self.obj_, bytes):
            self.obj_ = tu.pressor(self.obj_, **self._kwargs)
        else:
            self.obj_ = self.step_plan['item_demarker'].join(
                map(lambda x: (tu.pressor(x, **self._kwargs)), self.obj_))

        # compress elements into string
        self.obj_ = str(tu.pressor(self.obj_, **self._kwargs))

        # shuffle incoming object with the default key
        self.obj_ = cc.shuffle(str_in=self.obj_,
                               key_in=self.key_handler.program_keys[
                                   'key_default'],
                               direction=True)

        # starting nail
        self.obj_ += sl.get_nail(self.obj_,
                                 direction=True,
                                 **self.step_plan)

    def _forward_middle_step(self,
                             ) -> None:
        """
        Performing all middle forward stepping actions.

        :return: None.
        """

        # init the setter for simple instance lookups
        setter_ = sl.StepAssign(
            retriever=self.retriever,
            plan=self.step_plan)

        # move through middle steps
        for i in range(self.step_plan['depth']):
            # apply cryptor
            self.obj_ = self.step_plan['key_cryptor_zip'][i][1](
                str_in=self.obj_,
                key_in=self.key_handler.program_keys[
                    self.step_plan['key_cryptor_zip'][i][0]],
                direction=True,
                byte_len=self.step_plan['byte_len_interior'])

            # see if there are any key parameters to be included
            # adding static (item_demarker) and
            # dynamic points (-7) into demarker
            if self.step_plan['key_parameters'][i] is not None:
                self.obj_ += (str(self.step_plan['item_demarker'])[2:-1] +
                              self.obj_[-7:] +
                              str(self.step_plan['key_parameters'][i]))

            # call into setter with newly established metadata
            self.obj_ = setter_(
                self.obj_, direction=True,
                key_in=self.step_plan['key_cryptor_zip'][i][0],
                cryptor_in=self.step_plan['key_cryptor_zip'][i][1])

    def _forward_final_step(self,
                            ) -> None:
        """
        Performing all final forward stepping actions.

        :return: None.
        """

        # build and append final outgoing str
        # grab base character set (only b85b currently)
        charset = tu.b85s()
        char_setter = lambda x: (
            tu.convert_base_inttostr_arbitrary(x, charset))

        # build ending id string
        _program_version = char_setter(
            self.step_plan['version'])
        _program_subversion = char_setter(
            self.step_plan['subversion'])
        _program_subsubversion = char_setter(
            self.step_plan['subsubversion'])
        _default_key = char_setter(
            self.key_handler._kwargs['key_default']).rjust(3, charset[0])
        _thread_count = char_setter(
            self.step_plan['thread_count']).rjust(2, charset[0])
        _byte_len_interior = char_setter(
            self.step_plan['byte_len_interior'])
        _byte_len_exterior = str(
            self.step_plan['byte_len_exterior']).zfill(2)
        _compression_id = char_setter(
            self._kwargs['compression'])
        _hhash_selector = char_setter(
            self.step_plan['hhash_int'])

        # concat these all
        _end_str = (_program_version +
                    _program_subversion +
                    _program_subsubversion +
                    _default_key +
                    _thread_count +
                    _byte_len_interior +
                    _byte_len_exterior +
                    _compression_id +
                    _hhash_selector)

        # encode and append string
        if self.step_plan['byte_len_exterior'] == 0:
            # compress bytes
            self.obj_ = tu.pressor(bytes(str(self.obj_), 'utf-8'),
                                   **self._kwargs)
            # enforce encoding and add metadata
            self.obj_ = str(base64.b85encode(self.obj_))[2:-1]
            # ending nail
            self.obj_ = sl.get_nail(self.obj_,
                                    direction=True,
                                    final_nail=_end_str,
                                    **self.step_plan)
        else:
            raise te.InternalException('B85B encoding is currently the '
                                       'only supported encoding for '
                                       'external facing.')


class StepManagerBackward(StepManagerBase):
    """
    The backward step manager takes in an incoming forward inputs with
    its instructions and organizes backward stepping through all the
    cryptors and keys.

    Public Methods
    --------------
    __call__: Calling on an instance performs a backward call.

    Public Attributes
    --------------
    None

    """

    __slots__ = ('obj_',
                 '_args',
                 '_kwargs',
                 'key_handler',
                 'step_plan',
                 'retriever')

    def __init__(self,
                 obj_: typing.Union[bytes, list[bytes,],],
                 *args: typing.Union[bool, int, float, list, str,],
                 **kwargs: typing.Union[bool, int, float, list, str,],
                 ) -> None:

        # receive inputs if any inputs that are handed into the instance
        self.obj_ = obj_
        self._args = args
        self._kwargs = kwargs
        self._kwargs['direction'] = False

        # establish instances
        self.step_plan = {}
        self.retriever = sl.StepAssignRetriever(direction=False)

        # init default key with zero, this will be updated in the
        # first step with the recovered metadata
        self.key_handler = khc.KeyHandlerBackward(
            retriever=self.retriever, direction=False)

    def __call__(self,
                 *args: typing.Union[bool, int, float, list, str,],
                 **kwargs: typing.Union[bool, int, float, list, str,],
                 ) -> typing.Union[object, list[object,],]:
        """
        Calling instance moves through all backward steps.

        :param args: Not consumed at this time, held for flexibility.
        :param kwargs: Not consumed at this time, held for flexibility.
        :return: A decrypted raw byte object.
        """

        self._backward_first_step()
        self._backward_middle_step()
        self._backward_final_step()
        return self.obj_

    # -------- DECRYPTION --------

    def _backward_first_step(self,
                             ) -> None:
        """
        Performing all first backward stepping actions.

        :return: None.
        """

        # recover the decrypted object by the ending nail
        self.obj_, encryption_metadata = (
            sl.get_nail(self.obj_,
                        direction=False,
                        final_nail=None))

        # raise error if it exists
        if isinstance(self.obj_, te.ProgramException):
            raise self.obj_

        # get outward facing byte len for value conversion internally
        self.step_plan['_byte_len_exterior'] = int(
            encryption_metadata[9:11])
        # establish internal conversion settings for ending string
        if self.step_plan['_byte_len_exterior'] == 0:
            # only b85b supported at this time
            charset = tu.b85s()
            int_setter = lambda x: (
                tu.convert_base_strtoint_arbitrary(x, charset))
        else:
            raise te.DecryptionException('Only Base B85 encoding '
                                         'currently in operation, '
                                         'please only use a '
                                         'respective 00 code')

        # establish items back into the step plan
        self.step_plan['version'] = int_setter(
            encryption_metadata[0])
        self.step_plan['subversion'] = int_setter(
            encryption_metadata[1])
        self.step_plan['subsubversion'] = int_setter(
            encryption_metadata[2])
        self.step_plan['default_key'] = int_setter(
            encryption_metadata[3:6])
        self.step_plan['thread_count'] = int_setter(
            encryption_metadata[6:8])
        self.step_plan['byte_len_interior'] = int_setter(
            encryption_metadata[8])
        self.step_plan['compression'] = int_setter(
            encryption_metadata[11])
        self.step_plan['hhash_selector'] = int_setter(
            encryption_metadata[12])
        self.step_plan['version_full'] = [self.step_plan['version'],
                                          self.step_plan['subversion'],
                                          self.step_plan['subsubversion']]
        self.step_plan['item_demarker'] = self._get_demarker_bytes(
            self.step_plan['version_full'])
        # update the hhash with known selector
        self.key_handler.key_hhasher = functools.partial(
            ct.hhash,
            hash_select=self.step_plan['hhash_selector'],
            mode='plain',
            layers=0)

        # initialize the known keys at the outset:
        _known_keys_dict = {'key_default': self.step_plan['default_key']}
        if 'key_custom' in self._kwargs.keys():
            _known_keys_dict['key_custom'] = (self._kwargs['key_custom'])
        if 'key_filedir' in self._kwargs.keys():
            _known_keys_dict['key_filedir'] = (self._kwargs['key_filedir'])

        self.key_handler.set_all_keys(**_known_keys_dict)

        # prepare external object into internal object for middle stepping
        try:
            if (self.step_plan['byte_len_interior'] == 8 and
                    self.step_plan['_byte_len_exterior'] == 0):
                # evaluate string as bytes, encode it as bytes
                self.obj_ = base64.b85decode(
                    ast.literal_eval(
                        "b'" + self.obj_ + "'"))
                # decompress it and decode it to utf8
                self.obj_ = tu.pressor(self.obj_,
                                       compression=self.step_plan[
                                           'compression'],
                                       **self._kwargs
                                       ).decode('utf-8')
            else:
                raise te.DecryptionException(
                    f'Interior byte length is set to '
                    f'{self.step_plan["byte_len_interior"]}, '
                    f'but interior byte len must be '
                    f'set to 8 for the current program operation')

        except Exception as e:
            raise te.DecryptionException(f'Issue converting incoming byte '
                                         f'object, decryption not possible '
                                         f'with current input: \n'
                                         f'{e}')

    def _backward_middle_step(self,
                              ) -> None:
        """
        Performing all middle backward stepping actions.

        :return: None.
        """

        # init the getter for simple instance lookups
        getter_ = sl.StepAssign(
            retriever=self.retriever,
            plan=self.step_plan)

        # keep step backwards until starting nail
        while (sl.get_nail(self.obj_, direction=False, **self.step_plan) is
               None):
            # get step metadata
            self.obj_, key_, cryptor_ = getter_(self.obj_, direction=False)

            # check if it is under-determined
            if self.obj_ is None or len(self.obj_) < 11:
                warnings.warn('\n\n'
                              'General decryption failure: '
                              'this may be caused by a number '
                              'of reasons. Please ensure that '
                              'any/all of the keys and '
                              'passwords are correct. \n\n'
                              '- If opening and closing quotes '
                              'were accidentally included in the '
                              'incoming object to decrypt please '
                              'remove these from the start and '
                              'end of the decryption input. \n'
                              '- If the object that is being '
                              'decrypted has an expiration '
                              'time that is past expiration '
                              'this could also be why the '
                              'object is failing to decrypt. \n'
                              '- If a file or '
                              'directory is being used as a key '
                              'please ensure it is still in the '
                              'same location. \n'
                              '- If the public ip address of this '
                              'device is being used as a key '
                              'please ensure that it is still '
                              'the same. \n'
                              '- If the web contents of a url '
                              'is being used as a key please '
                              'ensure that the web contents of '
                              'that url are the same. \n'
                              '- If a custom '
                              'key is provided please ensure that '
                              'the key object being provided is '
                              'identical to the one used during '
                              'encryption. \n'
                              '- If all of these '
                              'keys/passwords are ensured to be '
                              'correct and otherwise identical to '
                              'those used during encryption it is '
                              'possible that the user who '
                              'encrypted this object set the '
                              'probability of successful '
                              'encryption to a value of less '
                              'than 100%. If this is the case '
                              'please continue attempting to '
                              'decrypt this object until it '
                              'successfully decrypts. \n\n'
                              'If all of the above is confirmed '
                              'to be working correctly please '
                              'ensure that your copy of the '
                              'program has not been tampered '
                              'with and that you are using '
                              'python version >= 3.9 \n')

                # using exit for multiple threads so that the program
                # doesn't partially keep running
                os._exit(0)

            # if the key is not already in the program keys dict then
            # add it back in
            if key_ not in self.key_handler.program_keys.keys():

                # if a parameter is required for the key then
                # evaluate it here
                # create a temporary index _ti for a substring match _ssm
                _ssm = str(self.step_plan['item_demarker'])[2:-1]
                _ti = self.obj_.find(_ssm)
                # search for match
                if (_ti > 0 and
                        self.obj_[_ti-7:_ti] ==
                        self.obj_[_ti+len(_ssm): _ti+len(_ssm)+7]):

                    # split on the match
                    # static item_demarker and dynamic points --> -7
                    self.obj_, key_parameter = self.obj_.split(
                        self.obj_[_ti: _ti+len(_ssm)+7])

                    # if there are any input keys that need to be
                    # overwritten at the time of decryption the
                    # replacements can be made here at runtime
                    # without further pre-intake

                    # overwrite key_filedir directory if specified
                    if (key_ == 'key_filedir' and
                            'key_path_update' in self._kwargs.keys()):
                        # check if the incoming object looks like a
                        # file or a directory
                        if '.' in pathlib.PurePath(key_parameter).parts[-1]:
                            key_parameter = \
                                (f'{self._kwargs["key_path_update"]}/'
                                 f'{os.path.split(key_parameter)[1]}')

                        # else the path looks like a directory
                        else:
                            key_parameter = self._kwargs['key_path_update']

                    # perform getting with parameter
                    self.key_handler.key_get(key_parameter,
                                             key_id=key_,
                                             get_item='func',
                                             direction=False)

                # if no parameter is required then just get
                else:
                    self.key_handler.key_get(key_id=key_,
                                             get_item='func',
                                             direction=False)

            # step backwards
            self.obj_ = cryptor_(str_in=self.obj_,
                                 key_in=(
                                     self.key_handler.program_keys[key_]),
                                 direction=False,
                                 byte_len=(
                                     self.step_plan['byte_len_interior']))

    def _backward_final_step(self,
                             ) -> None:
        """
        Performing all final backward stepping actions.

        :return: None.
        """

        # un-shuffle the object
        self.obj_ = cc.shuffle(
            str_in=(
                sl.get_nail(self.obj_, direction=False, **self.step_plan)),
            direction=False,
            key_in=self.key_handler.program_keys['key_default'])

        # decompress its bytes
        self.obj_ = tu.pressor(obj_in=ast.literal_eval(self.obj_),
                               direction=False,
                               compression=self.step_plan['compression'])

        # decompress components separately
        self.obj_ = [tu.pressor(obj_in=i,
                                direction=False,
                                compression=self.step_plan['compression'])
                     for i in
                     self.obj_.split(self.step_plan['item_demarker'])]

        # if the outgoing object is only one element then
        # set this element as it is
        if len(self.obj_) == 1:
            self.obj_ = self.obj_[0]

# eof
