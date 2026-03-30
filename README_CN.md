# AndroidTOOL - 高通安全工具 (Python)

[English](README.md) | [中文](README_CN.md)

> **注意：** 此 Python 版本已停止更新，后续维护将集中在 Rust 版本，详见 [Android_Tool_RUST](https://github.com/Dere3046/Android_Tool_RUST)。

~~基于反编译分析的 Qualcomm sectools.exe 功能的 Python 实现。~~

## ~~项目结构~~

~~```
common/
├── crypto/
│   └── openssl/       # OpenSSL 加密操作
├── data/              # 数据工具
├── logging/           # 日志模块
└── parser/            # 文件格式解析器
    ├── elf/           # ELF 解析器
    ├── mbn/           # MBN 解析器
    └── hash_segment/  # 哈希段定义

core/
├── elf_tool/          # ELF 操作
├── mbn_tool/          # MBN 操作
├── hash_sign_core.py  # 哈希和签名核心
└── secure_image/      # 安全镜像操作
    ├── signer/        # 签名器类
    └── encrypter/     # 加密器类

profile/               # 安全配置
```~~

## ~~功能特性~~

### ~~ELF 工具~~
- ~~解析和生成 ELF32/ELF64 镜像~~
- ~~插入段、合并文件、删除段~~
- ~~哈希表段支持~~

### ~~MBN 工具~~
- ~~解析 MBN 镜像 (v3-v8)~~
- ~~生成 MBN 镜像~~
- ~~启动镜像 ID 和目标指针支持~~

### ~~安全镜像~~
- ~~检查、验证、签名、哈希、加密、压缩~~
- ~~LOCAL/TEST/PLUGIN 签名模式~~
- ~~UIE/QBEC 加密模式~~
- ~~12 种 SHA 哈希变体~~
- ~~X.509 证书支持~~
- ~~Fuse blower 验证~~
- ~~Outfile 记录管理~~

### ~~支持的算法~~

**~~签名：~~** ~~ECDSA-P256, ECDSA-P384, RSA-2048/3072/4096~~

**~~哈希：~~** ~~SHA256/384/512, ONE-SHOT 变体，ZI 变体~~

**~~加密：~~** ~~AES-128-CBC, UIE, QBEC~~

## ~~依赖~~

~~- Python 3.9+~~
~~- cryptography 库~~

## ~~许可证~~

~~MIT License - 详见 [LICENSE](LICENSE) 文件。~~

## ~~免责声明~~

**~~仅供研究和教育目的使用~~**

~~本软件仅供安全研究、教育目的和逆向工程分析使用。用户有责任确保遵守所有适用的法律法规。作者不对本软件的任何滥用承担责任。~~

~~本工具不应用于：~~
- ~~任何非法活动~~

~~用户对本软件的使用承担所有责任和风险。~~

---

## ~~原始内容已移除~~

~~本文档的原始内容已不再适用。~~

**注意：** 我最初在 XDA 上发现了此工具。它仅以 EXE 二进制文件形式提供，我最初认为它不是开源的，因此对其进行了反编译。后来，我发现它实际上是开源的。

**源代码仓库：** https://github.com/basehub/sectools

**所以为了确保完整性，我将项目完整地克隆了过来。**
