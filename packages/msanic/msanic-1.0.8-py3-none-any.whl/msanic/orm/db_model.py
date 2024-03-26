from datetime import datetime

from tortoise import Model, fields, transactions
from tortoise.expressions import Q

from msanic.libs import tool_dt


class DbModel(Model):

    created = fields.BigIntField(null=True, index=True, default=0, description='创建时间')

    class Meta:
        abstract = True

    @classmethod
    def sheet_name(cls, set_time: datetime = None):
        """数据表名"""
        if hasattr(cls, 'split_type'):
            if not set_time:
                set_time = datetime.now()
            split_type = getattr(cls, 'split_type')
            if split_type == 1:
                cls._meta.db_table = f"{cls._meta.db_table}_{set_time.strftime('%Y')}"
            elif split_type == 2:
                cls._meta.db_table = f"{cls._meta.db_table}_{set_time.strftime('%Y_%m')}"
            elif split_type == 3:
                cls._meta.db_table = f"{cls._meta.db_table}_{set_time.strftime('%Y_%m_%d')}"
            else:
                cls._meta.db_table = f"{cls._meta.db_table}_{set_time.strftime('%Y-%W')}"
        return cls._meta.db_table

    @classmethod
    def pk_name(cls):
        return cls._meta.db_pk_column

    @classmethod
    def check_field(cls, field: str):
        return field in cls._meta.db_fields

    @classmethod
    def out_fields(cls, forbids: (list, tuple, set) = None):
        """禁止部分字段输出"""
        return [name for name in cls._meta.db_fields if name not in forbids] if forbids else cls._meta.db_fields

    @classmethod
    def query_set(cls, q_set: Q = None, outs: (tuple, list) = None, forbids: (tuple, list) = None, force_all=False):
        """
        获取查询模型和输出字段
        :param q_set: Q查询表达式
        :param outs: 指定输出字段(优先) 若指定的字段全部不在当前表字段集合里，将全部字段输出
        :param forbids: 指定不输出的字段(已指定out后将不生效)
        :param force_all: 强制所有
        """
        query_model = cls.filter(sta_del=False) if (hasattr(cls, 'sta_del')) and (not force_all) else cls.all()
        if q_set:
            query_model = query_model.filter(q_set)
        f_list = [f for f in outs if f in cls._meta.db_fields] if outs else (
            [v for v in cls._meta.db_fields if v not in forbids] if forbids else [])
        return query_model, f_list

    @classmethod
    async def get_on_page(cls, q_set: Q, page=1, page_size=20, order_key='-created', fmt_fun=None,
                          outs: (tuple, list) = None, forbids: (tuple, list) = None):
        query_model, field_list = cls.query_set(q_set, outs=outs, forbids=forbids)
        total = await query_model.count()
        if order_key != '-created':
            key = order_key[1:] if order_key[0] in ('-', '+') else order_key
            if key not in cls._meta.db_fields:
                order_key = '-created'
        if page < 1:
            page = 1
        offset = (page - 1) * page_size
        data_list = await query_model.order_by(order_key).limit(page_size).offset(offset).values(*field_list)
        if callable(fmt_fun):
            await fmt_fun(data_list)
        return data_list, total

    @classmethod
    async def get_by_pk(cls, val: (int, str), outs: (tuple, list) = None, forbids: (tuple, list) = None):
        if not cls._meta.db_pk_column:
            raise Exception(f'Current sheet {cls.sheet_name()} has no set primary key')
        query_model, f_list = cls.query_set(Q(**{cls._meta.db_pk_column: val}), outs=outs, forbids=forbids)
        return await query_model.limit(1).values(*f_list)

    @classmethod
    async def __query_order_out(cls, query_model, field_list, order_key: str = None, just_one: bool = True):
        if not order_key:
            return await query_model.limit(1).values(*field_list) if just_one else await query_model.values(*field_list)
        key = order_key[1:] if order_key[0] in ('-', '+') else order_key
        if key not in cls._meta.db_fields:
            order_key = '-created'
        return await query_model.order_by(order_key).limit(1).values(*field_list) if just_one else \
            await query_model.order_by(order_key).values(*field_list)

    @classmethod
    async def get_from_dict(
            cls,
            query_map: dict,
            outs: (tuple, list) = None,
            forbids: (tuple, list) = None,
            order_key: str = None,
            just_one: bool = True):
        query_model, f_list = cls.query_set(Q(**query_map), outs=outs, forbids=forbids)
        return await cls.__query_order_out(query_model, f_list, order_key=order_key, just_one=just_one)

    @classmethod
    async def get_form_qset(
            cls,
            q_set: Q,
            outs: (tuple, list) = None,
            forbids: (tuple, list) = None,
            order_key: str = None,
            just_one: bool = True,):
        query_model, f_list = cls.query_set(q_set, outs=outs, forbids=forbids)
        return await cls.__query_order_out(query_model, f_list, order_key=order_key, just_one=just_one)

    @classmethod
    async def get_count(cls, q_set: Q, farce_all=False):
        query_set, _ = cls.query_set(q_set, force_all=farce_all)
        return await query_set.count()

    @classmethod
    async def add_from_dict(cls, param: dict, fun_success=None):
        """
        自动分表模式创建
        公共 新增或更新 值为None采用默认值

        :param param: 字典数据模型
        :param fun_success: 执行成功后的补充处理函数 协程函数 参数为生成的Model模型
        """
        param['created'] = tool_dt.cur_time()
        new_dict = {field: val for field, val in param.items() if (field in cls._meta.db_fields) and (val is not None)}
        if not new_dict:
            return None
        row = await cls.create(**new_dict)
        if row:
            callable(fun_success) and await fun_success(row)
            return row
        return None

    @classmethod
    async def upgrade_by_pk(cls, pk_val: (int, str), param: dict, current: dict = None, fun_success=None):
        if not cls._meta.db_pk_column:
            raise Exception(f'Current sheet {cls.sheet_name()} has no set primary key')
        if not current:
            new_dict = {
                k: v for k, v in param.items() if (k in cls._meta.db_fields) and (k != 'created') and (v is not None)}
        else:
            new_dict = {k: v for k, v in param.items() if (k in cls._meta.db_fields) and (
                    k != 'created') and (v is not None) and (current.get(k) != v)}
        if new_dict:
            ('updated' in cls._meta.db_fields) and new_dict.update({'updated': tool_dt.cur_time()})
            async with transactions.atomic():
                sta = await cls.filter(**{cls._meta.db_pk_column: pk_val}).limit(1).update(**new_dict)
                if sta:
                    callable(fun_success) and await fun_success(new_dict)
                    return new_dict
            return False
        return None

    @classmethod
    async def upgrade_by_qset(cls, q_set: Q, param: dict, just_one=True, fun_success=None):
        new_dict = {k: v for k, v in param.items() if
                    (k in cls._meta.db_fields) and (k != 'created') and (v is not None)}
        if new_dict:
            ('updated' in cls._meta.db_fields) and new_dict.update({'updated': tool_dt.cur_time()})
            query_set = cls.filter(q_set)
            if just_one:
                query_set = query_set.limit(1)
            async with transactions.atomic():
                sta = await query_set.update(**new_dict)
                if sta:
                    callable(fun_success) and await fun_success(new_dict)
                    return new_dict
        return None

    @classmethod
    async def del_by_pk(cls, pk_val: (int, str), fun_success=None, fun_ags: (list, tuple) = None, force_del=False):
        if not cls._meta.db_pk_column:
            raise Exception(f'Current sheet {cls.sheet_name()} has no set primary key')
        if fun_ags is None:
            fun_ags = ()
        if (not hasattr(cls, 'sta_del')) or force_del:
            async with transactions.atomic():
                sta = await cls.filter(**{cls._meta.db_pk_column: pk_val}).limit(1).delete()
                if sta:
                    callable(fun_success) and await fun_success(*fun_ags)
                    return True
            return False
        async with transactions.atomic():
            sta = await cls.filter(**{cls._meta.db_pk_column: pk_val}).limit(1).update(sta_del=True)
            if sta:
                callable(fun_success) and await fun_success(*fun_ags)
                return True
        return False

    @classmethod
    async def del_fun(cls, q_set: Q, just_one=True, fun_success=None, fun_ags: (list, tuple) = None, force_del=False):
        if fun_ags is None:
            fun_ags = ()
        query_set = cls.filter(q_set)
        if just_one:
            query_set = query_set.limit(1)
        if (not hasattr(cls, 'sta_del')) or force_del:
            async with transactions.atomic():
                sta = await query_set.delete()
                if sta:
                    callable(fun_success) and await fun_success(*fun_ags)
                    return True
            return False
        async with transactions.atomic():
            sta = await query_set.update(sta_del=True)
            if sta:
                callable(fun_success) and await fun_success(*fun_ags)
                return True
        return False
