"""
The Depthcryption.tools_utils module houses the general
utility functions that are used throughout multiple
modules within the package. This module is responsible for
centralizing the general functions that could otherwise be
used in multiple locations, but would not be conceptually
organized to house these functions in a mix of several
places and be calling them from seemingly random and
different modules.

The following classes and functions are publicly available:
--------------
None

The following classes and functions are internally available to the program:
--------------
list_unpacker: Recursive list flattening.
pressor: Data compression approaches for the program.
write_out_file: Write out data automatically based on type.
write_out_directory Write out entire directory from a dict.
read_in_file: Read in a file automatically based on specified type.
read_in_directory: REad in entire directory into a dict.
random_sample_full: Randomly sample a list, ensuring all elements are used.
random_sample: Randomly sample a list, attempt to use all elements.
b85s: String set of base 85 B elements.
ex_prob: Example prob calculator, find attempts to achieve chance with prob.
convert_base_strtoint_arbitrary: Numerical base conversion -> str -> int
convert_base_inttostr_arbitrary: Numerical base conversion -> int -> str
str_arg_parser: Evaluate strings into their representative python objects.
get_ts_int: Get current timestamp as a string of integers.
get_ts_formatted: Get current string timestamp string, with local formatting.

"""

# standard
import ast
import datetime
import lzma
import math
import os
import pathlib
import secrets
import typing
import zlib
# local
from . import cryptors_tools as ct
from . import tools_exceptions as te


def list_unpacker(incoming_list: typing.Union[list, tuple,],
                  ) -> list:
    """
    Recursive function allows provides ordered flattening of arbitrarily
    nested permutations of lists, sets and tuples into a single
    outgoing list.

    :param incoming_list: Any level of nested lists/tuples/sets.
    :return: A flattened list.
    """

    # initiate the outgoing list
    outgoing_list = []

    # loop through the elements of the incoming list
    for i in incoming_list:
        # check if the element can be iterated upon and is not a string
        if type(i) in (list, set, tuple):
            # if the element is of list, set, or tuple type a recursive
            # function call is made for unpacking
            outgoing_list += list_unpacker(i)
        # if the current element is not of list type then append it
        # into the outgoing list
        else:
            outgoing_list.append(i)
    # once call is complete (recursive or not) then return the outgoing
    # list to the calling function
    return outgoing_list


def pressor(obj_in: bytes,
            compression: int,
            direction: bool,
            **kwargs: object,
            ) -> bytes:
    """
    Byte object compression system for whole program.

    :param obj_in: Single byte object for compression.
    :param compression: Int matching for compression type.
    :param direction: Compression/decompression call distinction,
        True/False booleans, respectively.
    :return: A (hopefully) compressed byte object.
    """

    # type check direction
    if not isinstance(direction, bool):
        raise te.InternalException(
            'A bool variable must be supplied to the '
            'pressor function direction argument.')

    if direction:
        try:
            # apply lzma compression
            if compression == 0:
                return lzma.compress(obj_in)
            # apply zip compression
            elif compression == 1:
                return zlib.compress(obj_in)
            else:
                raise te.InternalException(f'compression must be set '
                                           f'to either zlib or lzma, but '
                                           f'is instead set to '
                                           f'{compression}')
        except Exception as e:
            raise te.EncryptionException(f'Incoming object has failed '
                                         f'compression: {e}')
    else:
        try:
            # apply lzma decompression
            if compression == 0:
                return lzma.decompress(obj_in)
            # apply zip decompression
            elif compression == 1:
                return zlib.decompress(obj_in)
            else:
                raise te.InternalException(f'compression must be set '
                                           f'to either zlib (1) or '
                                           f'lzma (0), but '
                                           f'is instead set to '
                                           f'{compression}')
        except:
            return obj_in


def write_out_file(path_out: str,
                   obj_out: typing.Union[str, bytes, object,],
                   ) -> None:
    """
    Function to save object to file based on its type

    :param path_out: Where to save the file.
    :param obj_out: Object to be saved.
    :return: None.
    """
    if isinstance(obj_out, (str, int, float, complex)):
        with open(path_out, 'wt') as f:
            f.write(str(obj_out))
    else:
        with open(path_out, 'wb') as f:
            f.write(obj_out)


def write_out_directory(obj_out: dict[str, object,],
                        ) -> None:
    """
    Save a dict to a directory, key is path, value is object.

    :param obj_out: Dict to be saved.
    :return: None.
    """

    for i in obj_out.item():
        write_out_file(*i)


def read_in_file(path_in: typing.Union[str, pathlib.PurePath,],
                 is_str=False,
                 ) -> typing.Union[bytes, str,]:
    """
    Read in any file to string or binary content.

    :param path_in: Path of incoming file.
    :param is_str: True implies a string input is expected.
    :return: String or byte object read in from file (path_in).
    """

    # check if a string is to be read in
    if is_str:
        with open(path_in, mode='tr') as f:
            out_ = f.read()

    # else a byte object is to be read in
    else:
        with open(path_in, mode='br') as f:
            out_ = f.read()

    # return read in data
    return out_


def read_in_directory(path_in: typing.Union[str, pathlib.PurePath,],
                      ) -> typing.Dict[str, typing.Union[str, bytes,],]:
    """
    Read in all directory files, return relative paths + binary data as dict.

    :param path_in: A path to a directory.
    :return: A dict of the directory contents. Keys are relative file paths
        (relative from the provided path_in) and values are read in binary
        data.
    """
    # establish path
    path_in = pathlib.Path(path_in).resolve()
    # get a list of all files in directory and subdirectories
    path_walk = \
        [i for i in pathlib.Path(path_in).rglob('*') if os.path.isfile(i)]
    # read every file into a dictionary value,
    # set the dictionary key as the relative path
    all_files = {str(i).split(str(path_in))[1]: read_in_file(i)
                 for i in path_walk}
    # return dict
    return all_files


def random_sample_full(list_in: list,
                       n: int,
                       ) -> list:
    """
    Randomly sample a list n times, ensuring all elements are present.

    :param list_in: List to be sampled from.
    :param n: Number of return elements.
    :return: A random sampling of list_in with length n.
    """

    # check that the number of outgoing elements at least matches the
    # length of the incoming list such that all elements are represented
    if len(list_in) > n:
        raise te.InternalException(f'Cannot random sample list_in fully, '
                                   f'incoming list has {len(list_in)} '
                                   f'elements while the outgoing number of '
                                   f'elements must be {n}. \n'
                                   f'list_in >= n must be true')

    # generate outgoing list from permutations
    list_out = []
    while len(list_out) < n:
        list_out.extend([list_in[i] for i in
                         ct.shuffle_get_cyc(list_in,
                                            secrets.randbelow(int(1e11)))])
    # truncate list to desired length, reorder it and return
    list_out = list_out[:n]
    return [list_out[i] for i in ct.shuffle_get_cyc(
        list_out, secrets.randbelow(int(1e11)))]


def random_sample(list_in: list,
                  n: int,
                  ) -> list:
    """
    Randomly sample a list n times.

    :param list_in: List to be sampled from.
    :param n: Number of return elements.
    :return: A random sampling of list_in with length n.
    """

    # generate outgoing list from permutations of
    list_out = []
    while len(list_out) < n:
        list_out.extend([list_in[i] for i in
                         ct.shuffle_get_cyc(list_in,
                                            secrets.randbelow(int(1e11)))])

    # truncate list to desired length, reorder it and return
    list_out = list_out[:n]
    return [list_out[i] for i in ct.shuffle_get_cyc(
        list_out, secrets.randbelow(int(1e11)))]


def b85s() -> str:
    """
    Shorthand function call for B85B string set.

    :return: A sorted string of B85B string elements.
    """
    return ('!#$%&()*+-0123456789;<=>?@ABCDEFGHIJKLMNOPQ'
            'RSTUVWXYZ^_`abcdefghijklmnopqrstuvwxyz{|}~')


def ex_prob(x: typing.Union[int, float,],
            success_percent: float,
            ) -> int:
    """
    Example probability calculator for 1/x chances.

    :param x: Denominator in 1/x probability.
    :param success_percent: The chances of at least one success, wherein
        success_percent is the chance percentage, expressed as a decimal;
        ie 99% --> 0.99, 99.9% --> 0.999, 99.99% --> 0.9999, ect ...
    :return: Integer number of attempts to achieve success_percent with
        a probability denominator of 1/x.
    """

    return int(math.log(1 - success_percent) / math.log((x - 1) / x)) + 1


def convert_base_strtoint_arbitrary(value_in: str,
                                    charset=b85s(),
                                    ) -> int:
    """
    Utility function to convert values to provided character set
        (only works for positive values).

    :param value_in: Target value for conversion.
    :param charset: The desired outgoing character set and its ordering.
    :return: The value converted to its charset representation.
    """

    # unpack elements and init used values
    charset = [i for i in charset]
    value_in = [i for i in reversed(value_in)]
    csl = len(charset)
    value_out = 0

    # loop through each incoming value
    for i in range(len(value_in)):
        # append converted values to outgoing value
        value_out += charset.index(value_in[i]) * csl**i
    return value_out


def convert_base_inttostr_arbitrary(value_in: int,
                                    charset=b85s(),
                                    ) -> str:
    """
    Utility function to convert values to corresponding ints.

    :param value_in: Target value for conversion.
    :param charset: The desired outgoing character set and its ordering.
    :return: The value converted to its int.
    """

    # if the incoming value is larger than zero then calculate it
    if value_in > 0:
        csl = len(charset)
        value_out = ''
        while value_in > 0:
            value_out = f"{charset[value_in % csl]}{value_out}"
            value_in //= csl

    # if the incoming value is zero then return it as is
    else:
        value_out = charset[0]

    # return final calculated value
    return value_out


def str_arg_parser(*args: object,
                   ) -> list[str,]:
    """
    Utility function for ensuring that incoming arguements that
        are encapsulated in strings are appropriately handled as their
        native object types.

    :param args: Pending string arguments.
    :return: Appropriately interpreted objects.
    """

    # init outgoing elements and kick off loop
    args_out = []
    for i in args:

        # if it is a single length tuple give the object itself
        if isinstance(i, tuple) and len(i) == 1:

            # try to evaluate the argument if it needs evaluation
            try:
                _tmp = ast.literal_eval(i[0])
            # hand off as is if it is plain str
            except SyntaxError:
                _tmp = i[0]
            finally:
                args_out += [_tmp]

        elif isinstance(i, str):
            args_out += [ast.literal_eval(i)]

        else:
            raise te.InternalException('str_arg_parser must have inputs '
                                       'of str or tuple type')

    return args_out


def get_ts_int() -> str:
    """
    Get current local timestamp as an int string from years to milliseconds.

    :return: Int string of current time.
    """

    return datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')


def get_ts_formatted() -> str:
    """
    Get current timestamp formatted in local time sting.

    :return: Locally formatted current time string, years to milliseconds.
    """

    return datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')

# eof
