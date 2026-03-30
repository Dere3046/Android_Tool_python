# Sectools 反编译报告

## 执行摘要

成功从 `sectools.exe` (PyInstaller 打包) 提取并反编译了 Python 源代码和资源文件。

## 提取统计

| 项目 | 数量 |
|------|------|
| CArchive 文件 | 1,915 |
| PYZ 文件 | 1,132 |
| 反编译 Python 文件 | 1,105 |
| DLL/PYD 库文件 | 17 |
| 其他资源文件 | 71 |
| **总文件数** | **1,193** |
| **总大小** | 45.90 MB |

## 目录结构

```
sectools/
├── sectools.py              # 主程序入口
├── cmd_line_interface/      # 命令行界面
├── common/                  # 通用工具
├── core/                    # 核心功能模块
├── bin/                     # 二进制资源
├── open_source_licenses/    # 开源许可证
└── ... (标准库和第三方库)
```

## 主要功能模块

| 模块 | 功能 |
|------|------|
| secure_image | 安全镜像生成（签名、加密） |
| secure_debug | 安全调试配置 |
| fuseblower | 熔丝烧录工具 |
| fuse_validator | 熔丝验证器 |
| elf_tool | ELF 文件处理 |
| mbn_tool | MBN 文件生成 |
| tme_command | TME 命令 |

## 反编译问题

### 1. PyInstaller 5.3+ 格式问题
- PYZ 档案中的 pyc 文件不存储完整头部
- 只存储原始字节码（16 字节伪头部 + 字节码）
- **解决方案**: 使用 pydumpck 生成的 *.structed.pyc 文件

### 2. 反编译代码损坏
由于反编译工具的限制，部分代码损坏：
- `None` 占位符替代了原始函数调用
- 语法错误（如 `=` 代替 `==`）
- 控制流语句不完整

### 3. 标准库模块损坏
反编译的标准库模块有语法错误
- **解决方案**: 用 Python 3.10 标准库替换

## 运行状态

❌ **无法直接运行**

原因：
1. 项目特定模块（common, core, cmd_line_interface）有大量反编译损坏
2. 需要手动修复数百个语法错误
3. 部分逻辑无法从字节码恢复

## 建议

### 选项 1: 手动修复（推荐用于学习）
1. 替换所有标准库模块为原始 Python 3.10 版本
2. 手动修复关键业务逻辑文件
3. 使用 uncompyle6 或 pycdc 重新反编译特定文件

### 选项 2: 使用原始 EXE
如果需要使用工具功能，建议直接使用原始 `sectools.exe`

### 选项 3: 静态分析
使用反编译的代码进行静态分析，理解程序逻辑

## 工具和技术

- **提取**: pyinstxtractor.py
- **反编译**: pydumpck (pycdc + uncompyle6)
- **Python 版本**: 3.10
- **PyInstaller 版本**: 5.3+

## 输出位置

```
D:\AAwork\Android_Tool_python\sectools\
```

## 生成日期

2026-03-30
