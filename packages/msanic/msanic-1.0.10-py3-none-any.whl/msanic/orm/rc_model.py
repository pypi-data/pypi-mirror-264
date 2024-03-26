from abc import abstractmethod

from msanic.libs.component import LogsDI
from msanic.libs.rds_client import RdsClient
from msanic.orm.db_model import DbModel
from msanic.libs.tool import json_parse, json_encode


class RCModel(LogsDI):
    """数据缓存redis模型"""
    rds: RdsClient = None
    '''缓存redis客户端'''
    db_model: DbModel = None
    '''数据模型'''
    expired_mode = 0
    '''缓存过期模式 0--hash类的固定缓存(无过期) 1--key value类的时效型缓存 带过期时间 默认12小时'''
    expired_sec = 43200
    '''key value类的时效型缓存的过期时间'''

    @classmethod
    def set_rc(cls, rds, logs=None):
        cls.rds = rds
        # cls.db_model = db_model
        cls.logs = logs

    @classmethod
    @abstractmethod
    async def fun_set_cache(cls, info: dict) -> dict:
        """附加缓存设置"""
        pass

    @classmethod
    async def cache_by_pk(cls, pk_val: (int, str)):
        async def from_db():
            db_info = await cls.db_model.get_by_pk(pk_val)
            if db_info:
                if cls.expired_mode:
                    await cls.rds.set_item(key, json_encode(db_info), ex_time=cls.expired_sec)
                else:
                    await cls.rds.set_hash(cls.db_model.sheet_name(), pk_val, json_encode(db_info))
                pinfo = await cls.fun_set_cache(db_info)
                return pinfo
            return
        if not cls.db_model:
            return
        if cls.expired_mode:
            key = f"{cls.db_model.sheet_name()}:{pk_val}"
            info = await cls.rds.get_item(key)
        else:
            info = await cls.rds.get_hash(cls.db_model.sheet_name(), pk_val)
        if info:
            return json_parse(info, cls.logs.error if cls.logs else None)
        p_info = await cls.rds.locked(cls.db_model.sheet_name(), from_db)
        return p_info

    @classmethod
    async def cache_by_unique(cls, unique_map: dict, key_name: str):
        async def from_db():
            info = await cls.db_model.get_from_dict(unique_map, just_one=True)
            if info:
                pk_val = info.get(cls.db_model.pk_name())
                if cls.expired_mode:
                    await cls.rds.set_item(f'{key_name}:{unique_val}', pk_val, ex_time=cls.expired_sec)
                else:
                    await cls.rds.set_hash(key_name, unique_val, pk_val)
                await cls.fun_set_cache(info)
                return info
            return

        if not cls.db_model:
            return
        unique_val = '_'.join([str(unique_map.get(k)) for k in sorted(unique_map)])
        if cls.expired_mode:
            item_id = await cls.rds.get_item(f'{key_name}:{unique_val}')
        else:
            item_id = await cls.rds.get_hash(key_name, unique_val)
        if item_id:
            return await cls.cache_by_pk(item_id)
        return await cls.rds.locked(cls.db_model.sheet_name(), fun=from_db)

    @classmethod
    async def query_map(cls, is_super=False, field_name='name', groups: (list, tuple) = None, group_key='gid'):
        async def from_db():
            data_list = await cls.db_model.get_from_dict({})
            return [await cls.fun_set_cache(info) for n in data_list]

        if not groups:
            groups = []
        if not cls.db_model:
            return []
        pk_name = cls.db_model.pk_name()
        all_items = await cls.rds.get_hash_val(cls.db_model.sheet_name())
        if not all_items:
            all_items = await cls.rds.locked(cls.db_model.sheet_name(), fun=from_db, time_out=5)
        if (not is_super) and cls.db_model.check_field(group_key):
            new_list = []
            for item in all_items:
                info = json_parse(item, log_fun=cls.logs.error if cls.logs else None)
                g_id = info.get(group_key)
                (g_id in groups) and new_list.append({
                    'label': info.get(field_name), 'value': info.get(pk_name), group_key: g_id})
            return new_list
        return [{'label': info.get(field_name), 'value': info.get(pk_name), group_key: info.get(group_key)}
                for item in all_items if (info := json_parse(item, cls.logs.error if cls.logs else None))]

    @classmethod
    async def get_name(cls, pk_id: int or str, name_field='name'):
        if not pk_id:
            return '-'
        info = await cls.cache_by_pk(pk_id)
        return info.get(name_field) if info else '-'

    @classmethod
    async def get_map(cls, pk_id: int or str, name_list: list or tuple = None):
        if not pk_id:
            return {}
        info = await cls.cache_by_pk(pk_id)
        return {name: info.get(name) for name in name_list} if info else {}
