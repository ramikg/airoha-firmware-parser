import subprocess

KEY = '000102030405060708090a0b0c0d0e0f'
IV = '62633636633839306334636432383763'
ENCRYPTED_FILE = 'resources/fota_package.bin'
DECRYPTED_TARGET_FILE = 'resources/unencrypted_blob.bin'
PADDING_BYTE = b'\xFF'


def _assert_file_contents_are_equal(file1, file2):
    with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
        return f1.read().rstrip(PADDING_BYTE) == f2.read().rstrip(PADDING_BYTE)


def test_sanity():
    output_path = '/tmp/decrypted.bin'

    command = [
        'python', '../airoha_decrypt.py',
        f'--key={KEY}',
        f'--iv={IV}',
        f'--from={ENCRYPTED_FILE}',
        f'--to={output_path}'
    ]
    run_result = subprocess.run(command)
    assert run_result.returncode == 0

    assert _assert_file_contents_are_equal(DECRYPTED_TARGET_FILE, output_path)
