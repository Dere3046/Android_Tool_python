# AndroidTOOL

[English](README.md) | [中文](README_CN.md)

## What is AndroidTOOL?

AndroidTOOL is a Python-based open-source reimplementation of Qualcomm's sectools.exe for parsing, signing, encrypting, and verifying boot images (MBN/ELF), fully compatible with the original tool. Currently supports secure_image, mbn_tool, and elf_tool modules.

> **Note:** This Python version is no longer actively maintained. Future development will focus on the Rust version, available at [Android_Tool_RUST](https://github.com/Dere3046/Android_Tool_RUST).

## Features

- Parse and generate Qualcomm boot images (MBN, ELF)
- Inspect, sign, encrypt, and verify secure images
- Compatible with sectools.exe output

## Project Structure

```
reconstructed/
├── common/          Common utilities and parsers
│   ├── data/        Data utilities
│   ├── logging/     Logging module
│   └── parser/      File format parsers
│       ├── elf/               ELF parser (32/64-bit)
│       ├── elf_with_hash_segment/  ELF with hash segment
│       └── mbn/               MBN parser (v3-v8)
├── core/            Core tool implementations
│   ├── elf_tool/    ELF operations
│   ├── mbn_tool/    MBN operations
│   └── secure_image/ Secure image operations
└── profile/         Security profiles
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.