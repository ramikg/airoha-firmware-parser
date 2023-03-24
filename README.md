# Airoha firmware parser & decryptor

An _010 Editor_ template for parsing the Airoha firmware format, and a Python script for decrypting the firmware's encrypted part.

Products using this firmware format include the AirReps (an AirPods clone) and numerous Sony headphones (notably WH-1000XM4 and WH-1000XM5, whose MediaTek chips are rebranded Airoha chips. Additional models may be found in [this](https://github.com/lzghzr/MDR_Proxy) repository).

The only plaintext strings present in the firmware are "verion string" (Sony) and "version string" (AirReps).

## Parser usage

Simply load the template in 010 Editor and run it on your firmware file.

![Screenshot](resources/010_editor_screenshot.png)

To produce the parser I've analyzed most firmware fields by hand, until I've found out that an Airoha evaluation kit is [publicly available](https://github.com/haltsai/Airoha_AB1565EVK) and used it to complete the analysis.

## Decryptor usage

**Note – The decryption algorithm hasn't been tested, and is simply based on the mentioned evaluation kit.**  
An example of encrypted firmware with a known key and IV would be most helpful.

To decrypt, run:

```bash
pip install -Ur requirements.txt

python airoha_decrypt.py --key=0F0E0D0C0B0A09080706050403020100 --iv=63373832646334633039386336366362 --from=fw.encrypted --offset=0x1000 --to=fw.decrypted --verify-lzma
```

Explanation:

- `--offset` specifies the offset in the input file where the encrypted part starts. (Optional)
- `--verify-lzma` verifies that the decrypted file is a valid LZMA file. This is effectively equivalent to checking that the key and IV were correct. (Optional)
