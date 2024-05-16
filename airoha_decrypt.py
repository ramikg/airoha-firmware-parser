import argparse
import binascii
import lzma
import os
import struct

from Crypto.Cipher import AES


class AirohaDecryptInputAndOutputFilesMustBeDifferent(Exception):
    pass


def _parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('_from', type=argparse.FileType('rb'), help='Encrypted firmware file.')
    parser.add_argument('to', help='Decrypted (Decompressed too if applicable) file section.')
    
    parser.add_argument('--offset', type=lambda x: int(x, 0), default='0x1000',
                        help='Offset of the encrypted part in the input file.')
    parser.add_argument('--key', type=binascii.unhexlify, default='000102030405060708090a0b0c0d0e0f',
                        help='AES-128 key. Hex format.')
    parser.add_argument('--iv', type=binascii.unhexlify, default='62633636633839306334636432383763',
                        help='A 16-bytes IV for the AES-CBC. Hex format.')
    parser.add_argument('--no-decompress', action='store_true', help='Do not decompress the decrypted data.')
    return parser.parse_args()


def _decrypt(ciphertext, key, iv, offset=0):
    ciphertext = ciphertext[offset:]
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    decrypted = cipher.decrypt(ciphertext) # NOTE: Data may come with padding (with bytes 0xFF)    
    return decrypted


def _decompress(decrypted_data):
    # CPython can't handle an initialized size field in the LZMA header, so we set it to -1
    fixed_lzma = decrypted_data[:5] + struct.pack('<Q', 0xFFFFFFFFFFFFFFFF) + decrypted_data[5+8:]
    return lzma.decompress(fixed_lzma, format=lzma.FORMAT_ALONE)


if __name__ == '__main__':
    args = _parse_args()

    if os.path.exists(args.to) and os.path.samefile(args._from.name, args.to):
        raise AirohaDecryptInputAndOutputFilesMustBeDifferent()

    with args._from as encrypted_file:
        encrypted_data = encrypted_file.read()
    
    args.key = args.key[::-1]
    args.iv = args.iv[::-1]

    result = _decrypt(encrypted_data, args.key, args.iv, args.offset)

    if not args.no_decompress:
        try:
            decompressed_data = _decompress(result)
            result = decompressed_data
        except lzma.LZMAError as e:
            print(f'Failed to decompress: {e}. Writing decrypted data only.')

    with open(args.to, 'wb') as output:
        output.write(result)
