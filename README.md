# AndroidTOOL - Qualcomm Security Tool (Python)

[English](README.md) | [中文](README_CN.md)

> **Note:** This Python version has been discontinued. Future maintenance will focus on the Rust version. See [Android_Tool_RUST](https://github.com/Dere3046/Android_Tool_RUST).

~~Qualcomm sectools.exe functionality implementation based on decompilation analysis.~~

## ~~Project Structure~~

~~```
common/
├── crypto/
│   └── openssl/       # OpenSSL encryption operations
├── data/              # Data tools
├── logging/           # Logging module
└── parser/            # File format parser
    ├── elf/           # ELF parser
    ├── mbn/           # MBN parser
    └── hash_segment/  # Hash segment definitions

core/
├── elf_tool/          # ELF operations
├── mbn_tool/          # MBN operations
├── hash_sign_core.py  # Hash and signature core
└── secure_image/      # Secure image operations
    ├── signer/        # Signer class
    └── encrypter/     # Encrypter class

profile/               # Security profile
```~~

## ~~Features~~

### ~~ELF Tools~~
- ~~Parse and generate ELF32/ELF64 images~~
- ~~Insert segments, merge files, delete segments~~
- ~~Hash table segment support~~

### ~~MBN Tools~~
- ~~Parse MBN images (v3-v8)~~
- ~~Generate MBN images~~
- ~~Boot image ID and target pointer support~~

### ~~Secure Image~~
- ~~Check, verify, sign, hash, encrypt, compress~~
- ~~LOCAL/TEST/PLUGIN signature modes~~
- ~~UIE/QBEC encryption modes~~
- ~~12 SHA hash variants~~
- ~~X.509 certificate support~~
- ~~Fuse blower verification~~
- ~~Outfile record management~~

### ~~Supported Algorithms~~

**~~Signature:~~** ~~ECDSA-P256, ECDSA-P384, RSA-2048/3072/4096~~

**~~Hash:~~** ~~SHA256/384/512, ONE-SHOT variants, ZI variants~~

**~~Encryption:~~** ~~AES-128-CBC, UIE, QBEC~~

## ~~Dependencies~~

~~- Python 3.9+~~
~~- cryptography library~~

## ~~License~~

~~MIT License - See [LICENSE](LICENSE) file.~~

## ~~Disclaimer~~

**~~For research and educational purposes only~~**

~~This software is intended for security research, educational purposes, and reverse engineering analysis only. Users are responsible for ensuring compliance with all applicable laws and regulations. The authors assume no responsibility for any misuse of this software.~~

~~This tool should not be used for:~~
- ~~Any illegal activities~~

~~Users assume all responsibility and risk for the use of this software.~~

---

## ~~Original Content Removed~~

~~The original content of this document has been removed as it is no longer applicable.~~

**Note:** I initially discovered this tool on XDA. It was only available as an EXE binary, and I originally believed it was not open-source, so I decompiled it. Later, I discovered that it is actually open-source.

**Source Repository:** https://github.com/basehub/sectools

**Therefore, to ensure completeness, I have cloned the entire project.**
