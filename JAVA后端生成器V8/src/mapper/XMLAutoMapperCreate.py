from src.util import stringUtil
import re


def create_xml_mapper(config: dict):
    data = __create_xml_head(config) + '\n'
    data += __check_res_filed_repeat(config) + '\n'
    data += __create_result_map(config, False, False, False) + '\n'
    # 插入或更新
    data += _create_xml_insert_block(config) + '\n'
    data += _create_insert_list(config) + '\n'
    data += _create_insert_save_or_update_by_unique(config) + '\n'
    data += _create_insert_saver_or_update_by_where(config) + '\n'
    data += _create_insert_by_where_insert(config) + '\n'
    # 删
    data += _create_xml_delete_block(config) + '\n'
    data += _create_xml_delete_where_block(config) + '\n'
    if "falseDelete" in config:
        data += _create_xml_false_delete_block(config) + '\n'
    # 改
    data += _create_xml_update_by_key_block(config) + '\n'
    data += _create_xml_update_by_not_repeat_where_block(config) + '\n'
    data += _create_xml_update(config) + '\n'
    data += _create_xml_update_set_null_by_key(config) + '\n'
    # 单表查
    data += _create_xml_select_by_key(config) + '\n'
    data += _create_xml_select_one(config) + '\n'
    data += _create_xml_select(config) + '\n'
    # 计数
    data += _create_xml_count(config) + '\n'
    # 多表查
    data += _create_xml_x_to_x_block(config) + '\n'

    data += __create_xml_tail() + '\n'
    return data


def __create_xml_head(config: dict):
    data = '<?xml version="1.0" encoding="UTF-8"?>\n'
    data += '<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "http://mybatis.org/dtd/mybatis-3-mapper.dtd">\n'
    data += f'<mapper namespace="{config["path_xml_mapper"]}.{config["XMLAutoMapperName"]}">\n'
    return data


def __create_xml_tail():
    return "</mapper>\n"


def __table_filed_list(obj: dict) -> list:
    lists = [obj["key"].copy()]
    for i in obj["attr"]:
        lists.append(i.copy())
    return lists


def __check_res_filed_repeat(config: dict):
    tag = "\t"
    # 封装临时数据，将所有属性变成列表形式
    tables = {
        config["tableName"]: {
            "attr": __table_filed_list(config),
            "className": config["className"],
            "path_pojo": config["path_pojo"]
        }
    }
    one_to_one_list = []
    one_to_many_list = []
    many_to_many_list = []
    if config.get("oneToOne"):
        for obj in config.get("oneToOne"):
            tables[obj["tableName"]] = {
                "attr": __table_filed_list(obj),
                "className": obj["className"],
                "path_pojo": obj["path_pojo"],
                "foreign_key": obj["foreign_key"]
            }
            one_to_one_list.append(obj["tableName"])
    if config.get("oneToMany"):
        for obj in config.get("oneToMany"):
            tables[obj["tableName"]] = {
                "attr": __table_filed_list(obj),
                "className": obj["className"],
                "path_pojo": obj["path_pojo"],
                "foreign_key": obj["foreign_key"]
            }
            one_to_many_list.append(obj["tableName"])
    if config.get("manyToMany"):
        for obj in config.get("manyToMany"):
            if obj["many"]["tableName"] not in tables:
                tables[obj["many"]["tableName"]] = {
                    "attr": __table_filed_list(obj["many"]),
                    "className": obj["many"]["className"],
                    "path_pojo": obj["many"]["path_pojo"],
                    # 此处外键作用未知
                    "foreign_key": obj["many"]["foreign_key"]
                }
                many_to_many_list.append(obj["many"]["tableName"])
    # 替换
    # 重复判断，如果没有重复则直接返回空，没必要生成
    return_flag = True
    for table1 in tables:
        for attr1 in tables[table1]["attr"]:
            flag = False
            for table2 in tables:
                for attr2 in tables[table2]["attr"]:
                    if table1 != table2 and attr1["filed"] == attr2["filed"] and "filed_new" not in attr2:
                        flag = True
                        return_flag = False
                        # 是否在多表查询中用sql标签替换
                        config["replacementMapping"] = True
                        if "multiName" in config:
                            attr2["filed_new"] = f'{table2}_temp_{attr2["filed"]}'
                        else:
                            attr2["filed_new"] = f'{table2}_{attr2["filed"]}'
            if flag:
                if "multiName" in config:
                    attr1["filed_new"] = f'{table1}_temp_{attr1["filed"]}'
                else:
                    attr1["filed_new"] = f'{table1}_{attr1["filed"]}'
    if return_flag:
        # 是否在多表查询中用sql标签替换
        config["replacementMapping"] = False
    string_block = ""
    for table in tables:
        data = ""
        for attr in tables[table]["attr"]:
            if "filed_new" in attr:
                data += f'{table}.{attr["filed"]} AS {attr["filed_new"]},'
                if tables[table].get("foreign_key") == attr["filed"]:
                    tables[table]["foreign_key_new"] = attr["filed_new"]
            else:
                data += f'{table}.{attr["filed"]},'
        data = data.strip(",")
        data = f'<sql id="sql_filed_{table}">{data}</sql>'
        string_block += f'{tag}{data}\n'
    string_block += "\n"
    # 将替换后的数据存入次，方便查找替换的字段
    config["rep_obj"] = tables
    bean_info = {
        "resultMapName": f'res{config["className"]}MultiTable',
        "oneToMany": [],
        "oneToOne": [],
        "manyToMany": []
    }
    for table in tables:
        if "filed_new" in tables[table]["attr"][0]:
            tables[table]["attr"][0]["filed"] = tables[table]["attr"][0]["filed_new"]
        obj = {"key": tables[table]["attr"][0]}
        del tables[table]["attr"][0]
        obj["attr"] = tables[table]["attr"]
        obj["className"] = tables[table]["className"]
        obj["path_pojo"] = tables[table]["path_pojo"]
        if "foreign_key" in tables[table]:
            obj["foreign_key"] = tables[table]["foreign_key"]
        obj["tableName"] = table
        bean_info["replacementMapping"] = config["replacementMapping"]
        if table in one_to_one_list:
            bean_info["oneToOne"].append(obj)
        elif table in one_to_many_list:
            bean_info["oneToMany"].append(obj)
        elif table in many_to_many_list:
            bean_info["manyToMany"].append({"many": obj})
        else:
            bean_info.update(obj)
    # 此处加入config中主要针对子查询中，字段名被替换无法找到原本字段名问题
    config["bean_info"] = bean_info
    data = __create_result_map(bean_info)
    # 只有生成result_map才需，不然都是手动拼接
    bean_info["resultMapName"] = config["resultMapName"]
    # 封装模糊搜索需要的列表
    if "keyWordList" in config:
        bean_info["keyWordList"] = config["keyWordList"]
    # 封装是否采用模糊搜索
    if "fuzzySearch" in config:
        bean_info["fuzzySearch"] = config["fuzzySearch"]
    if "keyWord" in config:
        bean_info["keyWord"] = config["keyWord"]
    if return_flag:
        return data
    string_block += data
    return string_block


# 创建单表resMap块
def __create_result_map(config: dict, one_to_one=True, one_to_many=True, many_to_many=True) -> str:
    tag = "\t"
    data = ""
    # if config.get("replacementMapping"):
    #     data += f'{tag}<resultMap type="{config["path_pojo"]}.{config["className"]}" id="resOne{config["className"]}">\n'
    #     data += __create_method_result_map_key_value(config, 2)
    #     data += f'{tag}</resultMap>\n\n'
    data += f'{tag}<resultMap type="{config["path_pojo"]}.{config["className"]}" id="{config["resultMapName"]}">\n'
    data += __create_method_result_map_key_value(config, 2)
    if one_to_one and config.get("oneToOne"):
        for obj in config.get("oneToOne"):
            data += __create_result_map_one_to_one(obj, 2)
    table_set = set()
    if one_to_many and config.get("oneToMany"):
        for obj in config.get("oneToMany"):
            if obj["className"] in table_set:
                continue
            table_set.add(obj["className"])
            data += __create_result_map_one_to_many(obj, 2)
    if many_to_many and config.get("manyToMany"):
        for obj in config.get("manyToMany"):
            if obj["many"]["className"] in table_set:
                continue
            table_set.add(obj["many"]["className"])
            data += __create_result_map_one_to_many(obj["many"], 2)
    data += f'{tag}</resultMap>\n'
    return data


def __create_result_map_one_to_one(obj: dict, indent: int) -> str:
    tag = '\t' * indent
    data = f'{tag}<association property="{stringUtil.low_str_first(obj["className"])}" javaType="{obj["path_pojo"]}.{obj["className"]}">\n'
    data += __create_method_result_map_key_value(obj, indent + 1)
    data += f'{tag}</association>\n'
    return data


def __create_result_map_one_to_many(obj: dict, indent: int) -> str:
    tag = '\t' * indent
    data = f'{tag}<collection property="list{obj["className"]}" ofType="{obj["path_pojo"]}.{obj["className"]}">\n'
    data += __create_method_result_map_key_value(obj, indent + 1)
    data += f'{tag}</collection>\n'
    return data


# 根据对象生成res块
def __create_method_result_map_key_value(obj_info: dict, indent: int) -> str:
    tag = "\t" * indent
    data = f'{tag}<id column="{obj_info["key"]["filed"]}" property="{obj_info["key"]["attr"]}"/>\n'
    data += __create_method_result_map_attr_key_value(obj_info["attr"], indent)
    return data


# 根据对象生成res块
def __create_method_result_map_attr_key_value(obj: list, indent: int) -> str:
    tag = "\t" * indent
    data = ""
    for attr in obj:
        if "filed_new" in attr:
            data += f'{tag}<result column="{attr["filed_new"]}" property="{attr["attr"]}"/>\n'
        else:
            data += f'{tag}<result column="{attr["filed"]}" property="{attr["attr"]}"/>\n'
    return data


def __create_xml_block_insert_filed_if(config: dict, indent: int, param=None):
    tap = "\t" * indent
    max_len = len(config["attr"])
    data, j = "", 0
    if param:
        param += "."
    else:
        param = ""
    for attr in config["attr"]:
        j = j + 1
        dian = ","
        if j == max_len:
            dian = ""
        data += f'{tap}<if test="{param}{attr["attr"]}!=null">{attr["filed"]}{dian}</if>\n'
    return data


def __create_xml_block_insert_value_if(config: dict, indent: int, param=None):
    tap = "\t" * indent
    max_len = len(config["attr"])
    data, j = "", 0
    if param:
        param += "."
    else:
        param = ""
    for attr in config["attr"]:
        j = j + 1
        dian = ","
        if j == max_len:
            dian = ""
            data += f'{tap}<if test="{param}{attr["attr"]}!=null">#{{{param}{attr["attr"]}}}{dian}</if>\n'
    return data


def __create_xml_block_update_if(config: dict, indent: int, param=None, value_null=False):
    tap = "\t" * indent
    max_len = len(config["attr"])
    data, j = "", 0
    if param:
        param += "."
    else:
        param = ""
    for attr in config["attr"]:
        j = j + 1
        dian = ","
        if j == max_len:
            dian = ""
        t_a = f'{param}{attr["attr"]}'
        t_b = f'#{{{param}{attr["attr"]}}}'
        if value_null:
            t_b = "null"
        data += f'{tap}<if test="{t_a}!=null">{attr["filed"]}={t_b}{dian}</if>\n'
    return data


def __create_xml_block_any_select(config: dict, indent: int, param=None, fuzzy_search=True, table_as_name=None):
    tap = "\t" * indent
    if param:
        name = f'{param}.'
        code = f'{tap}<if test="{param}!=null">\n'
        lost = f"{tap}</if>\n"
        tap += '\t'
    else:
        name = ""
        code = ""
        lost = ""
    if table_as_name:
        table_as_name += "."
    else:
        table_as_name = ""
    data = f'{code}{tap}<if test="{name}{config["key"]["attr"]}!=null">AND {table_as_name}{config["key"]["filed"]}=#{{{name}{config["key"]["attr"]}}}</if>\n'
    data += f'{tap}<if test="{name}{config["key"]["attr"]}==null">\n'
    for attr in config["attr"]:
        data += f'{tap}\t<if test="{name}{attr["attr"]}!=null">AND {table_as_name}{attr["filed"]}=#{{{name}{attr["attr"]}}}</if>\n'
    data += f'{tap}</if>\n'
    data += f'{lost}'
    if fuzzy_search:
        data += __create_xml_block_fuzzy_search_if(config, indent, table_as_name)
    return data


def __create_xml_block_one_to_x_select(config: dict, indent: int, param=True):
    tap = "\t" * indent
    if param:
        name = f'{stringUtil.low_str_first(config["className"])}.'
        code = f'{tap}<if test="{stringUtil.low_str_first(config["className"])}!=null">\n'
        lost = f"{tap}</if>\n"
        tap += '\t'
    else:
        name = ""
        code = ""
        lost = ""
    # if config.get("replacementMapping"):
    table = config["tableName"] + "."
    # else:
    #     table = ""
    data = f'{code}{tap}<if test="{name}{config["key"]["attr"]}!=null">and {table}{config["key"]["filed"]}=#{{{name}{config["key"]["attr"]}}}</if>\n'
    data += f'{tap}<if test="{name}{config["key"]["attr"]}==null">\n'
    for attr in config["attr"]:
        data += f'{tap}\t<if test="{name}{attr["attr"]}!=null">and {table}{attr["filed"]}=#{{{name}{attr["attr"]}}}</if>\n'
    data += f'{tap}</if>\n'
    data += f'{lost}'
    data += __create_xml_block_fuzzy_search_if(config, indent, table)
    return data


def __create_xml_block_fuzzy_search_if(config: dict, indent: int, table=""):
    # if .... and (a like #{keyWord} or b like #{keyword})
    tag = "\t"
    block_str = ""
    if config.get("fuzzySearch") == "true" and "keyWordList" in config and len(config["keyWordList"]) > 0:
        key_word_name = config.get("keyWord").strip()
        if key_word_name == "":
            key_word_name = "keyWord"
        code = ""
        j = 0
        block_str = f'{tag * indent}<if test="{key_word_name}!=null">\n'
        for filed in config["keyWordList"]:
            if j == 0:
                code = f'{table}{filed} like #{{{key_word_name}}}'
                j = 1
            else:
                code += f' or {table}{filed} like #{{{key_word_name}}}'
        block_str += f'{tag * (indent + 1)}and ({code})\n'
        block_str += f'{tag * indent}</if>\n'
    return block_str


# 插入语句块
def _create_xml_insert_block(config: dict):
    tag = "\t"
    data = f'{tag}<insert id="insert{config["className"]}" parameterType="{config["path_pojo"]}.{config["className"]}" useGeneratedKeys="true" keyProperty="{config["key"]["attr"]}" keyColumn="{config["key"]["filed"]}">\n'
    data += f'{tag * 2}insert into {config["tableName"]}(\n'
    data += f'{tag * 2}<trim prefix="" suffixOverrides=",">\n'
    data += __create_xml_block_insert_filed_if(config, 3)
    data += f'{tag * 2}</trim>\n'
    data += f'{tag * 2}) values(\n'
    data += f'{tag * 2}<trim prefix="" suffixOverrides=",">\n'
    data += __create_xml_block_insert_value_if(config, 3)
    data += f"{tag * 2}</trim>\n\t\t)\n"
    data += f'{tag}</insert>\n'
    return data


# 删除语句块
def _create_xml_delete_block(config: dict):
    tag = "\t"
    data = f'{tag}<delete id="delete{config["className"]}By{stringUtil.upper_str_first(config["key"]["attr"])}">\n'
    data += f'{tag * 2}delete from {config["tableName"]} where {config["key"]["filed"]}=#{{{config["key"]["attr"]}}}\n'
    data += f'{tag}</delete>\n'
    return data


def _create_xml_delete_where_block(config: dict):
    tag = "\t"
    code = f' parameterType="{config["path_pojo"]}.{config["className"]}"'
    if config.get("fuzzySearch") == "true" and "keyWordList" in config and len(config["keyWordList"]) > 0:
        code = ""
        select_block = __create_xml_block_any_select(config, 4)
    else:
        select_block = __create_xml_block_any_select(config, 4, False)
    data = f'{tag}<delete id="delete{config["className"]}"{code}>\n'
    data += f'{tag * 2}delete from {config["tableName"]}\n'
    data += f'{tag * 3}<where>\n'
    data += select_block
    data += f'{tag * 3}</where>\n'
    data += f'{tag}</delete>\n'
    return data


# 假删
def _create_xml_false_delete_block(config: dict):
    tag = "\t"
    data = f'{tag}<update id="falseDelete{config["className"]}By{stringUtil.upper_str_first(config["key"]["attr"])}">\n'
    data += f'{tag * 2}update {config["tableName"]} set {config["falseDelete"]}=1 where {config["key"]["filed"]}=#{{{config["key"]["attr"]}}}\n'
    data += f'{tag}</update>\n'
    return data


def _create_xml_update_by_key_block(config: dict):
    tag = "\t"
    data = f'{tag}<update id="update{config["className"]}By{stringUtil.upper_str_first(config["key"]["attr"])}" parameterType="{config["path_pojo"]}.{config["className"]}">\n'
    data += f'{tag * 2}update {config["tableName"]}\n'
    data += f'{tag * 2}<set>\n'
    data += __create_xml_block_update_if(config, 3)
    data += f'{tag * 2}</set>\n'
    data += f'{tag * 2}where {config["key"]["filed"]}=#{{{config["key"]["attr"]}}}\n'
    data += f'{tag}</update>\n'
    return data


def _create_xml_update_by_not_repeat_where_block(config: dict):
    tag = "\t"
    data = f'{tag}<update id="update{config["className"]}ByNotRepeatWhere">\n'
    data += f'{tag * 2}update {config["tableName"]}\n'
    data += f'{tag * 2}<set>\n'
    data += __create_xml_block_update_if(config, 3, f'save{config["className"]}')
    data += f'{tag * 2}</set>\n'
    data += f'{tag * 2}where {config["key"]["filed"]}=#{{save{config["className"]}.{config["key"]["attr"]}}}\n'
    data += f'{tag * 2}<if test="condition{config["className"]}!=null">\n'
    data += f'{tag * 3}AND NOT EXISTS (SELECT {config["key"]["filed"]} FROM (SELECT * FROM {config["tableName"]} ) AS t \n'
    data += f'{tag * 3}<where>\n'
    data += __create_xml_block_any_select(config, 4, f'condition{config["className"]}', False, "t") + '\n'
    data += f'{tag * 3}</where>\n'
    data += f'{tag * 3})\n'
    data += f'{tag * 2}</if>\n'
    data += f'{tag}</update>\n'
    return data


def _create_xml_update(config: dict):
    tag = "\t"
    data = f'{tag}<update id="update{config["className"]}">\n'
    data += f'{tag * 2}update {config["tableName"]}\n'
    data += f'{tag * 2}<set>\n'
    data += __create_xml_block_update_if(config, 3, f'save{config["className"]}')
    data += f'{tag * 2}</set>\n'
    data += f'{tag * 2}<where>\n'
    data += f'{tag * 3}<if test="save{config["className"]}.{config["key"]["attr"]}!=null">\n'
    data += f'{tag * 4}AND {config["key"]["filed"]}=#{{save{config["className"]}.{config["key"]["attr"]}}}\n'
    data += f'{tag * 3}</if>\n'
    data += __create_xml_block_any_select(config, 3, f'condition{config["className"]}', False) + '\n'
    data += f'{tag * 2}</where>\n'
    data += f'{tag}</update>\n'
    return data


def _create_xml_update_set_null_by_key(config: dict):
    tag = "\t"
    data = f'{tag}<update id="update{config["className"]}SetNullBy{stringUtil.upper_str_first(config["key"]["attr"])}" parameterType="{config["path_pojo"]}.{config["className"]}">\n'
    data += f'{tag * 2}update {config["tableName"]}\n'
    data += f'{tag * 2}<set>\n'
    data += __create_xml_block_update_if(config, 3, value_null=True)
    data += f'{tag * 2}</set>\n'
    data += f'{tag * 2}where {config["key"]["filed"]}=#{{{config["key"]["attr"]}}}\n'
    data += f'{tag}</update>\n'
    return data


def _create_xml_select_by_key(config: dict):
    tag = "\t"
    if config["resultMap"] == "true":
        res_type = f'resultMap="res{config["className"]}"'
    else:
        res_type = f'resultType="{config["path_pojo"]}.{config["className"]}"'
    data = f'{tag}<select id="select{config["className"]}By{stringUtil.upper_str_first(config["key"]["attr"])}" {res_type}>\n'
    data += f'{tag * 2}select * from {config["tableName"]} where {config["key"]["filed"]}=#{{{config["key"]["attr"]}}}\n'
    data += f'{tag}</select>\n'
    return data


def _create_xml_select(config: dict):
    tag = "\t"
    if config["resultMap"] == "true":
        res_type = f'resultMap="res{config["className"]}"'
    else:
        res_type = f'resultType="{config["path_pojo"]}.{config["className"]}"'
    data = f'{tag}<select id="select{config["className"]}" {res_type}>\n'
    data += f'{tag * 2}select * from {config["tableName"]}\n'
    data += f'{tag * 2}<where>\n'
    data += __create_xml_block_any_select(config, 3, f'{stringUtil.low_str_first(config["className"])}')
    data += f'{tag * 2}</where>\n'
    data += f'{tag * 2}<if test="page!=null">\n'
    data += f'{tag * 3}limit #{{page.start}},#{{page.count}}\n'
    data += f'{tag * 2}</if>\n'
    data += f'{tag}</select>\n'
    return data


def _create_xml_count(config: dict):
    tag = "\t"
    code = f' parameterType="{config["path_pojo"]}.{config["className"]}"'
    if config.get("fuzzySearch") == "true" and "keyWordList" in config and len(config["keyWordList"]) > 0:
        code = ""
        select_block = __create_xml_block_any_select(config, 3, f'{stringUtil.low_str_first(config["className"])}')
    else:
        select_block = __create_xml_block_any_select(config, 3)
    data = f'{tag}<select id="count{config["className"]}" resultType="int"{code}>\n'
    data += f'{tag * 2}select count(*) from {config["tableName"]}\n'
    data += f'{tag * 2}<where>\n'
    data += select_block
    data += f'{tag * 2}</where>\n'
    data += f'{tag}</select>\n'
    return data


def _create_insert_save_or_update_by_unique(config: dict):
    tag = "\t"
    data = f'{tag}<insert id="saveOrUpdate{config["className"]}ByUnique" parameterType="{config["path_pojo"]}.{config["className"]}" useGeneratedKeys="true" keyProperty="{config["key"]["attr"]}" keyColumn="{config["key"]["filed"]}">\n'
    data += f'{tag * 2}insert into {config["tableName"]}(\n'
    data += f'{tag * 2}<trim prefix="" suffixOverrides=",">\n'
    data += __create_xml_block_insert_filed_if(config, 3)
    data += f'{tag * 2}</trim>\n'
    data += f'{tag * 2}) values(\n'
    data += f'{tag * 2}<trim prefix="" suffixOverrides=",">\n'
    data += __create_xml_block_insert_value_if(config, 3)
    data += f"{tag * 2}</trim>\n\t\t) ON DUPLICATE KEY UPDATE \n"
    data += f'{tag * 2}<trim prefix="" suffixOverrides=",">\n'
    data += __create_xml_block_update_if(config, 3)
    data += f'{tag * 2}</trim>\n'
    data += f'{tag}</insert>\n'
    return data


def _create_insert_saver_or_update_by_where(config: dict):
    tag = "\t"
    data = f'{tag}<insert id="saveOrUpdate{config["className"]}ByWhere">\n'
    data += f'{tag * 2}<selectKey keyProperty="condition{config["className"]}.{config["key"]["attr"]}"  keyColumn="{config["key"]["filed"]}" resultType="int" order="BEFORE">\n'
    data += f'{tag * 3}select IFNULL((\n'
    data += f'{tag * 4}select {config["key"]["filed"]} from {config["tableName"]}\n'
    data += f'{tag * 4}<where>\n'
    data += __create_xml_block_any_select(config, 5, f'condition{config["className"]}', False)
    data += f'{tag * 4}</where>\n'
    data += f'{tag * 3}),null)\n'
    data += f'{tag * 2}</selectKey>\n'

    data += f'{tag * 2}<if test="condition{config["className"]}.{config["key"]["attr"]}==null">\n'
    data += f'{tag * 3}insert into {config["tableName"]}(\n'
    data += f'{tag * 3}<trim prefix="" suffixOverrides=",">\n'
    data += __create_xml_block_insert_filed_if(config, 4, f'save{config["className"]}')
    data += f'{tag * 3}</trim>\n'
    data += f'{tag * 3}) values(\n'
    data += f'{tag * 3}<trim prefix="" suffixOverrides=",">\n'
    data += __create_xml_block_insert_value_if(config, 4, f'save{config["className"]}')
    data += f"{tag * 3}</trim>\n{tag * 2})\n"
    data += f'{tag * 2}</if>\n'

    data += f'{tag * 2}<if test="condition{config["className"]}.{config["key"]["attr"]}!=null">\n'
    data += f'{tag * 3}update {config["tableName"]}\n'
    data += f'{tag * 3}<set>\n'
    data += __create_xml_block_update_if(config, 4, f'save{config["className"]}')
    data += f'{tag * 3}</set>\n'
    data += f'{tag * 3}where {config["key"]["filed"]}=#{{condition{config["className"]}.{config["key"]["attr"]}}}\n'
    data += f'{tag * 2}</if>\n'
    data += f'{tag}</insert>\n'
    return data


def _create_insert_by_where_insert(config: dict):
    tag = "\t"
    data = f'{tag}<insert id="insert{config["className"]}ByWhereOnlySave" useGeneratedKeys="true" keyProperty="save{config["className"]}.{config["key"]["attr"]}" keyColumn="{config["key"]["filed"]}">\n'
    data += f'{tag * 2}insert into {config["tableName"]}(\n'
    data += f'{tag * 2}<trim prefix="" suffixOverrides=",">\n'
    data += __create_xml_block_insert_filed_if(config, 3, f'save{config["className"]}')
    data += f'{tag * 2}</trim>\n'
    data += f'{tag * 2}) select \n'
    data += f'{tag * 2}<trim prefix="" suffixOverrides=",">\n'
    data += __create_xml_block_insert_value_if(config, 3, f'save{config["className"]}')
    data += f"{tag * 2}</trim>\n"
    data += f'{tag * 2}FROM DUAL WHERE NOT EXISTS(\n'
    data += f'{tag * 3}select {config["key"]["filed"]} from {config["tableName"]}\n'
    data += f'{tag * 3}<where>\n'
    data += __create_xml_block_any_select(config, 4, f'condition{config["className"]}', False)
    data += f'{tag * 3}</where>\n'
    data += f'{tag * 2})\n'
    data += f'{tag}</insert>\n'
    return data


def __create_find_or_query_one_to_one(config: dict, select_type: str, inline=True):
    tag = "\t"
    method_str = ""
    if "oneToOne" in config:
        for obj in config["oneToOne"]:
            if config["replacementMapping"]:
                select_filed = f'\n{tag * 3}<include refid="sql_filed_{config["tableName"]}"/>,\n'
                select_filed += f'{tag * 3}<include refid="sql_filed_{obj["tableName"]}"/>\n{tag * 2}'
            else:
                select_filed = "* "
            data = f'{tag}<select id="{select_type}{config["className"]}OneToOne{obj["className"]}" resultMap="res{config["className"]}MultiTable">\n'
            if inline:
                data += f'{tag * 2}select {select_filed}from {config["tableName"]},{obj["tableName"]}\n'
                data += f'{tag * 2}<where>\n'
                data += f'{tag * 3}{config["tableName"]}.{obj["foreign_key"]} = {obj["tableName"]}.{obj["key"]["filed"]}\n'
            else:
                data += f'{tag * 2}select {select_filed}from {config["tableName"]} LEFT JOIN {obj["tableName"]} ON {config["tableName"]}.{obj["foreign_key"]} = {obj["tableName"]}.{obj["key"]["filed"]}\n'
                data += f'{tag * 2}<where>\n'
            data += __create_xml_block_one_to_x_select(config, 3)
            data += __create_xml_block_one_to_x_select(obj, 3)
            data += f'{tag * 2}</where>\n'
            data += f'{tag * 2}<if test="page!=null">\n'
            data += f'{tag * 3}limit #{{page.start}},#{{page.count}}\n'
            data += f'{tag * 2}</if>\n'
            data += f'{tag}</select>\n'
            method_str += data + '\n'
    return method_str


def __create_count_find_or_query_one_to_one(config: dict, select_type: str, inline=True):
    tag = "\t"
    method_str = ""
    if "oneToOne" in config:
        for obj in config["oneToOne"]:
            select_filed = "count(*) "
            data = f'{tag}<select id="count{stringUtil.upper_str_first(select_type)}{config["className"]}OneToOne{obj["className"]}" resultType="int">\n'
            if inline:
                data += f'{tag * 2}select {select_filed}from {config["tableName"]},{obj["tableName"]}\n'
                data += f'{tag * 2}<where>\n'
                data += f'{tag * 3}{config["tableName"]}.{obj["foreign_key"]} = {obj["tableName"]}.{obj["key"]["filed"]}\n'
            else:
                data += f'{tag * 2}select {select_filed}from {config["tableName"]} LEFT JOIN {obj["tableName"]} ON {config["tableName"]}.{obj["foreign_key"]} = {obj["tableName"]}.{obj["key"]["filed"]}\n'
                data += f'{tag * 2}<where>\n'
            data += __create_xml_block_one_to_x_select(config, 3)
            data += __create_xml_block_one_to_x_select(obj, 3)
            data += f'{tag * 2}</where>\n'
            data += f'{tag}</select>\n'
            method_str += data + '\n'
    return method_str


def __create_find_or_query_one_to_many(config: dict, select_type: str, inline=True):
    tag = "\t"
    method_str = ""
    if "oneToMany" in config:
        for obj in config["oneToMany"]:
            if config["replacementMapping"]:
                select_filed_left = f'\n{tag * 4}<include refid="sql_filed_{config["tableName"]}"/>\n{tag * 3}'
                select_filed_right = f'\n{tag * 4}<include refid="sql_filed_{obj["tableName"]}"/>\n{tag * 3}'
            else:
                select_filed_left = "* "
                select_filed_right = "* "

            data = f'{tag}<select id="{select_type}{config["className"]}OneToMany{obj["className"]}" resultMap="res{config["className"]}MultiTable">\n'
            subquery1 = f'{tag * 3}select {select_filed_left}from {config["tableName"]}\n'
            subquery1 += f'{tag * 3}<where>\n'
            subquery1 += __create_xml_block_one_to_x_select(config, 4)
            subquery1 += f'{tag * 3}</where>\n'
            subquery1 += f'{tag * 3}<if test="page!=null">\n'
            subquery1 += f'{tag * 4}limit #{{page.start}},#{{page.count}}\n'
            subquery1 += f'{tag * 3}</if>\n'

            subquery2 = f'{tag * 3}select {select_filed_right}from {obj["tableName"]}\n'
            subquery2 += f'{tag * 3}<where>\n'
            subquery2 += __create_xml_block_one_to_x_select(obj, 4)
            subquery2 += f'{tag * 3}</where>\n'
            subquery2 += f'{tag * 3}<if test="page1!=null">\n'
            subquery2 += f'{tag * 4}limit #{{page1.start}},#{{page1.count}}\n'
            subquery2 += f'{tag * 3}</if>\n'

            my_key = config["key"]["filed"]
            if "bean_info" in config:
                my_key = config["bean_info"]["key"]["filed"]
            r_key = obj["foreign_key"]
            if "rep_obj" in config:
                if config["rep_obj"].get(obj["tableName"]):
                    if config["rep_obj"].get(obj["tableName"]).get("foreign_key_new"):
                        r_key = config["rep_obj"].get(obj["tableName"]).get("foreign_key_new")
            if inline:
                data += f'{tag * 2}select * from (\n{subquery1}{tag * 2}) AS temp_{config["tableName"]},(\n{subquery2}{tag * 2}) AS temp_{obj["tableName"]}\n'
                data += f'{tag * 2}where\n'
                data += f'{tag * 3}temp_{config["tableName"]}.{my_key} = temp_{obj["tableName"]}.{r_key}\n'
            else:
                data += f'{tag * 2}select * from (\n{subquery1}{tag * 2}) AS temp_{config["tableName"]} LEFT JOIN (\n{subquery2}{tag * 2}) AS temp_{obj["tableName"]}\n'
                data += f'{tag * 2}ON temp_{config["tableName"]}.{my_key} = temp_{obj["tableName"]}.{r_key}\n'
            data += f'{tag}</select>\n'
            method_str += data + '\n'
    return method_str


def __create_count_find_or_query_one_to_many(config: dict, select_type: str, inline=True):
    tag = "\t"
    method_str = ""
    if "oneToMany" in config:
        for obj in config["oneToMany"]:
            if config["replacementMapping"]:
                select_filed_left = f'\n{tag * 4}<include refid="sql_filed_{config["tableName"]}"/>\n{tag * 3}'
                select_filed_right = f'\n{tag * 4}<include refid="sql_filed_{obj["tableName"]}"/>\n{tag * 3}'
            else:
                select_filed_left = "* "
                select_filed_right = "* "

            data = f'{tag}<select id="count{stringUtil.upper_str_first(select_type)}{config["className"]}OneToMany{obj["className"]}" resultType="int">\n'
            subquery1 = f'{tag * 3}select {select_filed_left}from {config["tableName"]}\n'
            subquery1 += f'{tag * 3}<where>\n'
            subquery1 += __create_xml_block_one_to_x_select(config, 4)
            subquery1 += f'{tag * 3}</where>\n'
            subquery1 += f'{tag * 3}<if test="page!=null">\n'
            subquery1 += f'{tag * 4}limit #{{page.start}},#{{page.count}}\n'
            subquery1 += f'{tag * 3}</if>\n'

            subquery2 = f'{tag * 3}select {select_filed_right}from {obj["tableName"]}\n'
            subquery2 += f'{tag * 3}<where>\n'
            subquery2 += __create_xml_block_one_to_x_select(obj, 4)
            subquery2 += f'{tag * 3}</where>\n'
            subquery2 += f'{tag * 3}<if test="page1!=null">\n'
            subquery2 += f'{tag * 4}limit #{{page1.start}},#{{page1.count}}\n'
            subquery2 += f'{tag * 3}</if>\n'

            my_key = config["key"]["filed"]
            if "bean_info" in config:
                my_key = config["bean_info"]["key"]["filed"]
            r_key = obj["foreign_key"]
            if "rep_obj" in config:
                if config["rep_obj"].get(obj["tableName"]):
                    if config["rep_obj"].get(obj["tableName"]).get("foreign_key_new"):
                        r_key = config["rep_obj"].get(obj["tableName"]).get("foreign_key_new")
            if inline:
                data += f'{tag * 2}select count(DISTINCT temp_{config["tableName"]}.{my_key}) from (\n{subquery1}{tag * 2}) AS temp_{config["tableName"]},(\n{subquery2}{tag * 2}) AS temp_{obj["tableName"]}\n'
                data += f'{tag * 2}where\n'
                data += f'{tag * 3}temp_{config["tableName"]}.{my_key} = temp_{obj["tableName"]}.{r_key}\n'
            else:
                data += f'{tag * 2}select count(DISTINCT temp_{config["tableName"]}.{my_key}) from (\n{subquery1}{tag * 2}) AS temp_{config["tableName"]} LEFT JOIN (\n{subquery2}{tag * 2}) AS temp_{obj["tableName"]}\n'
                data += f'{tag * 2}ON temp_{config["tableName"]}.{my_key} = temp_{obj["tableName"]}.{r_key}\n'
            data += f'{tag}</select>\n'
            method_str += data + '\n'
    return method_str


def __create_find_or_query_many_to_many(config: dict, select_type: str, inline=True):
    tag = "\t"
    method_str = ""
    if "manyToMany" in config:
        for obj in config["manyToMany"]:
            if config["replacementMapping"]:
                select_filed_main = f'\n{tag * 4}<include refid="sql_filed_{config["tableName"]}"/>\n{tag * 3}'
                select_filed_join = f'\n{tag * 3}<include refid="sql_filed_{obj["many"]["tableName"]}"/>,\n{tag * 3}temp_{config["tableName"]}.*\n{tag * 2}'
            else:
                select_filed_main = "* "
                select_filed_join = "* "

            data = f'{tag}<select id="{select_type}{config["className"]}ManyToManyLink{obj["to"]["className"]}On{obj["many"]["className"]}" resultMap="res{config["className"]}MultiTable">\n'
            subquery = f'{tag * 3}select {select_filed_main}from {config["tableName"]}\n'
            subquery += f'{tag * 3}<where>\n'
            subquery += __create_xml_block_one_to_x_select(config, 4)
            subquery += f'{tag * 3}</where>\n'
            subquery += f'{tag * 3}<if test="page!=null">\n'
            subquery += f'{tag * 4}limit #{{page.start}},#{{page.count}}\n'
            subquery += f'{tag * 3}</if>\n'
            my_key = config["key"]["filed"]
            if "bean_info" in config:
                my_key = config["bean_info"]["key"]["filed"]
            if inline:
                data += f'{tag * 2}select {select_filed_join}from (\n{subquery}{tag * 2}) AS temp_{config["tableName"]},{obj["to"]["tableName"]},{obj["many"]["tableName"]}\n'
                data += f'{tag * 2}where temp_{config["tableName"]}.{my_key} = {obj["to"]["tableName"]}.{obj["to"]["foreign_key"]}\n'
                data += f'{tag * 2}AND {obj["to"]["tableName"]}.{obj["many"]["foreign_key"]} = {obj["many"]["tableName"]}.{obj["many"]["key"]["filed"]}\n'
            else:
                data += f'{tag * 2}select {select_filed_join}from (\n{subquery}{tag * 2}) AS temp_{config["tableName"]} LEFT JOIN {obj["to"]["tableName"]}\n'
                data += f'{tag * 2}ON temp_{config["tableName"]}.{my_key} = {obj["to"]["tableName"]}.{obj["to"]["foreign_key"]}\n'
                data += f'{tag * 2}LEFT JOIN {obj["many"]["tableName"]} On {obj["to"]["tableName"]}.{obj["many"]["foreign_key"]} = {obj["many"]["tableName"]}.{obj["many"]["key"]["filed"]}\n'
            data += f'{tag}</select>\n'
            method_str += data + '\n'
    return method_str


def _create_xml_x_to_x_block(config: dict):
    method_str = ""
    # 一对一不需要解决查询的结果命名和条件问题
    method_str += __create_find_or_query_one_to_one(config, "find")
    method_str += __create_count_find_or_query_one_to_one(config, "find")
    method_str += __create_find_or_query_one_to_one(config, "query", False)
    # 左外连由左表决定
    # method_str += __create_count_find_or_query_one_to_one(config, "query", False)
    method_str += __create_find_or_query_one_to_many(config, "find")
    method_str += __create_count_find_or_query_one_to_many(config, "find")
    method_str += __create_find_or_query_one_to_many(config, "query", False)
    # 左外连最终条数由左表决定
    # method_str += __create_count_find_or_query_one_to_many(config, "query", False)
    method_str += __create_find_or_query_many_to_many(config, "find")
    method_str += __create_find_or_query_many_to_many(config, "query", False)
    return method_str


def _create_insert_list(config: dict):
    tag = "\t"
    data = f'{tag}<insert id="insert{config["className"]}List" parameterType="java.util.List" useGeneratedKeys="true" keyProperty="{config["key"]["attr"]}" keyColumn="{config["key"]["filed"]}">\n'
    data += f'{tag * 2}insert into {config["tableName"]}(\n'
    data += f'{tag * 3}'
    max_len = len(config["attr"])
    j = 0
    for attr in config["attr"]:
        j = j + 1
        if j == max_len:
            data += f'{attr["filed"]}\n'
        else:
            data += f'{attr["filed"]},'
    data += f'{tag * 2}) values\n'
    data += f'{tag * 2}<foreach collection="list" index="index" item="obj" separator=",">\n'
    data += f'{tag * 3}(\n'
    j = 0
    for attr in config["attr"]:
        j = j + 1
        if j == max_len:
            data += f'{tag * 4}#{{obj.{attr["attr"]}}}\n'
        else:
            data += f'{tag * 4}#{{obj.{attr["attr"]}}},\n'
    data += f'{tag * 3})\n'
    data += f'{tag * 2}</foreach>\n'
    data += f'{tag}</insert>\n'
    return data


def _create_xml_select_one(config: dict):
    tag = "\t"
    if config["resultMap"] == "true":
        res_type = f'resultMap="res{config["className"]}"'
    else:
        res_type = f'resultType="{config["path_pojo"]}.{config["className"]}"'
    data = f'{tag}<select id="selectOne{config["className"]}" {res_type}>\n'
    data += f'{tag * 2}select * from {config["tableName"]}\n'
    data += f'{tag * 2}<where>\n'
    data += __create_xml_block_any_select(config, 3, f'{stringUtil.low_str_first(config["className"])}')
    data += f'{tag * 2}</where>\n'
    data += f'{tag * 2}limit #{{index}},1\n'
    data += f'{tag}</select>\n'
    return data
