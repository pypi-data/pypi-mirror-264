"""
The DepthCryption.cryptor module houses the core internal logic for
how the program encrypts and decrypts objects. This module is
responsible for enacting the exact logic to encrypt and decrypt any
provided objects. To separate the core encryption and decryption
logic from some of the more technical aspects of the methodologies,
the precise tools needed for each crytion approach is migrated to
the cryptor_tools module, where appropriate. All functions in this
module must contain at least 4 inputs in the following order,
theses are described below:
-
str_in: The incoming 'string-like' to be altered.
key_in: The incoming key object that provides the altering pattern.
direction: True uses function for encrypting, False is for decrypting.
byte_len: How many bytes each element of str_in requires.
-

The following classes and functions are publicly available:
--------------
None

The following classes and functions are internally available to the program:
--------------
shift_linear: Encryption and decryption approach, please see function
    documentation for further information.
shift_recursive: Encryption and decryption approach, please see function
    documentation for further information.
shuffle: Encryption and decryption approach, please see function
    documentation for further information.
substitute: Encryption and decryption approach, please see function
    documentation for further information.
scramble_walk: Encryption and decryption approach, please see function
    documentation for further information.
scramble_shuffle: Encryption and decryption approach, please see function
    documentation for further information.
scramble_flip: Encryption and decryption approach, please see function
    documentation for further information.

"""

# local
from . import cryptors_tools as ct

# -------- Shifting --------
# ---- linear string shifting ----


def shift_linear(str_in: str,
                 key_in: object,
                 direction: bool,
                 byte_len: int = 8,
                 ) -> str:
    """
    Linearly forward/backward shifts every string element by key patterning.

    :param str_in: Incoming character to be operated on.
    :type str_in: str
    :param key_in: Object to establish shifting value patterns.
    :type key_in: object
    :param direction: Forwards is True, backwards is False.
    :type direction: bool
    :param byte_len: Number of bits per byte.
    :type byte_len: int
    :returns: A shifted utf-8 string.
    :rtype: str
    """

    # convert key into a list of integers, and apply all the shifts
    hashed_key = ct.hhash(key_in,
                          layers=-len(str_in),
                          mode='single_scramble_str')
    if direction:
        return ''.join(map(
            ct.shift_get, str_in,
            (int(hashed_key[i:i+3]) for i in range(len(hashed_key)))))
    else:
        return ''.join(map(ct.shift_get, str_in,
                           (-1 * int(hashed_key[i:i + 3]) for i in
                            range(len(hashed_key)))))

# ---- recursive string shifting ----


def shift_recursive(str_in: str,
                    key_in: object,
                    direction: bool,
                    byte_len: int = 8,
                    ) -> str:
    """
    Recursively forward shifts every string element with values from key.

    :param str_in: Incoming character to be operated on.
    :type str_in: str
    :param key_in: Object to establish shifting value patterns.
    :type key_in: object
    :param direction: Forwards is True, backwards is False.
    :type direction: bool
    :param byte_len: Number of bits per byte.
    :type byte_len: int
    :returns: A shifted utf-8 string.
    :rtype: str
    """

    # convert key into a list of integers
    hashed_key = ct.hhash(key_in,
                          layers=-len(str_in),
                          mode='single_scramble_str')
    shifts_list = [int(hashed_key[i:i+3]) for i in range(len(hashed_key))]
    # initiate outgoing string object with the first shift, loop through all
    if direction:
        obj_out = ct.shift_get(str_in[0], shifts_list[0])
        for i in range(1, len(str_in)):
            obj_out += ct.shift_get(
                str_in[i], shifts_list[i] + ord(str_in[i - 1]))
    else:
        obj_out = ct.shift_get(str_in[0], -shifts_list[0])
        for i in range(1, len(str_in)):
            obj_out += ct.shift_get(
                str_in[i], -(shifts_list[i] + ord(obj_out[i - 1])))
    return obj_out

# -------- Shuffling --------


def shuffle(str_in: str,
            key_in: object,
            direction: bool,
            byte_len: int = 8,
            sfunc: callable = ct.shuffle_get_cyc,
            ) -> str:
    """
    Apply a forward/backward shuffle to a string using the pattern from a key.

    :param str_in: Incoming string to be referenced from.
    :type str_in: str
    :param key_in: Object to establish shuffled value patterns.
    :type key_in: object
    :param direction: Forwards is True, backwards is False.
    :type direction: bool
    :param byte_len: Number of bits per byte.
    :type byte_len: int
    :param sfunc: Function to create the shuffled indices.
    :type sfunc: function
    :returns: A shuffled string.
    :rtype: str
    """

    # get a shuffle, apply it forward/backward, and return it
    if direction:
        return ''.join(str_in[i] for i in sfunc(str_in, key_in))
    else:
        return ''.join(list(zip(*sorted(zip(
            sfunc(str_in, key_in), str_in))))[1])

# -------- Substituting --------


def substitute(str_in: str,
               key_in: str,
               direction: bool,
               byte_len: int = 8,
               sfunc: callable = ct.shuffle_get_cyc,
               ) -> str:
    """
    Substitute string elements on utf-8 according to key.

    :param str_in: Incoming string to be referenced from.
    :type str_in: str:
    param key_in: Object to establish substituted value patterns.
    :type key_in: object
    :param direction: Forwards is True, backwards is False.
    :type direction: bool
    :param byte_len: Number of bits per byte.
    :type byte_len: int
    :param sfunc: Function to create the shuffled indices.
    :type sfunc: function
    :return: A string whose elements have been shuffled through utf-8 chars.
    :rtype: str
    """

    return str_in.translate(
        ct.substitute_get(key_in, direction, byte_len, sfunc))

# -------- Scrambling --------


def scramble_walk(str_in: str,
                  key_in: object,
                  direction: bool,
                  byte_len: int = 8,
                  ) -> str:
    """
    Apply a forward/backward scramble walk to str_in using key_in pattern.

    :param str_in: Incoming string to be referenced from.
    :type str_in: str
    :param key_in: Object to establish walk value patterns.
    :type key_in: object
    :param direction: Forwards is True, backwards is False.
    :type direction: bool
    :param byte_len: Number of bits per byte.
    :type byte_len: int
    :returns: A scrambled string.
    :rtype: str
    """

    # get string binary
    str_bin = ct.str_bin_get(str_in, byte_len)
    # get the walk value and walk the binary by that amount
    walk_val = int(str(ct.hhash(key_in))[-3:]) % len(str_bin)
    if direction:
        str_bin_walk = str_bin[walk_val:] + str_bin[:walk_val]
    else:
        str_bin_walk = str_bin[-walk_val:] + str_bin[:-walk_val]
    # return this reformulation as a new string
    return ct.bin_str_get(str_bin_walk, byte_len)


def scramble_shuffle(str_in: str,
                     key_in: object,
                     direction: bool,
                     byte_len: int = 8,
                     sfunc: callable = ct.shuffle_get_cyc,
                     ) -> str:
    """
    Apply a forward/backward scramble shuffle to str_in using key_in pattern.

    :param str_in: Incoming string to be referenced from.
    :type str_in: str
    :param key_in: Object to establish shuffled value patterns.
    :type key_in: object
    :param direction: Forwards is True, backwards is False.
    :type direction: bool
    :param byte_len: Number of bits per byte.
    :type byte_len: int
    :param sfunc: Function to create the shuffled indices.
    :type sfunc: function
    :returns: A scrambled string.
    :rtype: str
    """

    # get string binary string and shuffle it
    str_bin_shuffle = (
        shuffle(ct.str_bin_get(str_in, byte_len),
                key_in,
                direction,
                byte_len,
                sfunc))
    return ct.bin_str_get(str_bin_shuffle, byte_len)


def scramble_flip(str_in: str,
                  key_in: object,
                  direction: bool,
                  byte_len: int = 8,
                  ) -> str:
    """
    Apply a forward/backward scramble flip to str_in using key_in pattern.

    :param str_in: Incoming string to be referenced from.
    :type str_in: str
    :param key_in: Object to establish walk value patterns.
    :type key_in: object
    :param byte_len: Number of bits per byte.
    :type byte_len: int
    :param direction: Not used here, flip is reversed by second call.
    :type direction: bool
    :returns: A scrambled string.
    :rtype: str
    """

    # get binary int map
    str_bin = map(int, ''.join(
        map(
            lambda x: bin(ord(x))[2:].zfill(byte_len),
            str_in)))
    # get key ints map
    hashed_key = map(int,
                     ct.hhash(
                         key_in,
                         layers=-len(str_in)*byte_len,
                         mode='single_scramble_str'))
    # get flipped binary str
    str_bin_flip = ''.join(
        str(abs(next(str_bin) - (next(hashed_key) % 2)))
        for _ in '0' * (len(str_in)*byte_len))
    # return these as outgoing string
    return ct.bin_str_get(str_bin_flip, byte_len)

# eof
