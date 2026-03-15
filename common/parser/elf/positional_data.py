"""
ELF位置数据基类
基于反编译分析实现
"""

from typing import Any, Optional, Union


class AbstractPositionalData:
    """抽象位置数据类"""
    
    def __init__(self, data=None, check_is_type=None, bypass_validation=False):
        """初始化位置数据
        
        Args:
            data: 原始数据
            check_is_type: 检查类型
            bypass_validation: 是否跳过验证
        """
        self._data = data
        self.ignore = False
        
    def offset(self) -> int:
        """获取偏移量"""
        raise NotImplementedError
        
    def size(self) -> int:
        """获取大小"""
        raise NotImplementedError
        
    def alignment(self) -> int:
        """获取对齐方式"""
        raise NotImplementedError
        
    def address(self) -> int:
        """获取地址"""
        raise NotImplementedError
        
    def mem_size(self) -> int:
        """获取内存大小"""
        raise NotImplementedError
        
    def is_loadable(self) -> bool:
        """是否可加载"""
        return False
        
    def is_uie_encryptable(self) -> bool:
        """是否可UIE加密"""
        return False
        
    def is_qbec_encryptable(self) -> bool:
        """是否可QBEC加密"""
        return False
        
    def is_encryptable(self) -> bool:
        """是否可加密"""
        return self.is_uie_encryptable() or self.is_qbec_encryptable()
        
    def data_name(self) -> str:
        """数据名称"""
        return ""
        
    def is_to_be_ignored(self) -> bool:
        """是否应忽略"""
        return False
        
    def validate_before_operation(self, **kwargs) -> None:
        """操作前验证"""
        pass


class PositionalData(AbstractPositionalData):
    """位置数据实现类"""
    
    def __init__(self, data=None, check_is_type=None, bypass_validation=False):
        """初始化位置数据
        
        Args:
            data: 原始数据
            check_is_type: 检查类型
            bypass_validation: 是否跳过验证
        """
        super().__init__(data, check_is_type, bypass_validation)
        self._offset = 0
        self._size = 0
        self._alignment = 0
        self._address = 0
        self._mem_size = 0
        
    def offset(self) -> int:
        """获取偏移量"""
        return self._offset
        
    def size(self) -> int:
        """获取大小"""
        return self._size
        
    def alignment(self) -> int:
        """获取对齐方式"""
        return self._alignment
        
    def address(self) -> int:
        """获取地址"""
        return self._address
        
    def mem_size(self) -> int:
        """获取内存大小"""
        return self._mem_size

    def end(self) -> int:
        """获取结束偏移"""
        return self.offset() + self.size()