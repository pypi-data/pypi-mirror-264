from msanic.libs.component import BaseEnum, CodeObj


G_TIME_ZONE = 'UTC'
'''全局时区设置'''


class StaCode:
    """请求的响应状态码"""
    PASS = CodeObj(0, 200, 'Finished.')
    TEND = CodeObj(10, 410, 'Under maintenance.')
    FAIL = CodeObj(11, 400, 'Failed.')
    '''公用请求失败，不确定响应状态请使用该项，并确保响应的文字描述'''
    ERR_ARG = CodeObj(12, 422, 'Invalid params.',)
    '''参数错误或无效'''
    ERR_AUTH = CodeObj(13, 401, 'Invalid authorization.')
    ERR_SIGN = CodeObj(14, 412, 'Invalid sign in.')
    FORBID = CodeObj(15, 403, 'Forbidden')
    NON_PMS = CodeObj(16, 406, 'Non enough permission.')
    EXPIRED = CodeObj(17, 409, 'Request was expired.')
    REAPED = CodeObj(18, 421, 'Request is repeated.')
    ERR_CONF = CodeObj(21, 501, 'Error by configuration.')


class AreaLevel(BaseEnum):
    """地域级别"""
    NATION = 1, '国家'
    PROVINCE = 2, '省/直辖市/地区'
    CITY = 3, '地级市/州/区/县级市'
    COUNTY = 4, '县/区域'
    TOWN = 5, '镇/城区/片区'
    STREET = 6, '街道/村/乡'


class FileSta(BaseEnum):
    NULL = -1, '未设置'
    UPING = 1, '上传中'
    CHECKING = 2, '校验中'
    ERR = 3, '上传错误'
    FINISHED = 4, '完成'
