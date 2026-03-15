# AndroidTOOL

[English](README.md) | [中文](README_CN.md)

## What is AndroidTOOL?

A Python implementation of Qualcomm sectools.exe functionality based on decompilation analysis.

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