import traceback
from dataclasses import dataclass

from sanic import Request, response

from msanic.libs.component import BaseDI
from msanic.libs.manager import HeaderSet


@dataclass
class ReqFinish(Exception):
    """完成请求状态异常"""
    code: int
    '''状态码'''
    data: (dict, list, object) = None
    '''响应数据'''
    total: int = 0
    '''针对于分页数据响应的总数量'''
    hint: str = ''
    '''响应消息提示'''
    headers: dict = None
    '''附加响应头'''


@dataclass
class RdsError(Exception):
    code: int
    '''状态码'''
    data: (dict, list, object) = None
    '''响应数据'''
    total: int = 0
    '''针对于分页数据响应的总数量'''
    hint: str = ''


@dataclass
class WsRpsMsg(Exception):
    """websocket消息响应"""
    code: int
    '''状态码'''
    data = None
    '''响应数据'''
    hint: str = ''
    '''响应消息提示'''


class CatchExpt(BaseDI):

    __code_map = {
        400: '请求结构错误,无法解析的结构',
        404: 'API接口不存在',
        500: '出错啦，请稍后再试或联系管理员检查',
        403: '请求结构不支持'
    }

    @classmethod
    def __log_err_info(cls, req: Request, err_info: str):
        cls.conf.log.error(
            f"请求异常信息:\n接口--{req.path}\n方法--{req.method}\n头部--{req.headers.items()}\nquery参数--{req.args}\n"
            f"body--{str(req.body, 'utf8')}\n错误信息--{err_info}")

    @classmethod
    def catch_req(cls, req: Request, expt):
        req_id = req.headers.get('req_id')
        req_id and cls.conf.rds and cls.conf.rds.drop_item(f"{cls.conf.PROCESSING_REQ}:{req_id}")
        headers = HeaderSet.out(cls.conf)
        hasattr(expt, 'headers') and expt.headers and headers.update(expt.headers)
        if isinstance(expt, ReqFinish):
            return response.json({'c': expt.code, 'd': expt.data, 'm': expt.hint}, headers=headers)
        body = {'c': 500, 'd': None, 'm': 'There are some error, please connect administrator to check.'}
        if hasattr(expt, 'status_code'):
            hint = cls.__code_map.get(expt.status_code)
            body = {'c': expt.status_code, 'd': None, 'm': hint}
            if expt.status_code == 500:
                cls.__log_err_info(req, traceback.format_exc())
            return response.json(body, headers=headers)
        cls.__log_err_info(req, traceback.format_exc())
        return response.json(body, status=500)
