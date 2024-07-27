import argparse
import binascii
import lzma
import os
import struct

from Crypto.Cipher import AES


ENCRYPTED_PART_OFFSET_STRING = '0x1000'


class AirohaDecryptInputAndOutputFilesMustBeDifferent(Exception):
    pass


def _parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--from', dest='_from', metavar='FROM', type=argparse.FileType('rb'), required=True,
                        help='Encrypted firmware file.')
    parser.add_argument('--key', type=binascii.unhexlify,
                        help='AES-128 key. Hex format.')
    parser.add_argument('--iv', type=binascii.unhexlify,
                        help='A 16-bytes IV for the AES-CBC. Hex format.')
    parser.add_argument('--to', required=True,
                        help='Decrypted & decompressed firmware file.')
    parser.add_argument('--offset', type=lambda x: int(x, 0), default=ENCRYPTED_PART_OFFSET_STRING,
                        help=f'Offset of the encrypted part in the input file. Default is {ENCRYPTED_PART_OFFSET_STRING}.')
    parser.add_argument('--no-decompress', action='store_true',
                        help='Do not decompress the decrypted data.')
    parser.add_argument('--no-decrypt', action='store_true',
                        help='Do not decrypt (useful for compressed non-encrypted files).')
    parser.add_argument('--reverse-key-and-iv', action='store_false',
                        help='Reverse the bytes order in the input key and IV.')
    return parser.parse_args()


def _decrypt(ciphertext, key, iv, offset=0):
    ciphertext = ciphertext[offset:]
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    # Note that decrypted data may be padded with 0xFF bytes
    return cipher.decrypt(ciphertext)


def _decompress(decrypted_data):
    # CPython can't handle an initialized size field in the LZMA header, so we set it to -1
    fixed_lzma = decrypted_data[:5] + struct.pack('<Q', 0xFFFFFFFFFFFFFFFF) + decrypted_data[5+8:]
    return lzma.decompress(fixed_lzma, format=lzma.FORMAT_ALONE)


if __name__ == '__main__':
    args = _parse_args()

    if os.path.exists(args.to) and os.path.samefile(args._from.name, args.to):
        raise AirohaDecryptInputAndOutputFilesMustBeDifferent()

    with args._from as encrypted_file:
        output_data = encrypted_file.read()

    if not args.no_decrypt:
        if args.reverse_key_and_iv:
            args.key = args.key[::-1]
            args.iv = args.iv[::-1]

        output_data = _decrypt(output_data, args.key, args.iv, args.offset)
    if not args.no_decompress:
        output_data = _decompress(output_data)

    with open(args.to, 'wb') as output:
        output.write(output_data)
