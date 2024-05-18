# Sanity test

A sanity test for CI purposes.

## How to build a dummy FOTA package

Below are the instructions used for building the FOTA package used for testing.

1. Download the Airoha Tool Kit (ATK) from [here](https://github.com/npnet/Airoha_AB1585EVK/blob/main/mcu/tools/pc_tool/atk/AB158x_Airoha_Tool_Kit(ATK)_v3.1.6_20220525_144824.7z).
2. On a Windows PC, open the _FOTA Package Tool_.
3. Use the sample `flash_download.cfg` provided below. You can find more examples [here](https://github.com/npnet/Airoha_AB1565EVK/tree/main/mcu/tools/config).
4. Build the FOTA package using the default key & IV.

### Sample `flash_download.cfg`

```
general:
    config_version : v2.0
    platform: AB155x

main_region:
    address_type: physical
    rom_list:
        - rom:
            file: unencrypted_blob.bin
            name: ROFS
            begin_address: 0x08000000
```