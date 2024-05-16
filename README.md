# Airoha firmware parser & decryptor

An _010 Editor_ template for parsing the Airoha firmware format, and a Python script for decrypting the firmware's encrypted part.

Products using this firmware format include the AirReps (an AirPods clone) and numerous Sony headphones (notably WH-1000XM4 and WH-1000XM5, whose MediaTek chips are rebranded Airoha chips. Additional models may be found in [this](https://github.com/lzghzr/MDR_Proxy) repository).

The only plaintext strings present in the firmware are "verion_string" (Sony) and "version_string" (AirReps).

## Parser usage

Simply load the template in 010 Editor and run it on your firmware file.

![Screenshot](resources/010_editor_screenshot.png)

To produce the parser I've analyzed most firmware fields by hand, until I've found out that an Airoha evaluation kit is [publicly available](https://github.com/haltsai/Airoha_AB1565EVK) and used it to complete the analysis.

## Decryptor usage
### Notes
- The decryption, decompression algorithm has been tested with the firmware genertated by the offical FOTA Pacakge Tool from the said EVK
- A sample firmware file (generated with [this test payload](resources/fota_pacakge_filesystem.bin)) can be found [here](resources/fota_package_compressed_encrypted_default_key_iv.bin). The output should match the payload byte-to-byte (albeit with (potentially) extra padding).
- The offical tool used to generate the firmware can be found [here](https://github.com/npnet/Airoha_AB1585EVK/blob/main/mcu/tools/pc_tool/atk/AB158x_Airoha_Tool_Kit(ATK)_v3.1.6_20220525_144824.7z)
- The partition table that's required to genereate the firmware is procedurally generated by the EVK's build process. A sample (targeting AB155x SoCs) file is attached [here](resources/flash_download.cfg).

To decrypt, run:

```bash
pip install -Ur requirements.txt

# Decrypt and decompress the payload data
python airoha_decrypt.py --key=000102030405060708090a0b0c0d0e0f --iv=62633636633839306334636432383763 --offset=0x1000 fw.encrypted fw.decrypted

# Without decompression
python airoha_decrypt.py --key=000102030405060708090a0b0c0d0e0f --iv=62633636633839306334636432383763 --offset=0x1000 --no-decompress fw.encrypted fw.decrypted
```

