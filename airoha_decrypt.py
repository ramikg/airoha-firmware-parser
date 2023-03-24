import argparse
import binascii
import lzma
import os
import struct

from Crypto.Cipher import AES


ENCRYPTED_BLOCK_SIZE = 256


class AirohaDecryptInputAndOutputFilesMustBeDifferent(Exception):
    pass


def _parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--key', type=binascii.unhexlify, required=True,
                        help='AES-128 key. Hex format.')
    parser.add_argument('--iv', type=binascii.unhexlify, required=True,
                        help='A 16-bytes IV for the AES-CBC. Hex format.')
    parser.add_argument('--from', dest='_from', type=argparse.FileType('rb'), required=True,
                        help='Encrypted firmware file.')
    parser.add_argument('--to', required=True,
                        help='Decrypted firmware file.')
    parser.add_argument('--offset', type=lambda x: int(x, 0), default=0,
                        help='Offset of the encrypted part in the input file.')
    parser.add_argument('--verify-lzma', action='store_true',
                        help='Verify that the result is a valid LZMA file.')

    return parser.parse_args()


def _decrypt(ciphertext, key, iv, offset=0):
    ciphertext = ciphertext[offset:]

    decrypted = b''
    for index in range(0, len(ciphertext), ENCRYPTED_BLOCK_SIZE):
        cipher = AES.new(key, AES.MODE_CBC, iv=iv)
        decrypted += cipher.decrypt(ciphertext[index: index+ENCRYPTED_BLOCK_SIZE])

    return decrypted


def _verify_lzma_file(decrypted_data):
    # CPython can't handle an initialized size field in the LZMA header, so we set it to -1
    fixed_lzma = decrypted_data[:5] + struct.pack('<Q', 0xFFFFFFFFFFFFFFFF) + decrypted_data[5+8:]
    lzma.decompress(fixed_lzma, format=lzma.FORMAT_ALONE)


if __name__ == '__main__':
    args = _parse_args()

    if os.path.exists(args.to) and os.path.samefile(args._from.name, args.to):
        raise AirohaDecryptInputAndOutputFilesMustBeDifferent()

    with args._from as encrypted_file:
        encrypted_data = encrypted_file.read()

    decrypted_data = _decrypt(encrypted_data, args.key, args.iv, args.offset)
    if args.verify_lzma:
        _verify_lzma_file(decrypted_data)

    with open(args.to, 'wb') as decrypted_file:
        decrypted_file.write(decrypted_data)
