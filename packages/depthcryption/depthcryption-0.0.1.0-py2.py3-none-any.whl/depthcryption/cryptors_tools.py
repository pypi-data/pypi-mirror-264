"""
The DepthCryption.cryptor_tools module houses the technical tools
required to support the encryption and decryption functions, and
logic within the cryptor_cryptor module. The internal functions
here in this sense perform a lot of the 'heavy lifting' of the
program and are continuously used whenever the actual encryption
and decryption functions are invoked. This module in and of itself
is only responsible for housing these tools for the
cryptors_cryptors module.

The following classes and functions are publicly available:
--------------
None

The following classes and functions are internally available to the program:
--------------
shift_get: Encryption and decryption core technical implementation,
    please see function documentation for further information.
shuffle_get_mul: Encryption and decryption core technical implementation,
    please see function documentation for further information.
shuffle_get_mod: Encryption and decryption core technical implementation,
    please see function documentation for further information.
shuffle_get_cyc: Encryption and decryption core technical implementation,
    please see function documentation for further information.
substitute_get: Encryption and decryption core technical implementation,
    please see function documentation for further information.
str_bin_get: Encryption and decryption core technical implementation,
    please see function documentation for further information.
bin_str_get: Encryption and decryption core technical implementation,
    please see function documentation for further information.
hhash: Encryption and decryption core technical implementation,
    please see function documentation for further information.

"""

# standard
import itertools
import typing

# local
from . import simple_lookups as sl
from . import tools_exceptions as te
from . import tools_utils as tu

# -------- Shifting --------


def shift_get(str_in: str,
              shift_val: int,
              byte_len: int = 8,
              ) -> str:
    """
    Shifts a single string element a number of positions through utf-8.

    :param str_in: Incoming character to be operated on.
    :type str_in: str
    :param shift_val: The number of utf-8 positions to shift str_in.
    :type shift_val: int
    :param byte_len: Number of bits per byte.
    :type byte_len: int
    :returns: A shifted single utf-8 string.
    :rtype: str
    """

    # establish ranges and make shift call
    str_min = 0
    str_max = 2**byte_len
    return chr((((ord(str_in) + shift_val) - str_min) % str_max) + str_min)

# -------- Shuffling --------


def shuffle_get_mul(str_in: str,
                    key_in: object,
                    byte_len: int = 8,
                    ) -> list[int,]:
    """
    Get an iterable's shuffled indexing using multiplicative math.

    :param str_in: Incoming string to be referenced from.
    :type str_in: str
    :param key_in: Object to establish shuffled value patterns.
    :type key_in: object
    :param byte_len: Number of bits per byte.
    :type byte_len: int
    :returns: A list of shuffled integer indices.
    :rtype: list
    """

    # convert key into a list of integers
    hashed_key = hhash(key_in,
                       layers=-len(str_in),
                       mode='single_scramble_str')
    shuffled_i = map(lambda x: float(hashed_key[x:x+3])/1e3,
                     range(len(hashed_key)))
    # generate a list of indices to have the shuffling applied to
    order_out = list(range(len(str_in)))
    # pop incoming string elements in order of the shuffle into outgoing list
    return list(
        order_out.pop(int(len(order_out) * next(shuffled_i)))
        for _ in str_in)


def shuffle_get_mod(str_in: str,
                    key_in: object,
                    byte_len: int = 8,
                    ) -> list[int,]:
    """
    Get an iterable's shuffled indexing using modulo math.

    :param str_in: Incoming string to be referenced from.
    :type str_in: str
    :param key_in: Object to establish shuffled value patterns.
    :type key_in: object
    :param byte_len: Number of bits per byte.
    :type byte_len: int
    :returns: A list of shuffled integer indices.
    :rtype: list
    """

    # convert key into a list of integers
    hashed_key = hhash(key_in,
                       layers=-len(str_in),
                       mode='single_scramble_str')
    shuffled_i = map(lambda x: int(hashed_key[x:x+3])*1e3,
                     range(len(hashed_key)))
    # generate a list of indices to have the shuffling applied to
    order_out = list(range(len(str_in)))
    # pop incoming string elements in order of the shuffle into outgoing list
    return list(
        order_out.pop(int(next(shuffled_i) % len(order_out)))
        for _ in str_in)


def shuffle_get_cyc(str_in: typing.Union[str, list,],
                    key_in: object,
                    byte_len: int = 8,
                    ) -> list[int,]:
    """
    Get an iterable's shuffled indexing using cyclic indexing.
    Significantly lighter weight than shuffle_get_mul and
    shuffle_get_mod, but slightly less random. Intended for
    larger shuffles (elements>500). If the number of incoming
    elements is less than 500, shuffle_get_mod is called directly.

    :param str_in: Incoming string to be referenced from.
    :type str_in: str
    :param key_in: Object to establish shuffled value patterns.
    :type key_in: object
    :param byte_len: Number of bits per byte.
    :type byte_len: int
    :returns: A list of shuffled integer indices.
    :rtype: list
    """

    _sl = len(str_in)

    if _sl < 500:
        return shuffle_get_mod(str_in=str_in, key_in=key_in)

    # convert key into a list of integers
    hashed_key = hhash(key_in, layers=-_sl, mode='single_scramble_str')
    # create a reference set of unused indices
    unused = set(range(_sl))
    # init outgoing shuffled list
    order_out = list(itertools.accumulate(
        map(lambda x: 1 + int(hashed_key[x:x + 1]),
            range(1 + int(len(unused) / 8)))))
    # gather unused indices
    unused -= set(order_out)
    # make reference list of indices based from hhashed key
    acc_index_ref = list(itertools.accumulate(
        map(lambda x: 1 + int(hashed_key[x:x + 1]),
            range(1 + int(len(unused) / 9)))))
    counter = 0
    # largest step of two elements could be up to 20, stop operations at 55
    while len(unused) > 55:
        # get tuple of unused indices
        _tu = tuple(unused)
        # pull from back if even, front if odd, use the initialized
        # indices reference and truncate it, rather than recalculating
        if counter % 2 == 0:
            _il = [_tu[-i] for i in acc_index_ref[:int(len(unused) / 9)]]
        else:
            _il = [_tu[i] for i in acc_index_ref[:int(len(unused) / 9)]]
        # append the temporary index list into the outgoing shuffle
        order_out.extend(_il)
        # remove used indices from unused pile
        unused -= set(_il)
        counter += 1
    # bulk transport remaining elements and return
    return order_out + list(unused)

# -------- Substituting --------


def substitute_get(key_in: str,
                   direction: bool,
                   byte_len: int = 8,
                   sfunc: callable = shuffle_get_mul,
                   ) -> dict:
    """
    Create a new dictionary forward/backward mapping of utf-8 characters.

    :param key_in: Object to establish substituted value patterns.
    :type key_in: object
    :param direction: Forwards is True, backwards is False.
    :type direction: bool
    :param byte_len: Number of bits per byte.
    :type byte_len: int
    :param sfunc: Function to create the shuffled indices.
    :type sfunc: function
    :return: A dictionary of int mappings for utf-8 positions.
    :rtype: dict
    """

    if direction:
        return {i: j for i, j in enumerate(sfunc('0'*(2**byte_len), key_in))}
    else:
        return {j: i for i, j in enumerate(sfunc('0'*(2**byte_len), key_in))}

# -------- Scrambling --------
# - no internal tools established at this time

# -------- General --------


def str_bin_get(str_in: str,
                byte_len: int = 8,
                ) -> str:
    """
    Convert string to its utf-8 binary string.

    :param str_in: Incoming string to be referenced from.
    :type str_in: str
    :param byte_len: Number of bits per byte.
    :type byte_len: int
    :return: A binary string.
    :rtype: str
    """

    # get string binary, increase by 2 to account for insert '0b' string
    byte_in_2 = byte_len + 2
    zfiller = lambda x: x.zfill(byte_in_2)
    # return binary string and remove the 0b substring occurrences
    return ''.join(
        map(zfiller, map(bin, map(ord, str_in)))
    ).replace('0b', '')


def bin_str_get(bin_in: str,
                byte_len: int = 8,
                ) -> str:
    """
    Convert binary string to its utf-8 string.

    :param bin_in: Incoming binary string to be referenced from.
    :type bin_in: str
    :param byte_len: Number of bits per byte.
    :type byte_len: int
    :return: A utf-8 string.
    :rtype: str
    """

    return ''.join(chr(int(bin_in[i: i + byte_len], 2))
                   for i in range(0, len(bin_in), byte_len))


def hhash(*args: object,
          **kwargs: typing.Union[str, int,],
          ) -> typing.Union[str, int, list,]:
    """
    Heightened hash (hhash) function performs reiterative hashing of objects.

    :param args: All the objects that are to be hhashed.
    :param kwargs: Parameters that will determine how hashed layers
        operate, if layers are set to a negative number,
        single_evolve and single_evolve_str modes will run until they
        generate more values than the abs value of that input. Mode
        determines the internal functioning that the heightened
        hashing undertakes.

    :returns: The hhashed args, in format specified by mode.
    """

    # get core height function and initialized outgoing args
    hf, args_out = sl.HashContainer(**kwargs)(*args, **kwargs)

    # if the mode and layers kwargs are not provided then the
    # list of args with their corresponding hashes are established
    if ('mode' not in kwargs.keys() or
            kwargs['mode'] == 'plain' or
            'layers' not in kwargs.keys()):
        # if there is only a single element of args then
        # return only a single element
        if len(args_out) == 1:
            return args_out[0]
        # if there are multiple elements of kwargs return it as a list
        else:
            return args_out

    if kwargs['mode'] == 'deep_flat':
        # loop through each layer and perform a rehashing
        for _ in range(kwargs['layers']):
            args_out = list(map(lambda x: hf(str(x)), args_out))

    elif kwargs['mode'] == 'single_evolve':
        # perform rehashing on args_out for each layer
        # if layers is positive then interpret it as a loop count
        if kwargs['layers'] >= 0:
            [args_out.append(hf(args_out[-1]))
             for _ in range(kwargs['layers'])]
        # if layers is negative then run it till the count of values
        # in args_out is larger than the abs layers value
        else:
            while (len(''.join([str(i) for i in args_out])) <=
                   abs(kwargs['layers'])):
                args_out.append(hf(args_out[-1]))

    # returns a long string of the single has evolution,
    # this is zipped backwards before returning
    elif kwargs['mode'] == 'single_evolve_str':
        # perform rehashing on args_out for each layer
        # if layers is positive then interpret it as a loop count
        if kwargs['layers'] >= 0:
            [args_out.append(hf(args_out[-1]))
             for _ in range(kwargs['layers'])]
        # if layers is negative then run it till the count of values
        # in args_out is larger than the abs layers value
        else:
            while (len(''.join([str(i) for i in args_out])) <=
                   abs(kwargs['layers'])):
                args_out.append(hf(args_out[-1]))

        # perform a reverse zip of just the numbers
        reverse_zip_list = map(list,
                               itertools.zip_longest(
                                   *[[j for j in str(i)[::-1]]
                                     for i in reversed(args_out)],
                                   fillvalue='1'))
        args_out = ''.join(''.join(i) for i in reverse_zip_list)

    elif kwargs['mode'] == 'single_scramble_str':
        # quasi-random mode of producing a sufficiently long string of ints
        # note that this approach will eventually repeat after an extremely
        # long number of inputs, if required
        args_out = str(args_out[0])
        args_out += ''.join(reversed(args_out))
        target_len = len(args_out)*kwargs['layers'] if (
                kwargs['layers'] > 0) else (
            abs(kwargs['layers']))
        # check if a specified number of elements is already met
        if target_len <= len(args_out):
            return args_out
        # create a reference list of hhashes from existing hash str
        ref_list = tu.list_unpacker([[
            str(hf(args_out[i:i + j])) for i in range(len(args_out))]
            for j in range(16, 2, -1)])
        _rl = len(ref_list)
        # get an estimate length of how long a single element is
        ref_est_len = (len(ref_list[0]) +
                       len(ref_list[int(len(ref_list)/2)]) +
                       len(ref_list[-1]))/3

        # make list of steps tp be repeated
        step_list = [1 + int(args_out[i:i + 2])
                     for i in range(len(args_out))]
        # use target length to see how many elements are
        # needed against reference length to estimate
        # element count, remove some from estimate as padding

        est_len = int(target_len/ref_est_len)-3
        # lengthen step list to match the required count,
        # add three as padding
        step_list *= (3 + int(est_len / len(step_list)))
        # create indexer
        step_list = list(i % _rl for i in itertools.accumulate(step_list))

        # rebuild args out with the reference list and its indices
        args_out = ''.join(ref_list[i] for i in step_list)

        # check that it is of sufficient len, keep padding if not
        _cycle_index = 0
        while len(args_out) <= target_len:
            args_out += ref_list[_cycle_index % _rl]
            _cycle_index += 1

    else:
        raise te.InternalException(
            'hhash function not supplied with identifiable mode')

    # return layered hhash
    return args_out

# eof
