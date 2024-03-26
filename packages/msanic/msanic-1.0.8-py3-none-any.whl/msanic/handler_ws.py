from msanic.exception import WsRpsMsg
from msanic.base_conf import BaseConf
from msanic.libs.component import CodeObj, BaseDI
from msanic import verify


class WsHandler(BaseDI):
    CMD_FUN_MAP = {}

    def __init__(self, conf: BaseConf, cmd_type: int):
        self.__conf = conf
        self.__cmd_type = cmd_type

    @property
    def cmd_type(self):
        return self.__cmd_type

    async def funapi(self, cmd, uinfo, data):
        fun = self.CMD_FUN_MAP.get(cmd)
        if fun:
            try:
                data = await fun(uinfo, data)
            except WsRpsMsg as msg:
                return cmd, msg.data, msg.code, msg.hint
            return cmd, data, self.__conf.STA_CODE.PASS.val, ''
        return cmd, None, self.conf.STA_CODE.FAIL.val, 'unspecified message.'

    def sendmsg(self, code: CodeObj = None, data: dict or list = None, hint='success'):
        code, hint = (self.conf.STA_CODE.PASS.val, self.conf.STA_CODE.PASS.msg) if code is None else (
            code.val, hint or code.msg)
        raise WsRpsMsg(code, data, hint)

    def verify_str(self, val, require=False, default='', turn=0, minlen: int = None, maxlen: int = None, p_name=''):
        sta, val_info = verify.vstr(
            val, require=require, default=default, turn=turn, minlen=minlen, maxlen=maxlen, p_name=p_name)
        return val_info if sta else self.sendmsg(code=self.conf.STA_CODE.ERR_ARG.val, hint=val_info)

    def verify_int(self, v, require=False, default=0, minval: int = None, maxval: int = None, inner=True, p_name=''):
        sta, val_info = verify.vint(
            v, require=require, default=default, minval=minval, maxval=maxval, inner=inner, p_name=p_name)
        return val_info if sta else self.sendmsg(code=self.conf.STA_CODE.ERR_ARG.val, hint=val_info)

    def verify_float(self, val, require=False, default=None, keep_val=3, minval: float or int = None,
                     maxval: float or int = None, inner=True, p_name=''):
        sta, val_info = verify.vfloat(
            val, require=require, default=default, keep_val=keep_val, minval=minval, maxval=maxval,
            inner=inner, p_name=p_name)
        return val_info if sta else self.sendmsg(code=self.conf.STA_CODE.ERR_ARG.val, hint=val_info)

    def verify_type(self, val, type_fun, require=False, default=None, is_int=True, p_name=''):
        val = self.verify_int(val, require=require, default=default, p_name=p_name) if is_int else \
            self.verify_str(val, require=require, default=default, p_name=p_name)
        if val is None:
            return default
        if type_fun(val):
            return val
        return self.sendmsg(code=self.conf.STA_CODE.ERR_ARG.val, hint=f'{p_name}参数不在限定范围')

    def verify_time(self, val, require=False, default=None, time_min=None, time_max=None, inner=True, p_name=''):
        sta, val_info = verify.vdatetime(
            val, require=require, default=default, time_min=time_min, time_max=time_max, inner=inner, p_name=p_name)
        return val_info if sta else self.sendmsg(code=self.conf.STA_CODE.ERR_ARG.val, hint=val_info)
