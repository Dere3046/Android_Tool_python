# AndroidTOOL

[English](README.md) | [中文](README_CN.md)

## 什么是 AndroidTOOL？

AndroidTOOL 是基于反编译分析的 Qualcomm sectools.exe 功能的 Python 开源实现，用于解析、签名、加密和验证启动镜像（MBN/ELF），与原始工具完全兼容。目前支持 secure_image、mbn_tool 和 elf_tool 模块。

> **注意：** 此 Python 版本已停止更新，后续维护将集中在 Rust 版本，详见 [Android_Tool_RUST](https://github.com/Dere3046/Android_Tool_RUST)。

## 作用

- 解析和生成 Qualcomm 启动镜像（MBN、ELF）
- 检查、签名、加密和验证安全镜像
- 与 sectools.exe 输出兼容

## 项目结构

```
reconstructed/
├── common/          通用工具和解析器
│   ├── data/       数据工具
│   ├── logging/    日志模块
│   └── parser/     文件格式解析器
│       ├── elf/               ELF 解析器 (32/64 位)
│       ├── elf_with_hash_segment/  带哈希表的 ELF
│       └── mbn/               MBN 解析器 (v3-v8)
├── core/           核心工具实现
│   ├── elf_tool/   ELF 操作
│   ├── mbn_tool/   MBN 操作
│   └── secure_image/  安全镜像操作
└── profile/        安全配置
```

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。