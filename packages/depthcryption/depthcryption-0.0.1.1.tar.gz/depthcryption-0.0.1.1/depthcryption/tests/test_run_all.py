import os
import pathlib
import secrets
import unittest
from depthcryption import encrypt, decrypt, __Decrypt, __Encrypt

class Test_cryption_cycle(unittest.TestCase):

    def test_base(self):
        """ test most basic encryption decryption cycle"""
        tmp1 = 'some test string'
        tmp2 = 'another test string'
        tmp3 = ['some test structures',
                tuple([1, 1.1]),
                set([1, 1.1]),
                list([1, 1.1])]
        tmp4 = encrypt(tmp1, tmp2)
        tmp5 = encrypt(tmp3)
        tmp6 = decrypt(tmp4, tmp5)
        self.assertEqual([[tmp1, tmp2], tmp3], tmp6)

    def test_no_internet(self):
        """ test encryption decryption cycle with all offline parameters"""
        tmp1 = 'some test string'
        tmp2 = 'another test string'
        tmp3 = ['some test structures',
                tuple([1, 1.1]),
                set([1, 1.1]),
                list([1, 1.1])]
        tmp4 = encrypt(
            tmp1,
            tmp2,
            decryption_complexity='high',
            encryption_complexity='low',)
        tmp5 = encrypt(
            tmp3,
            compression=1,
            decryption_complexity='low',
            encryption_complexity='high',
            probability=1,
            key_os=True,
            key_py=True,
            key_time=[2265, 1],
            user_key=[f'a', r'test', {b'key'}],)
        tmp6 = decrypt(
            tmp4,
            tmp5,
            user_key=[f'a', r'test', {b'key'}])

        self.assertEqual([[tmp1, tmp2], tmp3], tmp6)

    def test_with_internet(self):
        """ test encryption decryption cycle with all online parameters"""
        tmp1 = 'some test string'
        tmp2 = 'another test string'
        tmp3 = ['some test structures',
                tuple([1, 1.1]),
                set([1, 1.1]),
                list([1, 1.1])]
        tmp4 = encrypt(
            tmp1,
            tmp2,
            key_ip=True,
            key_url="https://en.wikipedia.org/wiki/Boards_of_Canada")
        tmp5 = encrypt(
            tmp3,
            key_url="https://en.wikipedia.org/wiki/Boards_of_Canada",
            key_ip=True,)
        tmp6 = decrypt(tmp4, tmp5,)
        self.assertEqual([[tmp1, tmp2], tmp3], tmp6)


    def test_all_and_write(self):
        """ test encryption decryption cycle with all
        parameters while reading and writing files """
        tmp1 = 'some test string'
        tmp2 = 'another test string'
        tmp3 = ['some test structures',
                tuple([1, 1.1]),
                set([1, 1.1]),
                list([1, 1.1])]
        # depthcryption test directory path within tests dir _ddp
        _ddp = os.path.split(__file__)[0]
        _ddp += f'/DepthCryptionTest_{hash(str(secrets.randbelow(99999999)))}/'
        pathlib.Path(_ddp).mkdir(mode=0o777, parents=True, exist_ok=True)
        # write paths
        _wp1 = f'{_ddp}/{hash(str(secrets.randbelow(9999999999)))}.txt'
        _wp2 = f'{_ddp}/{hash(str(secrets.randbelow(9999999999)))}.txt'
        tmp4 = encrypt(
            tmp1,
            tmp2,
            decryption_complexity='low',
            encryption_complexity='low',
            key_url="https://en.wikipedia.org/wiki/Boards_of_Canada",
            key_ip=True,
            save_file=_wp1)
        tmp5 = encrypt(
            tmp3,
            save_file=_wp2,
            key_url="https://en.wikipedia.org/wiki/Boards_of_Canada",
            key_ip=True,
            compression=1,
            decryption_complexity='low',
            encryption_complexity='low',
            probability=1,
            key_os=True,
            key_py=True,
            key_time=[2265, 1],
            user_key=[f'a', r'test', {b'key'}], )
        tmp6 = decrypt(
            _wp1,
            _wp2,
            user_key=[f'a', r'test', {b'key'}],
            save_dir=_ddp)

        self.assertEqual([[tmp1, tmp2], tmp3], tmp6)

    def test_bad_nonkwarg(self):
        """test nonexistent kwarg call"""
        tmp1 = 'some test string'
        tmp2 = 'another test string'
        tmp3 = ['some test structures',
                tuple([1, 1.1]),
                set([1, 1.1]),
                list([1, 1.1])]
        with self.assertRaises(Exception):
            tmp4 = encrypt(
                tmp1,
                tmp2,
                nonexisting_kwarg=1)

    def test_bad_kwarg(self):
        """test kwarg call with wrong type"""
        tmp1 = 'some test string'
        tmp2 = 'another test string'
        tmp3 = ['some test structures',
                tuple([1, 1.1]),
                set([1, 1.1]),
                list([1, 1.1])]
        with self.assertRaises(Exception):
            tmp4 = encrypt(
                tmp1,
                tmp2,
                key_ip=1,
                probability='1')


if __name__ == '__main__':
    print('running tests in: ', __file__)
    unittest.main()

# eof
