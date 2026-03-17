# AndroidTOOL - Qualcomm Security Tool (Python)

[English](README.md) | [中文](README_CN.md)

> **Note:** This Python version is no longer actively maintained. Future development will focus on the Rust version, available at [Android_Tool_RUST](https://github.com/Dere3046/Android_Tool_RUST).

Python implementation of Qualcomm sectools.exe functionality based on decompiled analysis.

## Project Structure

```
common/
├── crypto/
│   └── openssl/       # OpenSSL crypto operations
├── data/              # Data utilities
├── logging/           # Logging module
└── parser/            # File format parsers
    ├── elf/           # ELF parser
    ├── mbn/           # MBN parser
    └── hash_segment/  # Hash segment defines

core/
├── elf_tool/          # ELF operations
├── mbn_tool/          # MBN operations
├── hash_sign_core.py  # Hash and sign core
└── secure_image/      # Secure image operations
    ├── signer/        # Signer classes
    └── encrypter/     # Encrypter classes

profile/               # Security profiles
```

## Features

### ELF Tool
- Parse and generate ELF32/ELF64 images
- Insert segments, combine files, remove sections
- Hash table segment support

### MBN Tool
- Parse and generate MBN images (v3-v8)
- Boot image ID and destination pointer support

### Secure Image
- Inspect, validate, sign, hash, encrypt, compress
- LOCAL/TEST/PLUGIN signing modes
- UIE/QBEC encryption modes
- 12 SHA hash variants
- X.509 certificate support
- Fuse blower validation
- Outfile record management

### Supported Algorithms

**Signature:** ECDSA-P256, ECDSA-P384, RSA-2048/3072/4096

**Hash:** SHA256/384/512, ONE-SHOT variants, ZI variants

**Encryption:** AES-128-CBC, UIE, QBEC

## Requirements

- Python 3.9+
- cryptography library

## License

MIT License - See [LICENSE](LICENSE) file for details.

## Disclaimer

**FOR RESEARCH AND EDUCATIONAL PURPOSES ONLY**

This software is provided for security research, educational purposes, and reverse engineering analysis only. Users are responsible for ensuring compliance with all applicable laws and regulations. The authors disclaim all liability for any misuse of this software.

This tool should NOT be used for:
- Any illegal activities

Users assume all responsibility and risk for their use of this tool.