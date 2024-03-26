from enum import Enum
from types import DynamicClassAttribute

from dataclasses import dataclass

from msanic.libs.mult_log import MultLogger


class BaseEnum(Enum):
    """
    继承自该类的枚举设置的模型必须为： name = (value/值, desc/描述或说明) 否则报错

    该类不允许被二次继承
    """

    @DynamicClassAttribute
    def val(self):
        """值"""
        return self.value[0]

    @DynamicClassAttribute
    def label(self):
        """描述"""
        return self.value[1]

    @DynamicClassAttribute
    def data(self):
        """数据(第三项 可选)"""
        if len(self.value) > 2:
            return self.value[2]
        return None

    @classmethod
    def fetch_name(cls, name) -> bool:
        """是否包含命名"""
        return name in cls._member_names_

    @classmethod
    def fetch_val(cls, value):
        """是否包含指定值"""
        v: BaseEnum
        for v in cls._value2member_map_.values():
            if v.val == value:
                return v
        return None

    @classmethod
    def get_name(cls, value):
        """获取指定值的描述"""
        v: BaseEnum
        for v in cls._value2member_map_.values():
            if v.val == value:
                return v.label
        return ""

    @classmethod
    def map_list(cls, outs: list = None):
        """
        以value -- label map的方式返回类型映射

        :param outs: 不输出的值集合, 该参数内的值不做输出
        """
        v: BaseEnum
        if not outs:
            return {v.val: v.label for v in cls._value2member_map_.values()}
        return {v.val: v.label for v in cls._value2member_map_.values() if v.val not in outs}


class LogsMeta:
    """日志输出模型"""

    def __init__(self, logs: MultLogger = None):
        self.__logs = logs

    def log_err(self, err: str):
        self.__logs.error(err) if self.__logs else print(err)

    def log_info(self, info: str):
        self.__logs.info(info) if self.__logs else print(info)


class LogsDI:

    logs: MultLogger = None

    def log_err(self, err: str):
        self.logs.error(err) if self.logs else print(err)

    def log_info(self, info: str):
        self.logs.info(info) if self.logs else print(info)


class BaseDI:
    """基础配置依赖模型"""

    conf = None

    @property
    def rds(self):
        """缓存连接池"""
        return self.conf.rds

    @property
    def log(self):
        """文件日志"""
        return self.conf.log

    @property
    def rng(self):
        """随机值相关工具"""
        return self.conf.rng

    @classmethod
    def set_conf(cls, conf):
        cls.conf = conf


@dataclass
class CodeObj:
    """状态码对象"""
    val: int
    '''指定响应码'''
    http: int = 200
    '''映射的状态码'''
    msg: str = ''
    '''附加的消息'''
