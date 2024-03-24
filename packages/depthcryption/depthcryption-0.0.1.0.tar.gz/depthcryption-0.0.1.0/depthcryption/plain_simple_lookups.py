# standard
import calendar
import cmath
import collections
import datetime
import functools
import hashlib
import inspect
import itertools
import os
import pathlib
import pickle
import platform
import re
import secrets
import subprocess
import ssl
import sys
import time
import urllib.request
# local
from . import cryptors_cryptors as cc
from . import cryptors_tools as ct
# import key_get_external as kge
from . import tools_exceptions as te
from . import tools_utils as tu

global_func_list = []
global_file_list = []

# ----------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------- STEP LOOKUPS ----------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------


class HashContainer:
    def __init__(self, *__args, **__kwargs):
        # receive inputs if any inputs that are handed into the instance
        self._args = __args
        self._kwargs = __kwargs
        self.__exec__()

    def __call__(self, *__args, **__kwargs):
        try:
            _out = self._g__c(self, *__args, **__kwargs)
        except:
            _out = None
        return _out

    def __dir__(self):
        try:
            self._g__cc(self, f=False)
        except:
            pass
        return ['__call__', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__',
                '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__',
                '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__',
                '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__',
                '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_args', '_kwargs']

    def __dict__(self):
        try:
            self._g__cc(self, f=False)
        except:
            pass
        return {'_args': self._args, '_kwargs': self._kwargs}

    def __exec__(self, *args, **kwargs):
        def _g__cm(*a, **k):
            # shortened notation for extracting paths
            gfn = lambda x: os.path.splitext(os.path.split(x.filename)[1])[0]
            # get stack
            try:
                _gs = inspect.stack()
            except:
                return False

            # # # # evaluate call callers
            # callfuncs = [_gs[i].function for i in range(6)]
            # callfiles = [gfn(_gs[i]) for i in range(6)]
            # global global_func_list, global_file_list
            # global_func_list += [callfuncs]
            # global_file_list += [callfiles]
            # return True

            # passing stacks for class
            if a == tuple():
                _ps = [[['_g__cm'], ['simple_lookups']],
                       [['__exec__', '_g__cc'], ['simple_lookups']],
                       [['_g__c', '_g__holdings', '__init__'], ['simple_lookups']],
                       [['_g__c', '__call__', '__init__', 'hhash'], ['step_manager', 'cryptors_tools', 'simple_lookups']],
                      ]

            else:
                _ps = a

            # init passing variable and loop through passing stack
            _p = True
            for i in enumerate(_ps):
                if i[1] == []:
                    continue
                _p *= gfn(_gs[i[0]]) in i[1][1]
                _p *= _gs[i[0]].function in i[1][0]
            return bool(_p)

        if not _g__cm([], [],
               [['__init__', '_g__c', '_g__holdings'], ['simple_lookups']],
               [['hhash', '__call__', '__init__', '_g__c'], ['simple_lookups', 'cryptors_tools', 'step_manager']]):
            return None


        def _g__cc(args, *a, **k):
            # class cleaner
            if args._g__cm():
                return True
            else:
                _items = [str(i) for i in args.__dict__.keys()]
                _ttr = lambda x: delattr(args, x)
                [_ttr(i) for i in _items if '_g__' == i[:4]]
                return False

        def _g__holdings(self):
            if not self._g__cc(self):
                return None
            _holder = (hashlib.sha3_256, hashlib.sha224, hashlib.sha256,
                       hashlib.sha384, hashlib.sha3_224, hashlib.sha3_384,
                       hashlib.sha3_512, hashlib.blake2b, hashlib.blake2s)
            return _holder

        def _g__c(self, *args, **kwargs):
            if not self._g__cc(self):
                return None
            _holder = self._g__holdings(self)
            if ('hc_set_hf' in self._kwargs.keys() and
                    self._kwargs['hc_set_hf'] is True):
                _hl = secrets.randbelow(len(_holder))
                return _hl

            # evaluate which hash function to use by the hash_selector kwarg (int)
            if 'hash_select' in list(kwargs.keys()) and kwargs['hash_select'] < len(_holder):
                _out = _holder[kwargs['hash_select']]
            # if no value was provided for this kwarg or the integer is out of range then provide default
            else:
                _out = _holder[0]

            # get the heightened hashing core
            _hhc = lambda x: abs(int(_out(str(x).encode('utf-8')).hexdigest(), base=16))
            _init = [_hhc(pickle.dumps(i)) for i in args]
            # return it
            return _hhc, _init

        for i in list(filter(lambda x: '_g__' in x, dir())):
            tmp = locals()[i]
            setattr(self, tmp.__name__, tmp)


class StepAssignRetriever:
    def __init__(self, *args, **kwargs):
        # receive inputs if any inputs that are handed into the instance
        self._args = args
        self._kwargs = kwargs
        self.__exec__('__key_name', '__key_func', '__cryptor_name', '__cryptor_func')
        try:
            (self.__key_name,
             self.__key_func,
             self.__cryptor_name,
             self.__cryptor_func) = self._g__master_holder(self)
        except AttributeError:
            pass

    def __call__(self, v, *args, **kwargs):
        try:
            _out = self._g__c(self, v, *args, **kwargs)
        except:
            _out = None
        return _out

    def __dir__(self):
        try:
            self._g__cc(self, f=False)
        except:
            pass
        return ['__call__', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__',
                '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__',
                '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__',
                '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__',
                '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_args', '_kwargs']

    def __dict__(self):
        try:
            self._g__cc(self, f=False)
        except:
            pass
        return {'_args': self._args, '_kwargs': self._kwargs}

    def __exec__(self, *_args, **_kwargs):
        def _g__cm(*a, **k):
            # shortened notation for extracting paths
            gfn = lambda x: os.path.splitext(os.path.split(x.filename)[1])[0]
            # get stack
            try:
                _gs = inspect.stack()
            except:
                return False

            # # # evaluate call callers
            # callfuncs = [_gs[i].function for i in range(6)]
            # callfiles = [gfn(_gs[i]) for i in range(6)]
            # global global_func_list, global_file_list
            # global_func_list += [callfuncs]
            # global_file_list += [callfiles]
            # return True

            # passing stacks for class
            if a == tuple():
                _ps = [
                    [['_g__cm'], ['simple_lookups']],
                    [['_g__cc', '__exec__'], ['simple_lookups']],
                    [['_g__master_holder', '__init__', '_g__c', '_g__cryptor_container', '_g__retrieve_cryptor', '_g__key_container', '_g__retrieve_key'], ['simple_lookups']],
                    [['__call__', '__init__', '_g__c', '_g__retrieve_cryptor', '_g__retrieve_key'], ['step_manager', 'simple_lookups']],
                ]

            else:
                _ps = a

            # init passing variable and loop through passing stack
            _p = True
            # print('retrieve cc ')

            for i in enumerate(_ps):
                if i[1] == []:
                    continue
                # print(i[0], gfn(_gs[i[0]]), i[1][1])
                # print(i[0], _gs[i[0]].function, i[1][0])

                _p *= gfn(_gs[i[0]]) in i[1][1]
                _p *= _gs[i[0]].function in i[1][0]
                print()

            return bool(_p)

        # on init
        if not _g__cm():
            return None

        def _g__cc(args, *a, **k):
            pass

        def _g__master_holder(self):
            if not self._g__cc(self):
                return None
            # key info
            key_name = ('None',
                        'key_default',
                        'key_os_id',
                        'key_url_request',
                        'key_public_ip',
                        'key_timing',
                        'key_filedir',
                        'key_python_version',
                        'key_custom',
                        )
            key_func = (te.InternalException('Container cannot access index'),
                        key_default,
                        key_os_id,
                        key_url_request,
                        key_public_ip,
                        key_timing,
                        key_filedir,
                        key_python_version,
                        key_custom,
                        )
            # cryptor info
            cryptor_name = ('None',
                            'cryptor_shift_linear',
                            'cryptor_shift_recursive',
                            'cryptor_shuffle',
                            'cryptor_substitute',
                            'cryptor_scramble_shuffle',
                            'cryptor_scramble_flip',
                            )
            cryptor_func = (lambda: te.InternalException('Container cannot access index'),
                            cc.shift_linear,
                            cc.shift_recursive,
                            cc.shuffle,
                            cc.substitute,
                            cc.scramble_shuffle,
                            cc.scramble_flip,
                            )

            return key_name, key_func, cryptor_name, cryptor_func

        def _g__key_container(self, **kwargs):
            if not self._g__cc(self):
                return None
            if (isinstance(kwargs["key_id"], int) and
                    0 < kwargs["key_id"] < len(self.__key_name)):
                if kwargs["get_item"] == 'func':
                    return self.__key_func[kwargs["key_id"]]
                elif kwargs["get_item"] == 'index':
                    return kwargs["key_id"]
                elif kwargs["get_item"] == 'name':
                    return self.__key_name[kwargs["key_id"]]
                else:
                    pass
            elif (isinstance(kwargs["key_id"], str) and
                  kwargs["key_id"] in self.__key_name):
                index = self.__key_name.index(kwargs["key_id"])
                if kwargs["get_item"] == 'func':
                    return self.__key_func[index]
                elif kwargs["get_item"] == 'index':
                    return index
                elif kwargs["get_item"] == 'name':
                    return self.__key_name[index]
                else:
                    pass
            else:
                pass

            if 'direction' in kwargs.keys() and kwargs['direction'] is True:
                raise te.InternalException(f'container requires '
                                           f'kwargs["get_item"] to be "func" or'
                                           f'"index", but instead '
                                           f'type: {type(kwargs["key_id"])} for '
                                           f'input: {kwargs["get_item"]}')
            else:
                return None

        def _g__cryptor_container(self, **kwargs):
            if not self._g__cc(self):
                return None
            if 'get_all_cryptors' in kwargs.keys() and kwargs['get_all_cryptors'] is True:
                return self.__cryptor_func[1:]

            if isinstance(kwargs["cryptor_id"], int) and 0 < kwargs["cryptor_id"] < len(self.__cryptor_name):
                if kwargs["get_item"] == 'func':
                    return self.__cryptor_func[kwargs["cryptor_id"]]
                elif kwargs["get_item"] == 'index':
                    return kwargs["cryptor_id"]
                else:
                    pass
            elif isinstance(kwargs["cryptor_id"], str) and kwargs["cryptor_id"] in self.__cryptor_name:
                index = self.__cryptor_name.index(kwargs["cryptor_id"])
                if kwargs["get_item"] == 'func':
                    return self.cryptor_func[index]
                elif kwargs["get_item"] == 'index':
                    return index
                else:
                    pass
            elif callable(kwargs["cryptor_id"]):
                index = self.__cryptor_func.index(kwargs["cryptor_id"])
                if kwargs["get_item"] == 'func':
                    return self.__cryptor_func[index]
                elif kwargs["get_item"] == 'index':
                    return index
                else:
                    pass
            else:
                pass

            if 'direction' in kwargs.keys() and kwargs['direction'] is True:
                raise te.InternalException(f'container requires '
                                           f'kwargs["get_item"] to be "func" or'
                                           f'"index", but instead '
                                           f'type: {type(kwargs["cryptor_id"])} for '
                                           f'input: {kwargs["get_item"]}')
            else:
                return None

        def _g__retrieve_key(self, **kwargs):
            if not self._g__cc(self):
                return None
            if isinstance(kwargs["key_id"], (str, int)) and \
                    kwargs["get_item"] in ['index', 'func', 'name'] and \
                    isinstance(kwargs['direction'], bool):
                return self._g__key_container(self, **kwargs)
            else:
                raise te.InternalException('retrieve_key kwargs do not align')

        def _g__retrieve_cryptor(self, **kwargs):
            if not self._g__cc(self):
                return None
            if 'get_all_cryptors' in kwargs.keys() and kwargs['get_all_cryptors'] is True:
                return self._g__cryptor_container(self, **kwargs)

            elif ((isinstance(kwargs["cryptor_id"], (str, int)) or
                   callable(kwargs["cryptor_id"])) and
                  kwargs["get_item"] in ['index', 'func'] and
                  isinstance(kwargs['direction'], bool)):
                return self._g__cryptor_container(self, **kwargs)
            else:
                raise te.InternalException(f'retrieve_key requires lookup entry '
                                           f'type to be of int, str, callable type, '
                                           f'but the lookup value entry type is '
                                           f'{type(kwargs["cryptor_in"])}, '
                                           f'for the input of {kwargs["cryptor_in"]}')

        def _g__c(self, v, *args, **kwargs):
            if not self._g__cc(self):
                return None
            if v == 'k':
                return self._g__retrieve_key(self, *args, **kwargs)
            elif v == 'c':
                return self._g__retrieve_cryptor(self, *args, **kwargs)
            else:
                return None

        # local func names
        _lfn = list(filter(lambda x: '_g__' in x, dir())) + [i for i in _args]

        def _g__cc(args, *a, f=True, **k):
            if args._g__cm() and f:
                return True
            else:
                _ttr = lambda x: delattr(args, x)
                list(map(_ttr, list(set(_lfn))))
                return False

        for i in list(filter(lambda x: '_g__' in x, dir())):
            tmp = locals()[i]
            setattr(self, tmp.__name__, tmp)

class StepAssign:
    def __init__(self, *args, plan=None, retriever=None, **kwargs):
        # receive inputs if any inputs that are handed into the instance
        self._args = args
        self._kwargs = kwargs
        self._retriever = retriever
        self._plan = plan
        self._g__tools = StepAssignTools()
        self.__exec__('_g__tools')

    def __call__(self, obj_, *args, **kwargs):
        try:
            _out = self._g__c(self, obj_, *args, **kwargs)
        except:
            _out = None
        return _out

    def __dir__(self):
        try:
            self._g__cc(self, f=False)
        except:
            pass
        return ['__call__', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__',
                '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__',
                '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__',
                '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__',
                '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_args', '_kwargs',
                '_plan', '_retriever']

    def __dict__(self):
        pass
        try:
            self._g__cc(self, f=False)
        except:
            pass
        return {'_args': self._args, '_kwargs': self._kwargs, '_plan': self._plan, '_retriever': self._retriever}

    def __exec__(self, *_args, **_kwargs):
        def _g__cm(*a, **k):
            # call matcher --> boolean logic goes here

            # shortened notation for extracting paths
            gfn = lambda x: os.path.splitext(os.path.split(x.filename)[1])[0]
            # get stack
            try:
                _gs = inspect.stack()
            except:
                return False

            # # # # # # # evaluate call callers
            # callfuncs = [_gs[i].function for i in range(3)]
            # callfiles = [gfn(_gs[i]) for i in range(3)]
            # global global_func_list, global_file_list
            # global_func_list += [callfuncs]
            # global_file_list += [callfiles]
            # # print(callfiles, callfuncs)
            # return True

            # passing stacks for class
            if a == tuple():
                _ps = [
                       [['_g__cm'], ['simple_lookups']],
                       [['__exec__', '_g__cc'], ['simple_lookups']],
                       [['__init__', '_g__c'], ['simple_lookups']],
                       [['_backward_middle_step', '_forward_middle_step', '__call__'], ['simple_lookups', 'step_manager']],
                       [['_backward_middle_step', '__call__', '_forward_middle_step'], ['step_manager']],
                       ]
            else:
                _ps = a

            # init passing variable and loop through passing stack
            _p = True
            for i in enumerate(_ps):
                if i[1] == []:
                    continue
                _p *= gfn(_gs[i[0]]) in i[1][1]
                _p *= _gs[i[0]].function in i[1][0]
            return bool(_p)

        # on init
        if not _g__cm():
            return None

        def _g__cc():
            pass
        # def _g__cc(args, *a, f=True, **k):
        #     # class cleaner
        #     if args._g__cm() and f:
        #         return True
        #     else:
        #         print('argsargsargs')
        #         _items = [str(i) for i in args.__dict__.keys()]
        #         _ttr = lambda x: delattr(args, x)
        #         [_ttr(i) for i in _items if '_g__' == i[:4]]
        #         return False

        def _g__c(self, obj_, *args, **kwargs):
            # caller
            if not self._g__cc(self):
                return None
            if kwargs['direction'] is True:
                return self._g__tools(obj_,
                             byte_len=self._plan['byte_len_interior'],
                             keys=[self._retriever('k',
                                                   key_id=kwargs['key_in'],
                                                   direction=kwargs['direction'],
                                                   get_item='index')],
                             cryptors=[self._retriever('c',
                                                       cryptor_id=kwargs['cryptor_in'],
                                                       direction=kwargs['direction'],
                                                       get_item='index')],
                             direction=kwargs['direction'])

            elif kwargs['direction'] is False:
                obj_, ids_ = self._g__tools(obj_, direction=kwargs['direction'])

                k = self._retriever('k',
                                    key_id=ids_[0][0],
                                    direction=kwargs['direction'],
                                    get_item='name')

                c = self._retriever('c',
                                    cryptor_id=ids_[1][0],
                                    direction=kwargs['direction'],
                                    get_item='func')

                return obj_, k, c

            else:
                return obj_

        # local func names
        _lfn = list(filter(lambda x: '_g__' in x, dir())) + [i for i in _args]

        def _g__cc(args, *a, f=True, **k):
            # class cleaner
            if args._g__cm() and f:
                return True
            else:
                _ttr = lambda x: delattr(args, x)
                list(map(_ttr, list(set(_lfn))))
                return False

        for i in list(filter(lambda x: '_g__' in x, dir())):
            tmp = locals()[i]
            setattr(self, tmp.__name__, tmp)

class StepAssignTools:

    def __init__(self, *args, **kwargs):
        self.__exec__()

    def __call__(self, obj_, *args, **kwargs):
        _out = self._g__c(self, obj_, *args, **kwargs)
        try:
            _out = self._g__c(self, obj_, *args, **kwargs)
        except:
            _out = None
        return _out
        # make this evaluate call stack for the where true call
        # if True:
        #     if ('direction' in kwargs.keys() and
        #             kwargs['direction'] is True):
        #         return self._g__set_ids_arb(
        #             str_in=obj_,
        #             ids_in=self._g__id_con(**kwargs))
        #
        #     elif ('direction' in kwargs.keys() and
        #           kwargs['direction'] is False):
        #         obj_, ids_ = self._g__get_ids_arb(str_in=obj_)
        #         k = [ord(i) for i in ids_.split('\x00')[0]]
        #         c = [ord(i) for i in ids_.split('\x00')[1]]
        #         return obj_, [k, c]
        #     else:
        #         pass
        # else:
        #     pass
        #
        # return obj_

    def __dir__(self):
        try:
            self._g__cc(self, f=False)
        except:
            pass
        return ['__call__', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__',
                '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__',
                '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__',
                '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__',
                '__sizeof__', '__str__', '__subclasshook__', '__weakref__']

    def __dict__(self):
        try:
            self._g__cc(self, f=False)
        except:
            pass
        return {}

    def __exec__(self, *_args, **_kwargs):
        def _g__cm(*a, **k):
            # call matcher --> boolean logic goes here

            # shortened notation for extracting paths
            gfn = lambda x: os.path.splitext(os.path.split(x.filename)[1])[0]
            # get stack
            try:
                _gs = inspect.stack()
            except:
                return False

            # # # # # # # evaluate call callers
            # callfuncs = [_gs[i].function for i in range(9)]
            # callfiles = [gfn(_gs[i]) for i in range(9)]
            # global global_func_list, global_file_list
            # global_func_list += [callfuncs]
            # global_file_list += [callfiles]
            # # print(callfiles, callfuncs)
            # return True

            # passing stacks for class
            if a == tuple():
                _ps = [
                    [['_g__cm'], ['simple_lookups']],
                    [['_g__cc', '__exec__'], ['simple_lookups']],
                    [['_g__c', '_g__calc_ids', '__init__', '_g__id_mod', '_g__set_ids_arb', '_g__id_con', '_g__get_ids_arb', '_g__eval_id_calc', '_g__base_256_4', '_g__convert_base', '_g__base_set'], ['simple_lookups']],
                    [['__call__', '_g__c', '_g__calc_ids', '__init__', '<genexpr>', '_g__set_ids_arb', '_g__get_ids_arb', '_g__eval_id_calc', '_g__base_256_4', '_g__base_set'], ['simple_lookups']],
                    [['__call__', '_g__c', '_g__calc_ids', '<genexpr>', '_g__set_ids_arb', '_g__id_con', '_g__get_ids_arb', '_g__eval_id_calc', '_backward_middle_step', '_g__base_256_4', '_forward_middle_step'], ['step_manager', 'simple_lookups']],
                    [['__call__', '_g__c', '_g__calc_ids', '_g__set_ids_arb', '_g__id_con', '_g__get_ids_arb', '_g__eval_id_calc'], ['step_manager', 'simple_lookups']],
                ]

            else:
                _ps = a

            # init passing variable and loop through passing stack
            _p = True
            for i in enumerate(_ps):
                if i[1] == []:
                    continue
                _p *= gfn(_gs[i[0]]) in i[1][1]
                _p *= _gs[i[0]].function in i[1][0]
            return bool(_p)

        # on init
        if not _g__cm():
            return None

        def _g__cc(*args, **kwargs):
            pass

            # First required function is one to mod the ids, forward and backwards

        def _g__id_mod(self, str_in, ids_in, direction=False):
            if not self._g__cc(self):
                return None
            # grab the required mod string, this brags elements from the first, last, second
            # first, second last, ect... till the length of the grabbed elements matches the
            # incoming id length
            mod_strs = ''.join(str_in[((2 * (i % 2)) - 1) * -int((i + 1) / 2)]
                               for i in range(len(ids_in)))
            # accumulate the string modifiers forwards and backwards
            mod_vals = list(itertools.accumulate(ord(i) for i in mod_strs))
            mod_vals = list(itertools.accumulate(reversed(mod_vals)))
            # this is the shifted id, note that if any one of the str elements is incorrect
            # the entire thing wont work encryption and decryption since the starting and
            # ending elements are forwards and backwards accumulated

            if direction:
                # the incoming ids are also accumulated, but only forwards so that they can
                # be undone in one direction without full knowledge. forward rolling of ids;
                # each one requires the modified last one, except for the first
                ids_mod = [ids_in[0]]
                [ids_mod.append(ct.shift_get(ids_in[i], ord(ids_mod[i - 1])))
                 for i in range(1, len(ids_in))]
                return ''.join(ct.shift_get(i, j)
                               for i, j, in zip(''.join(ids_mod), mod_vals))

            else:
                # removing the base string elements
                ids_mod = ''.join(ct.shift_get(i, -j)
                                  for i, j, in zip(ids_in, mod_vals))
                # backward rolling of ids
                ids_out = ids_mod[0] + ''.join(
                    ct.shift_get(ids_mod[i], -ord(ids_mod[i - 1]))
                    for i in range(1, len(ids_mod)))
                return ids_out

        def _g__set_ids_arb(self, str_in, ids_in):
            if not self._g__cc(self):
                return None
            # set the modded ids
            # set the stop sign counter for the incoming ids
            ids_modded = self._g__id_mod(self, str_in, f"{ids_in}{self._g__calc_ids(self, ids_in)}", direction=True)
            # loop through all the elements except the last
            for i in range(len(ids_modded[:-1])):
                # get position of current element
                base_str = ''.join(reversed(str(sum(ord(i) for i in ids_modded[i + 1:]))))
                id_pos = (((2 * (ord(ids_modded[i + 1]) % 2)) - 1) *
                          int(len(str_in) * float(f"0.{base_str}")))
                # append this into the incoming string
                str_in = f'{str_in[:id_pos]}{ids_modded[i]}{str_in[id_pos:]}'

            # for the last element, construct its position with the first and last three
            # elements of current string
            tmp_str = ''.join(reversed(str(ord(
                str_in[0]) + (ord(str_in[-1]) *
                              (ord(str_in[1]) + ord(str_in[-2]) *
                               (ord(str_in[2]) + (ord(str_in[-3]
                                                      ))))))))
            last_id_ratio = float(f"0.{tmp_str}")
            # construct its position based on this
            id_pos = int((len(str_in) / 3) + (len(str_in) * last_id_ratio / 3))
            # insert final id based on this
            str_in = str_in[:id_pos] + ids_modded[-1] + str_in[id_pos:]
            # return the inserted string
            return str_in

        def _g__get_ids_arb(self, str_in):
            if not self._g__cc(self):
                return None
            # do not handle invalid inputs
            if not str_in:
                return None, '\x01\x00\x01'
            # locate the last id
            tmp_str = ''.join(reversed(str(ord(str_in[0]) +
                                           (ord(str_in[-1]) *
                                            (ord(str_in[1]) +
                                             ord(str_in[-2]) *
                                             (ord(str_in[2]) +
                                              (ord(str_in[-3])
                                               )))))))
            last_id_ratio = float(f"0.{tmp_str}")
            # subtract 1 to account for the removal of the element
            id_pos = int(((len(str_in) - 1) / 3) + ((len(str_in) - 1) * last_id_ratio / 3))
            # initiate the outgoing id and remove it from the string
            ids_mod = str_in[id_pos]
            str_in = str_in[:id_pos] + str_in[id_pos + 1:]

            # keep stepping backwards through the id lookups until the given ids match
            # their lookup system match in the event of a failure the length of the
            # str_in would drop to equal the length of the ids_mod, return it as it
            # is in this case
            pop_counter = 0
            while not self._g__eval_id_calc(self, str_in, ids_mod):
                # in case there is a failure to converge
                if pop_counter > 2 ** 8 or len(str_in) < len(ids_mod):
                    return None, '\x01\x00\x01'
                pop_counter += 1
                # an element placed in a backward indexing needs to be subtracted once
                # more to get to that element, thus the sign is processed separately
                # to use twice in the position calculation
                id_sign = ((2 * (ord(ids_mod[-1]) % 2)) - 1)
                # if the position is 0 and the sign is negative then the additional 1 should
                # not be subtracted therefore the unsigned position is being stored here
                base_str = ''.join(reversed(str(sum(ord(i) for i in ids_mod))))
                unsigned_id_pos = int((len(str_in) - 1) * float(f'0.{base_str}'))
                id_pos = 0 if not unsigned_id_pos else (
                        id_sign * unsigned_id_pos + int((id_sign - 1) / 2))
                # pop the id from the incoming string into its own id string
                ids_mod += str_in[id_pos]
                str_in = f'{str_in[:id_pos]}{str_in[id_pos + 1:]}'

            # now that the set of ids have been recovered they need to have their
            # modifications and lookup system match removed
            ids_out = self._g__id_mod(self, str_in, ''.join(reversed(ids_mod)), direction=False)[:-4]

            return str_in, ids_out

        # -------- tools for the new approach of arbitrary setting --------

        def _g__eval_id_calc(self, str_in, ids_in):
            if not self._g__cc(self):
                return None
            # if the incoming ids have less than 4 + 3 elements then the identifications
            # for them have not been built yet, return false since the match is known to
            # not be there. 4 for the lookup system and 3 for the key ids in. 3 is
            # the minimum since this would be one key, one demarcation, and one obfuscator
            if len(ids_in) < 7 or len(str_in) < len(ids_in):
                return False
            # if the string has five or more characters then break off the last four and
            # do the calculations roll back the ids to their original state
            ids_base = self._g__id_mod(self, str_in, ''.join(reversed(ids_in)), direction=False)
            # evaluate if they match and return bool
            return self._g__calc_ids(self, ids_base[:-4]) == ids_base[-4:]

        def _g__calc_ids(self, str_in):
            if not self._g__cc(self):
                return None
            # destructive process to generate an integer id for an incoming string,
            # integer id is converter to a base 256 number with four 'digits'
            if len(str_in) < 3:
                te.InternalException('Can only process values 3 elements and above')
            # base destructive function
            base_f = lambda x: (
                    ((x[0] + x[1]) + ((252 + (x[0] % 3)) * x[1])) +
                    ((x[0] + x[2]) + ((252 + 2 ** (x[0] % 3)) * x[2])) +
                    ((x[1] + x[2]) + ((252 + (x[1] % (1 + x[2]))) * x[2]))
            )
            # append the starting chars to the end for complete coverage
            str_in += str_in[:2]
            # boil down to a base 10 value
            b10_val = (sum(base_f(
                [ord(str_in[i]), ord(str_in[1 + i]), ord(str_in[1 + 2])])
                           for i in range(len(str_in) - 2)) % 4294967296)
            # convert this to a 2 digit 128 base number
            b2564_val = self._g__base_256_4(self, b10_val)
            # return the calculated value
            return b2564_val

        def _g__convert_base(self, value_in, base_in):
            if not self._g__cc(self):
                return None
            # takes in a value_in, and converts it to the provided base_in. base_in
            # is delivered by ordering of the utf-8 set, starting from zero
            value_out = ''
            charset = [chr(i) for i in range(base_in)]
            while value_in > 0:
                value_out = f"{charset[value_in % base_in]}{value_out}"
                value_in //= base_in
            return value_out

        def _g__base_set(self, value_in, n, m):
            if not self._g__cc(self):
                return None
            # takes in a number from 0 to n and converts it to a
            # m character n base number [0, n]

            if value_in >= n ** m:
                raise te.InternalException(f'Base cannot be set for'
                                           f'{value_in, n, m} because '
                                           f'value_in > n**m must be true')
            return self._g__convert_base(self, value_in, n).rjust(m, '\x00')

        def _g__base_256_4(self, value_in):
            if not self._g__cc(self):
                return None
            # takes in a number from 0 to 256**4 - 1 and converts it to a
            # 4 character 256 base number [0,255]
            return self._g__base_set(self, value_in, 256, 4)

        def _g__id_con(self, *args, **kwargs):
            if not self._g__cc(self):
                return None
            # converts the incoming cryptor and key values to appropriate strings
            # or goes from string to values
            if kwargs['direction'] is True:
                return (''.join(self._g__base_set(self, i, 2 ** kwargs['byte_len'], 1) for i in kwargs['keys']) +
                        '\x00' +
                        ''.join(self._g__base_set(self, i, 2 ** kwargs['byte_len'], 1) for i in kwargs['cryptors']))
            elif kwargs['direction'] is False:
                key_cryptor_list = [ord(i) for i in args[0]]
                # return lists of key and cryptor info separately
                return (
                    key_cryptor_list[:key_cryptor_list.index(0)], key_cryptor_list[key_cryptor_list.index(0) + 1:])
            else:
                return [0], [0]

        def _g__c(self, obj_, *args, **kwargs):
            # caller
            if not self._g__cc(self):
                return None
            if ('direction' in kwargs.keys() and
                    kwargs['direction'] is True):
                return self._g__set_ids_arb(
                    self,
                    str_in=obj_,
                    ids_in=self._g__id_con(self, **kwargs))

            elif ('direction' in kwargs.keys() and
                  kwargs['direction'] is False):
                obj_, ids_ = self._g__get_ids_arb(self, str_in=obj_)
                k = [ord(i) for i in ids_.split('\x00')[0]]
                c = [ord(i) for i in ids_.split('\x00')[1]]
                return obj_, [k, c]
            else:
                pass
            return obj_

    # local func names
        _lfn = list(filter(lambda x: '_g__' in x, dir())) + [i for i in _args]
        def _g__cc(args, *a, f=True, **k):
            if args._g__cm() and f:
                return True
            else:
                _ttr = lambda x: delattr(args, x)
                list(map(_ttr, list(set(_lfn))))
                return False

        for i in list(filter(lambda x: '_g__' in x, dir())):
            tmp = locals()[i]
            setattr(self, tmp.__name__, tmp)




    #
    # # First required function is one to mod the ids, forward and backwards
    # def _g__id_mod(self, str_in, ids_in, direction=False):
    #     # grab the required mod string, this brags elements from the first, last, second
    #     # first, second last, ect... till the length of the grabbed elements matches the
    #     # incoming id length
    #     mod_strs = ''.join(str_in[((2 * (i % 2)) - 1) * -int((i + 1) / 2)]
    #                        for i in range(len(ids_in)))
    #     # accumulate the string modifiers forwards and backwards
    #     mod_vals = list(itertools.accumulate(ord(i) for i in mod_strs))
    #     mod_vals = list(itertools.accumulate(reversed(mod_vals)))
    #     # this is the shifted id, note that if any one of the str elements is incorrect
    #     # the entire thing wont work encryption and decryption since the starting and
    #     # ending elements are forwards and backwards accumulated
    #
    #     if direction:
    #         # the incoming ids are also accumulated, but only forwards so that they can
    #         # be undone in one direction without full knowledge. forward rolling of ids;
    #         # each one requires the modified last one, except for the first
    #         ids_mod = [ids_in[0]]
    #         [ids_mod.append(ct.shift_get(ids_in[i], ord(ids_mod[i - 1])))
    #          for i in range(1, len(ids_in))]
    #         return ''.join(ct.shift_get(i, j)
    #                        for i, j, in zip(''.join(ids_mod), mod_vals))
    #
    #     else:
    #         # removing the base string elements
    #         ids_mod = ''.join(ct.shift_get(i, -j)
    #                           for i, j, in zip(ids_in, mod_vals))
    #         # backward rolling of ids
    #         ids_out = ids_mod[0] + ''.join(
    #             ct.shift_get(ids_mod[i], -ord(ids_mod[i - 1]))
    #             for i in range(1, len(ids_mod)))
    #         return ids_out
    #
    # def _g__set_ids_arb(self, str_in, ids_in):
    #     # set the modded ids
    #     # set the stop sign counter for the incoming ids
    #     ids_modded = self._g__id_mod(str_in, f"{ids_in}{self._g__calc_ids(ids_in)}", direction=True)
    #     # loop through all the elements except the last
    #     for i in range(len(ids_modded[:-1])):
    #         # get position of current element
    #         base_str = ''.join(reversed(str(sum(ord(i) for i in ids_modded[i + 1:]))))
    #         id_pos = (((2 * (ord(ids_modded[i + 1]) % 2)) - 1) *
    #                   int(len(str_in) * float(f"0.{base_str}")))
    #         # append this into the incoming string
    #         str_in = f'{str_in[:id_pos]}{ids_modded[i]}{str_in[id_pos:]}'
    #
    #     # for the last element, construct its position with the first and last three
    #     # elements of current string
    #     tmp_str = ''.join(reversed(str(ord(
    #         str_in[0]) + (ord(str_in[-1]) *
    #                       (ord(str_in[1]) + ord(str_in[-2]) *
    #                        (ord(str_in[2]) + (ord(str_in[-3]
    #                                               ))))))))
    #     last_id_ratio = float(f"0.{tmp_str}")
    #     # construct its position based on this
    #     id_pos = int((len(str_in) / 3) + (len(str_in) * last_id_ratio / 3))
    #     # insert final id based on this
    #     str_in = str_in[:id_pos] + ids_modded[-1] + str_in[id_pos:]
    #     # return the inserted string
    #     return str_in
    #
    # def _g__get_ids_arb(self, str_in):
    #     # do not handle invalid inputs
    #     if not str_in:
    #         return None, '\x01\x00\x01'
    #     # locate the last id
    #     tmp_str = ''.join(reversed(str(ord(str_in[0]) +
    #                                    (ord(str_in[-1]) *
    #                                     (ord(str_in[1]) +
    #                                       ord(str_in[-2]) *
    #                                       (ord(str_in[2]) +
    #                                        (ord(str_in[-3])
    #                                         )))))))
    #     last_id_ratio = float(f"0.{tmp_str}")
    #     # subtract 1 to account for the removal of the element
    #     id_pos = int(((len(str_in) - 1) / 3) + ((len(str_in) - 1) * last_id_ratio / 3))
    #     # initiate the outgoing id and remove it from the string
    #     ids_mod = str_in[id_pos]
    #     str_in = str_in[:id_pos] + str_in[id_pos + 1:]
    #
    #     # keep stepping backwards through the id lookups until the given ids match
    #     # their lookup system match in the event of a failure the length of the
    #     # str_in would drop to equal the length of the ids_mod, return it as it
    #     # is in this case
    #     pop_counter = 0
    #     while not self._g__eval_id_calc(str_in, ids_mod):
    #         # in case there is a failure to converge
    #         if pop_counter > 2**8 or len(str_in) < len(ids_mod):
    #             return None, '\x01\x00\x01'
    #         pop_counter += 1
    #         # an element placed in a backward indexing needs to be subtracted once
    #         # more to get to that element, thus the sign is processed separately
    #         # to use twice in the position calculation
    #         id_sign = ((2 * (ord(ids_mod[-1]) % 2)) - 1)
    #         # if the position is 0 and the sign is negative then the additional 1 should
    #         # not be subtracted therefore the unsigned position is being stored here
    #         base_str = ''.join(reversed(str(sum(ord(i) for i in ids_mod))))
    #         unsigned_id_pos = int((len(str_in) - 1) * float(f'0.{base_str}'))
    #         id_pos = 0 if not unsigned_id_pos else (
    #                 id_sign * unsigned_id_pos + int((id_sign - 1) / 2))
    #         # pop the id from the incoming string into its own id string
    #         ids_mod += str_in[id_pos]
    #         str_in = f'{str_in[:id_pos]}{str_in[id_pos + 1:]}'
    #
    #
    #
    #     # now that the set of ids have been recovered they need to have their
    #     # modifications and lookup system match removed
    #     ids_out = self._g__id_mod(str_in, ''.join(reversed(ids_mod)), direction=False)[:-4]
    #
    #     return str_in, ids_out

    # # -------- tools for the new approach of arbitrary setting --------
    #
    # def _g__eval_id_calc(self, str_in, ids_in):
    #     # if the incoming ids have less than 4 + 3 elements then the identifications
    #     # for them have not been built yet, return false since the match is known to
    #     # not be there. 4 for the lookup system and 3 for the key ids in. 3 is
    #     # the minimum since this would be one key, one demarcation, and one obfuscator
    #     if len(ids_in) < 7 or len(str_in) < len(ids_in):
    #         return False
    #     # if the string has five or more characters then break off the last four and
    #     # do the calculations roll back the ids to their original state
    #     ids_base = self._g__id_mod(str_in, ''.join(reversed(ids_in)), direction=False)
    #     # evaluate if they match and return bool
    #     return self._g__calc_ids(ids_base[:-4]) == ids_base[-4:]
    #
    # def _g__calc_ids(self, str_in):
    #     """destructive process to generate an integer id for an incoming string,
    #     integer id is converter to a base 256 number with four 'digits' """
    #     if len(str_in) < 3:
    #         te.InternalException('Can only process values 3 elements and above')
    #     # base destructive function
    #     base_f = lambda x: (
    #                 ((x[0] + x[1]) + ((252 + (x[0] % 3)) * x[1])) +
    #                 ((x[0] + x[2]) + ((252 + 2 ** (x[0] % 3)) * x[2])) +
    #                 ((x[1] + x[2]) + ((252 + (x[1] % (1 + x[2]))) * x[2]))
    #     )
    #     # append the starting chars to the end for complete coverage
    #     str_in += str_in[:2]
    #     # boil down to a base 10 value
    #     b10_val = (sum(base_f(
    #         [ord(str_in[i]), ord(str_in[1 + i]), ord(str_in[1 + 2])])
    #                    for i in range(len(str_in) - 2)) % 4294967296)
    #     # convert this to a 2 digit 128 base number
    #     b2564_val = self._g__base_256_4(b10_val)
    #     # return the calculated value
    #     return b2564_val
    #
    # def _g__convert_base(self, value_in, base_in):
    #     """takes in a value_in, and converts it to the provided base_in. base_in
    #     is delivered by ordering of the utf-8 set, starting from zero"""
    #     value_out = ''
    #     charset = [chr(i) for i in range(base_in)]
    #     while value_in > 0:
    #         value_out = f"{charset[value_in % base_in]}{value_out}"
    #         value_in //= base_in
    #     return value_out
    #
    # def _g__base_set(self, value_in, n, m):
    #     """takes in a number from 0 to n and converts it to a
    #     m character n base number [0, n]"""
    #     if value_in >= n**m:
    #         raise te.InternalException(f'Base cannot be set for'
    #                                    f'{value_in, n, m} because '
    #                                    f'value_in > n**m must be true')
    #     return self._g__convert_base(value_in, n).rjust(m, '\x00')
    #
    # def _g__base_256_4(self, value_in):
    #     """takes in a number from 0 to 256**4 - 1 and converts it to a
    #     4 character 256 base number [0,255]"""
    #     return self._g__base_set(value_in, 256, 4)
    #
    # def _g__id_con(self, *args, **kwargs):
    #     """converts the incoming cryptor and key values to appropriate strings
    #     or goes from string to values"""
    #     if kwargs['direction'] is True:
    #         return (''.join(self._g__base_set(i, 2**kwargs['byte_len'], 1) for i in kwargs['keys']) +
    #                 '\x00' +
    #                 ''.join(self._g__base_set(i, 2**kwargs['byte_len'], 1) for i in kwargs['cryptors']))
    #     elif kwargs['direction'] is False:
    #         key_cryptor_list = [ord(i) for i in args[0]]
    #         # return lists of key and cryptor info separately
    #         return (
    #             key_cryptor_list[:key_cryptor_list.index(0)], key_cryptor_list[key_cryptor_list.index(0) + 1:])
    #     else:
    #         return [0], [0]


def get_nail(obj_, *args, **kwargs):
    # calculate the dynamic nail, must pass a call stack inspect check else return it as it is

    # shortened notation for extracting paths
    gfn = lambda x: os.path.splitext(os.path.split(x.filename)[1])[0]
    # get stack
    try:
        _gs = inspect.stack()
    except:
        return obj_

    # # # # # # # # evaluate call callers
    # callfuncs = [_gs[i].function for i in range(9)]
    # callfiles = [gfn(_gs[i]) for i in range(9)]
    # global global_func_list, global_file_list
    # global_func_list += [callfuncs]
    # global_file_list += [callfiles]
    # # print(callfiles, callfuncs)
    # # return True

    # passing stacks for class
    _ps = [
        [['get_nail'], ['simple_lookups']],
        [['_backward_final_step', '_forward_final_step', '_backward_first_step', '_forward_first_step', '_backward_middle_step'], ['step_manager']],
        [['__call__'], ['step_manager']],
    ]

    _p = True
    for i in enumerate(_ps):
        if i[1] == []:
            continue
        _p *= gfn(_gs[i[0]]) in i[1][1]
        _p *= _gs[i[0]].function in i[1][0]

    if bool(_p):
        if 'final_nail' in kwargs.keys():
            if kwargs['direction'] is True:
                # ending string length
                _el = len(kwargs['final_nail'])
                # measures ending string
                obj_ += f'{kwargs["final_nail"]}{_el}{str(len(str(_el))).zfill(2)}'
                obj_ += cc.shuffle(str_in=obj_[:20],
                                   key_in=0.0,
                                   direction=False)
                # shuffle final results
                for _ in range(kwargs['decrypt_complexity']):
                    obj_ = cc.shuffle(str_in=obj_,
                                      key_in=0.0,
                                      direction=False)
                return obj_

            # if backward pop nail off if it matches
            elif kwargs['direction'] is False:
                # first step to take is descramble the incoming object, try 1e2 times
                unscramble_count = 0
                while (obj_[:20] !=
                       cc.shuffle(str_in=obj_[-20:],
                                  key_in=0.0,
                                  direction=True)):
                    obj_ = cc.shuffle(str_in=obj_,
                                      key_in=0.0,
                                      direction=True)
                    unscramble_count += 1
                    if unscramble_count > 1e2:
                        return (te.DecryptionException(
                            'No valid object to be decrypted can be established '
                            'from the input. Please ensure that the object to be '
                            'decrypted is entered correctly, is not '
                            'missing any specific element, and does not have any '
                            'additional elements than those which are part of '
                            'the originally encrypted object. If all of this has '
                            'been confirmed and this message is still arising '
                            'please check that leading quotes have not '
                            'been accidentally placed around the object '
                            '(in the first and last positions). This '
                            'error only pertains checking if a valid object '
                            'exists and does not contain any '
                            'information about any of the passwords/keys used '
                            'to encrypt this object, as they have not been '
                            'evaluated yet.'),
                                None)
                # find the number of metadata tags
                # find the initial position, ending base, and the starting base
                _ip = int(obj_[-22:-20])
                _eb = -22 - _ip
                _sb = _eb - int(obj_[-22 - _ip: -22])
                # return decryption object and metadata
                return obj_[:_sb], obj_[_sb:_eb]
            else:
                pass
        # args 0 must be sting of length>11
        _out = cc.shuffle(str_in=obj_[:10],
                          key_in=obj_[9:11],
                          direction=True)
        _static = ct.bin_str_get(
            ''.join(('0' if i % 2 == 1 else '1') * kwargs['byte_len_interior']
                    for i in range(
                9 +ord(_out[int(len(_out)/2)]) % 5)),
            kwargs['byte_len_interior'])
        _out = cc.shuffle(str_in=_out+_static,
                          key_in=_out[-6:],
                          direction=False)
        # if forward return nail as is
        if kwargs['direction'] is True:
            return _out
        # if backward pop nail off if it matches
        elif kwargs['direction'] is False:
            if obj_[-len(_out):] == _out:
                return obj_[:-len(_out)]
            else:
                return None
        # if no direction return obj_
        else:
            pass
    # inspect stack fail then return as is
    else:
        pass
    return obj_


# ----------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------ INTERNAL KEY LOOKUPS ------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

def hhasher(args):
    @functools.wraps(args)
    def hashed_key(self, *__args, **__kwargs):
        try:
            output = args(self, *__args, **__kwargs)
        except:
            output = secrets.randbelow(111111111)
        # if output is None:
        #     warnings.warn(f'Warning: Key is None, and may '
        #                   f'not be working as expected; please ensure '
        #                   f'that None is the desired return for the '
        #                   f'following key \n'
        #                   f' --> {str(self.__class__).split(".")[1]} \n'
        #                   f'Line warning occurred on: ',
        #                   UserWarning,
        #                   stacklevel=2)
        # return error if it exists
        if isinstance(output, te.ProgramException):
            return output
        return ct.hhash(output, mode='plain', hash_select=0, layers=0)
    return hashed_key


class key_os_id:
    # returns the id of the current operating system for a given key"""

    def __init__(self, *args, direction=False, **kwargs):
        self.direction = direction

    @hhasher
    def __call__(self, *args, **kwargs):
        # shortened notation for extracting paths
        gfn = lambda x: os.path.splitext(os.path.split(x.filename)[1])[0]
        # get stack
        try:
            _gs = inspect.stack()
        except:
            return secrets.randbelow(111111111)

        # # # # # # # evaluate call callers
        # callfuncs = [_gs[i].function for i in range(9)]
        # callfiles = [gfn(_gs[i]) for i in range(9)]
        # global global_func_list, global_file_list
        # global_func_list += [callfuncs]
        # global_file_list += [callfiles]
        # py - machineid
        # # print(callfiles, callfuncs)
        # # return True

        # passing stacks for class

        _ps = [
            [['__call__'], ['simple_lookups']],
            [['hashed_key'], ['simple_lookups']],
            [['key_set'], ['key_handler_cache']],
            [['set_all_keys', 'key_get'], ['key_handler_cache']],
            [['__init__', '_backward_middle_step'], ['key_handler_cache', 'step_manager']],
            [['__call__', '__init__'], ['key_handler_cache', 'step_manager']],
        ]


        # # init passing variable and loop through passing stack
        _p = True
        for i in enumerate(_ps):
            if i[1] == []:
                continue
            _p *= gfn(_gs[i[0]]) in i[1][1]
            _p *= _gs[i[0]].function in i[1][0]

        if bool(_p):
            # get the operating system UUID"""

            def _run(*__args):
                # runs command in command line
                try:
                    return subprocess.run(__args[0],
                                          shell=True,
                                          capture_output=True,
                                          check=True,
                                          encoding='utf-8'
                                          ).stdout.strip()
                except:
                    return None

            def _fileget(*__args):
                # file getter
                try:
                    with open(__args[0]) as f:
                        return f.read()
                except:
                    return None

            # init outgoing var
            _out = None

            # run system checks and attempt to get osid from command line
            if sys.platform == 'darwin':
                _out = _run("ioreg -d2 -c IOPlatformExpertDevice | "
                                "awk -F\\\" '/IOPlatformUUID/{print $(NF-1)}'")

            elif sys.platform in ('win32', 'cygwin', 'msys'):
                _out = _run("powershell.exe -ExecutionPolicy bypass -command ("
                                "Get-CimInstance -Class Win32_ComputerSystemProduct).UUID")
                if not _out:
                    _out = _run('wmic csproduct get osid').split('\n')[2].strip()

            elif sys.platform.startswith('linux'):
                _out = _fileget('/var/lib/dbus/machine-id')

                if not _out:
                    _out = _fileget('/etc/machine-id')

                if not _out:
                    cgroup = _fileget('/proc/self/cgroup')
                    if cgroup and 'docker' in cgroup:
                        _out = _run('head -1 /proc/self/cgroup | cut -d/ -f3')

                if not _out:
                    mountinfo = _fileget('/proc/self/mountinfo')
                    if mountinfo and 'docker' in mountinfo:
                        _out = _run("grep -oP '(?<=docker/containers/)([a-f0-9]+)"
                                        "(?=/hostname)' /proc/self/mountinfo")

                if not _out and 'microsoft' in platform.uname().release:
                    _out = _run("powershell.exe -ExecutionPolicy bypass -command '(Get-CimInstance "
                                    "-Class Win32_ComputerSystemProduct).UUID'")

            elif sys.platform.startswith(('openbsd', 'freebsd')):
                _out = _fileget('/etc/hostid')

                if not _out:
                    _out = _run('kenv -q smbios.system.osid')

            if _out is None:
                if self.direction:
                    return te.EncryptionException(f"Could not locate operating system "
                                                  f"ID on {sys.platform}")
                else:
                    return None

            return _out
        else:
            return secrets.randbelow(111111111)

    #
    # def _get_id(self, *args):
    #     # gest the operating system ID"""
    #
    #     def _run(*__args):
    #         # runs command in command line
    #         try:
    #             return subprocess.run(__args[0],
    #                                   shell=True,
    #                                   capture_output=True,
    #                                   check=True,
    #                                   encoding='utf-8'
    #                                   ).stdout.strip()
    #         except:
    #             return None
    #
    #     def _fileget(*__args):
    #         # file getter
    #         try:
    #             with open(__args[0]) as f:
    #                 return f.read()
    #         except:
    #             return None
    #
    #     # init outgoing var
    #     osid_out = None
    #
    #     # run system checks and attempt to get osid from command line
    #     if sys.platform == 'darwin':
    #         osid_out = _run("ioreg -d2 -c IOPlatformExpertDevice | "
    #                                   "awk -F\\\" '/IOPlatformUUID/{print $(NF-1)}'")
    #
    #     elif sys.platform in ('win32', 'cygwin', 'msys'):
    #         osid_out = _run("powershell.exe -ExecutionPolicy bypass -command ("
    #                                   "Get-CimInstance -Class Win32_ComputerSystemProduct).UUID")
    #         if not osid_out:
    #             osid_out = _run('wmic csproduct get osid').split('\n')[2].strip()
    #
    #     elif sys.platform.startswith('linux'):
    #         osid_out = _fileget('/var/lib/dbus/machine-id')
    #
    #         if not osid_out:
    #             osid_out = _fileget('/etc/machine-id')
    #
    #         if not osid_out:
    #             cgroup = _fileget('/proc/self/cgroup')
    #             if cgroup and 'docker' in cgroup:
    #                 osid_out = _run('head -1 /proc/self/cgroup | cut -d/ -f3')
    #
    #         if not osid_out:
    #             mountinfo = _fileget('/proc/self/mountinfo')
    #             if mountinfo and 'docker' in mountinfo:
    #                 osid_out = _run("grep -oP '(?<=docker/containers/)([a-f0-9]+)"
    #                                           "(?=/hostname)' /proc/self/mountinfo")
    #
    #         if not osid_out and 'microsoft' in platform.uname().release:
    #             osid_out = _run("powershell.exe -ExecutionPolicy bypass -command '(Get-CimInstance "
    #                                       "-Class Win32_ComputerSystemProduct).UUID'")
    #
    #     elif sys.platform.startswith(('openbsd', 'freebsd')):
    #         osid_out = _fileget('/etc/hostid')
    #
    #         if not osid_out:
    #             osid_out = _run('kenv -q smbios.system.osid')
    #
    #     if osid_out is None:
    #         if self.direction:
    #             return te.EncryptionException(f"Could not locate operating system "
    #                                      f"ID (os_id) on {sys.platform}")
    #         else:
    #             return None
    #
    #     return osid_out


# ---- INTERNET REQ ----

class key_url_request:

    def __init__(self, *args, direction=False, **kwargs):
        self.direction = direction

    @hhasher
    def __call__(self, *args, **kwargs):
        # shortened notation for extracting paths
        gfn = lambda x: os.path.splitext(os.path.split(x.filename)[1])[0]
        # get stack
        try:
            _gs = inspect.stack()
        except:
            return secrets.randbelow(111111111)

        # # # # # # # evaluate call callers
        # callfuncs = [_gs[i].function for i in range(9)]
        # callfiles = [gfn(_gs[i]) for i in range(9)]
        # global global_func_list, global_file_list
        # global_func_list += [callfuncs]
        # global_file_list += [callfiles]
        # # print(callfiles, callfuncs)
        # # # return True

        # passing stacks for class

        _ps = [
            [['__call__'], ['simple_lookups']],
            [['hashed_key'], ['simple_lookups']],
            [['key_set'], ['key_handler_cache']],
            [['key_get', 'set_all_keys'], ['key_handler_cache']],
            [['__init__', '_backward_middle_step'], ['key_handler_cache', 'step_manager']],
            [['__init__', '__call__'], ['key_handler_cache', 'step_manager']],
            ]

        # # init passing variable and loop through passing stack
        _p = True
        for i in enumerate(_ps):
            if i[1] == []:
                continue
            _p *= gfn(_gs[i[0]]) in i[1][1]
            _p *= _gs[i[0]].function in i[1][0]

        if bool(_p):
            # takes in a url list, reads in the contents of the link and returns it as a string"""

            # try to get contents of page(s) or return none
            try:
                # allow unverified ssl
                ssl._create_default_https_context = ssl._create_unverified_context

                # if it is a forward call then evaluate directly
                if self.direction:
                    return str([urllib.request.urlopen(i).read()
                                for i in tu.list_unpacker(args)])
                # if it is a backwards call then parse list string into url strings
                else:
                    return str([urllib.request.urlopen(i).read()
                                for i in
                                tu.list_unpacker(tu.str_arg_parser(args))])

            except Exception as e:
                if self.direction:
                    return te.EncryptionException(f"Could not connect to (all) the "
                                                  f"provided site(s) to retrieve "
                                                  f"a key: {args} \n"
                                                  f"{e}")
                else:
                    return None
        else:
            return secrets.randbelow(111111111)

        # return self._url_request(*args)
    #
    # def _url_request(self, *args):
    #     # takes in a url list, reads in the contents of the link and returns it as a string"""
    #
    #     # try to get contents of page(s) or return none
    #     try:
    #         # allow unverified ssl
    #         ssl._create_default_https_context = ssl._create_unverified_context
    #
    #         # if it is a forward call then evaluate directly
    #         if self.direction:
    #             return str([urllib.request.urlopen(i).read()
    #                         for i in tu.list_unpacker(args)])
    #         # if it is a backwards call then parse list string into url strings
    #         else:
    #             return str([urllib.request.urlopen(i).read()
    #                         for i in
    #                         tu.list_unpacker(tu.str_arg_parser(args))])
    #
    #     except Exception as e:
    #         if self.direction:
    #             return te.EncryptionException(f"Could not connect to (all) the "
    #                                          f"provided site(s) to retrieve "
    #                                          f"a key: {args} \n"
    #                                          f"{e}")
    #         else:
    #             return None



# ---- IP ----
class key_public_ip:

    def __init__(self, *args, direction=False, **kwargs):

        self.direction = direction

    @hhasher
    def __call__(self, *args, **kwargs):
        # shortened notation for extracting paths
        gfn = lambda x: os.path.splitext(os.path.split(x.filename)[1])[0]
        # get stack
        try:
            _gs = inspect.stack()
        except:
            return secrets.randbelow(111111111)

        # # # # # # # evaluate call callers
        # callfuncs = [_gs[i].function for i in range(9)]
        # callfiles = [gfn(_gs[i]) for i in range(9)]
        # global global_func_list, global_file_list
        # global_func_list += [callfuncs]
        # global_file_list += [callfiles]
        # # print(callfiles, callfuncs)
        # # # return True

        # passing stacks for class

        _ps = [
            [['__call__'], ['simple_lookups']],
            [['hashed_key'], ['simple_lookups']],
            [['key_set'], ['key_handler_cache']],
            [['set_all_keys', 'key_get'], ['key_handler_cache']],
            [['_backward_middle_step', '__init__'], ['key_handler_cache', 'step_manager']],
            [['__init__', '__call__'], ['key_handler_cache', 'step_manager']],
        ]

        # # init passing variable and loop through passing stack
        _p = True
        for i in enumerate(_ps):
            if i[1] == []:
                continue
            _p *= gfn(_gs[i[0]]) in i[1][1]
            _p *= _gs[i[0]].function in i[1][0]

        if bool(_p):
            # once the same ip has occurred twice then it is valid, searches for ipv4
            # ck these in a try loop (that breaks once it hits 2+ same), add a timeout"""
            # anon function read in site contents
            read_site = lambda x: [urllib.request.urlopen(x).read()] + [urllib.request.urlopen(x).getheaders()]
            # anon function to take in many objects and convert to string
            to_str = lambda x: ''.join(str(i) for i in tu.list_unpacker([x]))
            # anon function to parse out all ip info
            ip_read = lambda x: re.findall("([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)", str(x))
            # anon function to scrape any ipv4 address from a given page
            get_ip = lambda x: ip_read(to_str(read_site(x)))

            # list of websites that display public ip of sender
            site_list = ['https://checkip.amazonaws.com', 'https://www.wikipedia.org', 'https://ifconfig.me/',
                         'https://ipecho.net/', 'https://api.ipify.org/', 'https://icanhazip.com/',
                         'https://ifconfig.co/ip', 'https://ipecho.net/plain', 'https://ipinfo.io/ip']

            # shuffle the site list so that the program doesn't hit the same ones in the same order
            start_value = secrets.randbelow(len(site_list))
            site_list = [site_list[(i + start_value) % len(site_list)] for i in range(len(site_list))]
            # initiate the list of ips collected
            ip_list = []

            # loop through the sites and collect the ips, break when there are two of the same
            for i in site_list:
                # try to grab the ip, if there is any connection issue then move to the next site
                try:
                    ip_list.extend(get_ip(i))
                except urllib.error.URLError:
                    continue

                # if n public ip shows up twice or more then return it
                if collections.Counter(ip_list).most_common(1)[0][1] > 1:
                    return collections.Counter(ip_list).most_common(1)[0][0]

            # if there is not a public ip that showed up twice then evaluate how to handle
            if self.direction:
                return te.EncryptionException('The Current Public IPv4 address is '
                                              'required by the program, but cannot '
                                              'be found. Please check that this '
                                              'device has an internet connection, '
                                              'and a stable IPv4 address')
            else:
                return None
        else:
            return secrets.randbelow(111111111)


    #
    #     return self._public_ip()
    #
    # def _public_ip(self):
    #     # once the same ip has occurred twice then it is valid, searches for ipv4
    #     # ck these in a try loop (that breaks once it hits 2+ same), add a timeout"""
    #     # anon function read in site contents
    #     read_site = lambda x: [urllib.request.urlopen(x).read()] + [urllib.request.urlopen(x).getheaders()]
    #     # anon function to take in many objects and convert to string
    #     to_str = lambda x: ''.join(str(i) for i in tu.list_unpacker([x]))
    #     # anon function to parse out all ip info
    #     ip_read = lambda x: re.findall("([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)", str(x))
    #     # anon function to scrape any ipv4 address from a given page
    #     get_ip = lambda x: ip_read(to_str(read_site(x)))
    #
    #     # list of websites that display public ip of sender
    #     site_list = ['https://checkip.amazonaws.com', 'https://www.wikipedia.org', 'https://ifconfig.me/',
    #                  'https://ipecho.net/', 'https://api.ipify.org/', 'https://icanhazip.com/',
    #                  'https://ifconfig.co/ip', 'https://ipecho.net/plain', 'https://ipinfo.io/ip']
    #
    #     # shuffle the site list so that the program doesn't hit the same ones in the same order
    #     start_value = secrets.randbelow(len(site_list))
    #     site_list = [site_list[(i + start_value) % len(site_list)] for i in range(len(site_list))]
    #     # initiate the list of ips collected
    #     ip_list = []
    #
    #     # loop through the sites and collect the ips, break when there are two of the same
    #     for i in site_list:
    #         # try to grab the ip, if there is any connection issue then move to the next site
    #         try:
    #             ip_list.extend(get_ip(i))
    #         except urllib.error.URLError:
    #             continue
    #
    #         # if n public ip shows up twice or more then return it
    #         if collections.Counter(ip_list).most_common(1)[0][1] > 1:
    #             return collections.Counter(ip_list).most_common(1)[0][0]
    #
    #     # if there is not a public ip that showed up twice then evaluate how to handle
    #     if self.direction:
    #         return te. EncryptionException('The Current Public IPv4 address is '
    #                                       'required by the program, but cannot '
    #                                       'be found. Please check that this '
    #                                       'device has an internet connection, '
    #                                       'and a stable IPv4 address')
    #     else:
    #         return None


class key_timing:

    def __init__(self, *args, direction=False, **kwargs):
        self.direction = direction

    @hhasher
    def __call__(self, *args, **kwargs):

        # shortened notation for extracting paths
        gfn = lambda x: os.path.splitext(os.path.split(x.filename)[1])[0]
        # get stack
        try:
            _gs = inspect.stack()
        except:
            return secrets.randbelow(111111111)

        # # # # # # # evaluate call callers
        # callfuncs = [_gs[i].function for i in range(9)]
        # callfiles = [gfn(_gs[i]) for i in range(9)]
        # global global_func_list, global_file_list
        # global_func_list += [callfuncs]
        # global_file_list += [callfiles]
        # # print(callfiles, callfuncs)
        # # # return True

        # passing stacks for class

        _ps = [
            [['__call__'], ['simple_lookups']],
            [['hashed_key'], ['simple_lookups']],
            [['key_set'], ['key_handler_cache']],
            [['set_all_keys', 'key_get'], ['key_handler_cache']],
            [['_backward_middle_step', '__init__'], ['key_handler_cache', 'step_manager']],
            [['__call__', '__init__'], ['key_handler_cache', 'step_manager']],
            ]


        # # init passing variable and loop through passing stack
        _p = True
        for i in enumerate(_ps):
            if i[1] == []:
                continue
            _p *= gfn(_gs[i[0]]) in i[1][1]
            _p *= _gs[i[0]].function in i[1][0]

        if bool(_p):
            if self.direction is True:
                if isinstance(
                        self.key_timing_set(*args, **kwargs),
                        te.ProgramException):
                    return self.key_timing_set(*args, **kwargs)
                else:
                    return 0
            elif self.direction is False:
                args = tu.str_arg_parser(args)
                st = args[0][0]
                et = args[0][1]
                # getting timing"""
                tf = lambda x: abs(int(abs(cmath.sqrt(x + 1)) * (cmath.pi - cmath.log(x).imag)))
                try:
                    return tf(time.time() - et) + tf(st - time.time())
                except ValueError:
                    time.sleep(5e-7)
                    return tf(time.time() - et) + tf(st - time.time())
            else:
                return secrets.randbelow(111111111)


    # def _key_timing_establish(self, *args, **kwargs):
    #     if isinstance(
    #             self.key_timing_set(*args, **kwargs),
    #             te.ProgramException):
    #         return self.key_timing_set(*args, **kwargs)
    #     return 0

    @staticmethod
    def key_timing_set(*args, **kwargs):

        # shortened notation for extracting paths
        gfn = lambda x: os.path.splitext(os.path.split(x.filename)[1])[0]
        # get stack
        try:
            _gs = inspect.stack()
        except:
            return secrets.randbelow(111111111)

        # # # # # # # evaluate call callers
        # callfuncs = [_gs[i].function for i in range(6)]
        # callfiles = [gfn(_gs[i]) for i in range(6)]
        # global global_func_list, global_file_list
        # global_func_list += [callfuncs]
        # global_file_list += [callfiles]
        # # print(callfiles, callfuncs)
        # # # return True

        # passing stacks for class

        _ps = [
            [['key_timing_set'], ['simple_lookups']],
            [['__call__', 'forward_step_plan'], ['simple_lookups', 'step_manager']],
            [['__init__', 'hashed_key'], ['simple_lookups', 'step_manager']],
        ]

        # # init passing variable and loop through passing stack
        _p = True
        for i in enumerate(_ps):
            if i[1] == []:
                continue
            _p *= gfn(_gs[i[0]]) in i[1][1]
            _p *= _gs[i[0]].function in i[1][0]

        if not bool(_p):
            _out = [time.time() + 100 + secrets.randbelow(11111)]
            return _out

        # The set_expiration_time function takes in a user specified expiration time,
        # idates it, and returns it as a unix timestamp"""
        if 'expiration_time' not in kwargs.keys():
            kwargs['expiration_time'] = args[0]

        # establish the format of the input and how to handle it
        try:
            # allow any float-like objects to be interpreted as a float
            expt_obj_in = float(kwargs['expiration_time'])

        except TypeError:
            # see that user gave a list, tuple, or set, return as list
            if type(kwargs['expiration_time']) in (list, set, tuple):
                try:
                    expt_obj_in = [int(i) for i in kwargs['expiration_time']]
                except ValueError:
                    return te.EncryptionException(f'User provided expiration time of type'
                                            f' {type(kwargs["expiration_time"])} with elements of'
                                              f' {", ".join(type(i) for i in kwargs["expiration_time"])}, '
                                              f'type but the program can only handle types with a single element as: '
                                              f'float, int, decimal.Decimal, str, and multiple elements as: '
                                              f'list, set, tuple')


            # see if user gave datetime obj, return it as a list
            elif type(kwargs['expiration_time']) == datetime.datetime:
                expt_obj_in = list(kwargs['expiration_time'].timetuple())[:6]

            # type catch for anything that the program cannot evaluate
            else:
                return te.EncryptionException(f'User provided expiration time of type'
                                             f' {type(kwargs["expiration_time"])}, '
                                          f'but the program can only handle types with a single element as: '
                                          f'float, int, decimal.Decimal, str, and multiple elements as: list, set, '
                                          f'tuple')

        # process the entry into a unix time
        # if just a single float is received then pass that on
        if type(expt_obj_in) == float:
            # if len is one assume it is a unix time. set the milliseconds and return
            expt_unix = kwargs['expiration_time'] + secrets.randbelow(1000)/1e3

        # if it is a list with seven or less elements
        elif type(expt_obj_in) == list and len(expt_obj_in) < 8:
            # if len is between 2 and 7 then assume that is a datetime obj capable list,
            # assumed order [yyyy, mm, dd, hh, mm, ss, (mmmmmm)]
            # initiate base reference time list to some microseconds into epoch
            base_dt_list = [1970, 1, 1, 0, 0, 0, secrets.randbelow(int(1e6))]
            # replace base datetime with user supplied values TODO check that this logic is correct in this line
            expt_in = kwargs['expiration_time'] + base_dt_list[len(kwargs['expiration_time']):]
            # get utc datetime obj from this and catch if the user entered a nonacceptable format
            try:
                expt_utc = datetime.datetime(*expt_in).astimezone(datetime.timezone.utc)
            except ValueError as error_msg:
                te.EncryptionException(f'The program cannot convert the provided expiration time ('
                                    f'{", ".join(str(i) for i in expt_in)}) into the corresponding '
                                    f'unix time: {error_msg}')
            # set this into unix time
            expt_unix = calendar.timegm(expt_utc.utctimetuple())

        else:
            return te.EncryptionException(f'User provided expiration time ({expt_obj_in}) with too many elements '
                                      f'({len(expt_obj_in)}), please enter time again with 7 or less elements')

        # check that the generated time is not in the past, if it is return an exception to the user
        if expt_unix < time.time():
            return te.EncryptionException(f'User provided expiration time that has already expired. \n'
                                          f'Current unix time is {int(time.time())} and the entered time '
                                          f'is {expt_unix} \n'
                                          f'Please choose a date & time in the future')

        # setting the start time, this is currently implemented as being 5 mins before this moment, this should be
        # enough time for threads, async, and processes to catch up
        startt_unix = round(time.time(), 6) - 3e2

        # if the time is set and all the validation passes then return the expiration time to the program
        return [startt_unix, expt_unix]

    # @staticmethod
    # def _key_timing_get(*args):
        # args = tu.str_arg_parser(args)
        # st = args[0][0]
        # et = args[0][1]
        # # getting timing"""
        # tf = lambda x: abs(int(abs(cmath.sqrt(x+1)) * (cmath.pi - cmath.log(x).imag)))
        # try:
        #     return tf(time.time() - et) + tf(st - time.time())
        # except ValueError:
        #     time.sleep(5e-7)
        #     return tf(time.time() - et) + tf(st - time.time())


 # ---- FILE BASED ----

class key_filedir:

    # returns an id for a given file or directory"""

    def __init__(self, *args, direction=False, **kwargs):
        # self._args = args
        # self._kwargs = kwargs
        self.direction = direction

    @hhasher
    def __call__(self, path_in, *args, **kwargs):
        # shortened notation for extracting paths
        gfn = lambda x: os.path.splitext(os.path.split(x.filename)[1])[0]
        # get stack
        try:
            _gs = inspect.stack()
        except:
            return secrets.randbelow(111111111)

        # # # # # # # evaluate call callers
        # callfuncs = [_gs[i].function for i in range(9)]
        # callfiles = [gfn(_gs[i]) for i in range(9)]
        # global global_func_list, global_file_list
        # global_func_list += [callfuncs]
        # global_file_list += [callfiles]
        # # print(callfiles, callfuncs)
        # return True

        # passing stacks for class

        _ps = [
            [['__call__'], ['simple_lookups']],
            [['hashed_key'], ['simple_lookups']],
            [['key_set'], ['key_handler_cache']],
            [['key_get', 'set_all_keys'], ['key_handler_cache']],
            [['__init__', '_backward_middle_step'], ['key_handler_cache', 'step_manager']],
            [['__init__', '__call__'], ['key_handler_cache', 'step_manager']],
        ]

        # init passing variable and loop through passing stack
        _p = True
        for i in enumerate(_ps):
            if i[1] == []:
                continue
            _p *= gfn(_gs[i[0]]) in i[1][1]
            _p *= _gs[i[0]].function in i[1][0]

        if bool(_p):
            def _hhash_file(_path_in):
                # read in any file to binary content"""
                with open(_path_in, mode='br') as f:
                    binary_out = f.read()
                return {
                    '/' + os.path.split(_path_in)[1]:
                        ct.hhash(binary_out, mode='plain', hash_select=0, layers=0)}

            def _hhash_dir(_path_in):
                # read in all files of a directory and return relative paths and binary data in a dict"""
                _path_in = pathlib.Path(_path_in).resolve()
                # allow windows paths to have forward slashes
                if isinstance(_path_in, pathlib.WindowsPath):
                    # get a list of all files in directory and subdirectories
                    path_walk = [i for i in pathlib.Path(_path_in.as_posix()).rglob('*') if os.path.isfile(i)]
                    # read every file into a dictionary value, set the dictionary key as the relative path
                    all_files = {str(i.as_posix()).split(str(_path_in.as_posix()))[1]: _hhash_file(i) for i in
                                 path_walk}
                    # all_files['_key_filedir_hhash_dir_basepath'] = str(_path_in.as_posix())
                # for other file systems
                else:
                    # get a list of all files in directory and subdirectories
                    path_walk = [i for i in pathlib.Path(_path_in).rglob('*') if os.path.isfile(i)]
                    # read every file into a dictionary value, set the dictionary key as the relative path
                    all_files = {str(i).split(str(_path_in))[1]: _hhash_file(i) for i in path_walk}
                    # all_files['_key_filedir_hhash_dir_basepath'] = str(_path_in)
                return all_files

            if self.direction:
                if os.path.isfile(path_in):
                    return _hhash_file(path_in)
                elif os.path.isdir(path_in):
                    return _hhash_dir(path_in)
                else:
                    return te.EncryptionException(f'The directory/file key was provided with the following path, '
                                                  f'but it is not an existing directory or file: \n{path_in}')
            else:
                if os.path.isfile(path_in):
                    try:
                        return _hhash_file(path_in)
                    except:
                        return None
                elif os.path.isdir(path_in):
                    try:
                        return _hhash_dir(path_in)
                    except:
                        return None
                else:
                    return None
        else:
            return secrets.randbelow(111111111)
    #
    # def _filedir(self, path_in):
    #
    #     def _hhash_file(path_in):
    #         # read in any file to binary content"""
    #         with open(path_in, mode='br') as f:
    #             binary_out = f.read()
    #         return {
    #             '/' + os.path.split(path_in)[1]:
    #                 ct.hhash(binary_out, mode='plain', hash_select=0, layers=0)}
    #
    #     def _hhash_dir(path_in):
    #         # read in all files of a directory and return relative paths and binary data in a dict"""
    #         path_in = pathlib.Path(path_in).resolve()
    #         # allow windows paths to have forward slashes
    #         if isinstance(path_in, pathlib.WindowsPath):
    #             # get a list of all files in directory and subdirectories
    #             path_walk = [i for i in pathlib.Path(path_in.as_posix()).rglob('*') if os.path.isfile(i)]
    #             # read every file into a dictionary value, set the dictionary key as the relative path
    #             all_files = {str(i.as_posix()).split(str(path_in.as_posix()))[1]: _hhash_file(i) for i in
    #                          path_walk}
    #             # all_files['_key_filedir_hhash_dir_basepath'] = str(path_in.as_posix())
    #         # for other file systems
    #         else:
    #             # get a list of all files in directory and subdirectories
    #             path_walk = [i for i in pathlib.Path(path_in).rglob('*') if os.path.isfile(i)]
    #             # read every file into a dictionary value, set the dictionary key as the relative path
    #             all_files = {str(i).split(str(path_in))[1]: _hhash_file(i) for i in path_walk}
    #             # all_files['_key_filedir_hhash_dir_basepath'] = str(path_in)
    #         return all_files
    #
    #     if self.direction:
    #         if os.path.isfile(path_in):
    #             return _hhash_file(path_in)
    #         elif os.path.isdir(path_in):
    #             return _hhash_dir(path_in)
    #         else:
    #             return te.EncryptionException(f'The directory/file key was provided with the following path, '
    #                                           f'but it is not an existing directory or file: \n{path_in}')
    #     else:
    #         if os.path.isfile(path_in):
    #             try:
    #                 return _hhash_file(path_in)
    #             except:
    #                 return None
    #         elif os.path.isdir(path_in):
    #             try:
    #                 return _hhash_dir(path_in)
    #             except:
    #                 return None
    #         else:
    #             return None


# ---- python version ----

class key_python_version:

    def __init__(self, *args, **kwargs):
        pass

    @hhasher
    def __call__(self, *args, **kwargs):
        # shortened notation for extracting paths
        gfn = lambda x: os.path.splitext(os.path.split(x.filename)[1])[0]
        # get stack
        try:
            _gs = inspect.stack()
        except:
            return secrets.randbelow(111111111)

        # # # # # # # evaluate call callers
        # callfuncs = [_gs[i].function for i in range(9)]
        # callfiles = [gfn(_gs[i]) for i in range(9)]
        # global global_func_list, global_file_list
        # global_func_list += [callfuncs]
        # global_file_list += [callfiles]
        # # print(callfiles, callfuncs)
        # return True

        # passing stacks for class

        _ps = [[['__call__'], ['simple_lookups']],
               [['hashed_key'], ['simple_lookups']],
               [['key_set'], ['key_handler_cache']],
               [['set_all_keys', 'key_get'], ['key_handler_cache']],
               [['__init__', '_backward_middle_step'], ['step_manager', 'key_handler_cache']],
               [['__init__', '__call__'], ['step_manager', 'key_handler_cache']],
               ]

        # init passing variable and loop through passing stack
        _p = True
        for i in enumerate(_ps):
            if i[1] == []:
                continue
            _p *= gfn(_gs[i[0]]) in i[1][1]
            _p *= _gs[i[0]].function in i[1][0]

        if bool(_p):
            _out = '.'.join(str(i) for i in sys.version_info[:3])
        else:
            _out = secrets.randbelow(111111111)
        return _out

# ---- default key ----

class key_default:
    # the program default key"""

    def __init__(self, *args, **kwargs):
        pass

    @hhasher
    def __call__(self, *args, **kwargs):
        # call matcher --> boolean logic goes here

        # shortened notation for extracting paths
        gfn = lambda x: os.path.splitext(os.path.split(x.filename)[1])[0]
        # get stack
        try:
            _gs = inspect.stack()
        except:
            return secrets.randbelow(111111111)

        # # # # # # # evaluate call callers
        # callfuncs = [_gs[i].function for i in range(9)]
        # callfiles = [gfn(_gs[i]) for i in range(9)]
        # global global_func_list, global_file_list
        # global_func_list += [callfuncs]
        # global_file_list += [callfiles]
        # # print(callfiles, callfuncs)
        # return True

        # passing stacks for class

        _ps = [
             [['__call__'], ['simple_lookups']],
             [['hashed_key'], ['simple_lookups']],
             [['key_set'], ['key_handler_cache']],
             [['set_all_keys'], ['key_handler_cache']],
             [['__init__', '_backward_first_step'], ['key_handler_cache', 'step_manager']],
             [['__init__', '__call__'], ['key_handler_cache', 'step_manager']],
        ]

        # init passing variable and loop through passing stack
        _p = True
        for i in enumerate(_ps):
            if i[1] == []:
                continue
            _p *= gfn(_gs[i[0]]) in i[1][1]
            _p *= _gs[i[0]].function in i[1][0]

        if bool(_p):
            _out = str(1 + secrets.randbelow(args[0]))
        else:
            _out = secrets.randbelow(111111111)
        return _out


# ----------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------ EXTERNAL KEY LOOKUPS ------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

class key_custom:

    __slots__ = ()

    def __init__(self, *args, **kwargs):
        pass

    @hhasher
    def __call__(self, *args, **kwargs):
        # call matcher --> boolean logic goes here

        # shortened notation for extracting paths
        gfn = lambda x: os.path.splitext(os.path.split(x.filename)[1])[0]
        # get stack
        try:
            _gs = inspect.stack()
        except:
            return secrets.randbelow(111111111)

        # # # # # # # evaluate call callers
        # callfuncs = [_gs[i].function for i in range(9)]
        # callfiles = [gfn(_gs[i]) for i in range(9)]
        # global global_func_list, global_file_list
        # global_func_list += [callfuncs]
        # global_file_list += [callfiles]
        # # print(callfiles, callfuncs)
        # # return True

        # passing stacks for class

        _ps = [[['__call__'], ['simple_lookups']],
               [['hashed_key'], ['simple_lookups']],
               [['key_set'], ['key_handler_cache']],
               [['set_all_keys'], ['key_handler_cache']],
               [['__init__', '_backward_first_step'], ['step_manager', 'key_handler_cache']],
               [['__init__', '__call__'], ['step_manager', 'key_handler_cache']]
               ]

        # init passing variable and loop through passing stack
        _p = True
        for i in enumerate(_ps):
            if i[1] == []:
                continue
            _p *= gfn(_gs[i[0]]) in i[1][1]
            _p *= _gs[i[0]].function in i[1][0]

        if bool(_p):
            _out = pickle.dumps(args) + pickle.dumps(kwargs)
        else:
            _out = secrets.randbelow(111111111)

        return _out

    #     return self._custom_key(*args, **kwargs)
    #
    # @staticmethod
    # def _custom_key(*args, **kwargs):
    #     return

# if __name__ == '__main__':
#     print('running', __file__)
#     aa = retrieve_key(direction=True, get_item='func', key_id=1)
#     bb = aa(1)
#     print(bb)
#     zz = retrieve_key(direction=True, get_item='func', key_id=2)()
#     print(zz)
#     retrieve_key(direction=True, get_item='func', key_id=5)([2025, 3])
#     # retrieve_key(direction=True, get_item='func', key_id=5)(1708139888)
#     print(bb)
#
#

# eof
