from src.util import stringUtil


def create_xml_mapper(config: dict):
    data = __create_xml_head(config) + '\n'
    data += __create_result_map(config) + '\n'
    data += _create_xml_select(config) + '\n'

    data += __create_xml_tail() + '\n'
    return data


def __create_xml_head(config: dict):
    data = '<?xml version="1.0" encoding="UTF-8"?>\n'
    data += '<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "http://mybatis.org/dtd/mybatis-3-mapper.dtd">\n'
    data += f'<mapper namespace="{config["extradimensionalData"]["path_xml_mapper"]}.{config["extradimensionalData"]["XMLMapperName"]}">\n'
    return data


def __create_xml_tail():
    return "</mapper>\n"


def __table_filed_list(obj: dict) -> list:
    lists = [obj["key"].copy()]
    for i in obj["attr"]:
        lists.append(i.copy())
    return lists


def __create_result_map(config: dict) -> str:
    tag = "\t"
    data = ""
    data += f'{tag}<resultMap type="{config["path_pojo"]}.{config["className"]}" id="{config["resultMapName"]}" extends="{config["path_xml_mapper"]}.{config["XMLMapperName"]}.{config["resultMapName"]}">\n'
    data += f'{tag}</resultMap>\n\n'

    data += f'{tag}<resultMap type="{config["extradimensionalData"]["path_pojo"]}.{config["extradimensionalData"]["className"]}" id="res{config["extradimensionalData"]["className"]}">\n'
    data += __create_method_result_map_key_value(config["extradimensionalData"], 2)
    data += f'{tag}</resultMap>\n\n'
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
        elif "filed" in attr:
            data += f'{tag}<result column="{attr["filed"]}" property="{attr["attr"]}"/>\n'
    return data


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
        return ""
    string_block = ""
    for table in tables:
        data = f'<sql id="sql_filed_{table}"><include refid="{config["path_xml_mapper"]}.{config["XMLAutoMapperName"]}.sql_filed_{table}"/></sql>'
        string_block += f'{tag}{data}\n'
    string_block += "\n"
    bean_info = {"resultMapName": f'res{config["className"]}MultiTable', "oneToMany": [], "oneToOne": []}
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
            pass
        else:
            bean_info.update(obj)
    # 此处加入config中主要针对子查询中，字段名被替换无法找到原本字段名问题
    config["bean_info"] = bean_info
    bean_info["path_xml_mapper"] = config["path_xml_mapper"]
    bean_info["XMLAutoMapperName"] = config["XMLAutoMapperName"]
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
    # string_block += data
    return string_block


def _create_xml_select(config: dict):
    tag = "\t"
    res_type = f'resultMap="res{config["extradimensionalData"]["className"]}"'
    data = f'{tag}<select id="select{config["extradimensionalData"]["className"]}" {res_type}>\n'
    data += f'{tag * 2}select * from {config["tableName"]}\n'
    data += f'{tag * 2}<where>\n'
    data += __create_xml_block_any_select(config, 3, f'{stringUtil.low_str_first(config["className"])}')
    data += f'{tag * 2}</where>\n'
    if config.get("SQLInjection") == "true":
        data += f'{tag * 2}<if test="SQLInjection!=null">\n'
        data += f'{tag * 3}${{SQLInjection}}\n'
        data += f'{tag * 2}</if>\n'
    data += f'{tag * 2}<if test="page!=null">\n'
    data += f'{tag * 3}limit #{{page.start}},#{{page.count}}\n'
    data += f'{tag * 2}</if>\n'
    data += f'{tag}</select>\n'
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
    for attr in config["attr"]:
        if "Date" == attr.get("type"):
            data += f'{tap}<if test="{name}{attr["attr"]}!=null">AND DATE({table_as_name}{attr["filed"]})=DATE(#{{{name}{attr["attr"]}}})</if>\n'
        else:
            data += f'{tap}<if test="{name}{attr["attr"]}!=null">AND {table_as_name}{attr["filed"]}=#{{{name}{attr["attr"]}}}</if>\n'
    data += f'{lost}'
    if fuzzy_search:
        data += __create_xml_block_fuzzy_search_if(config, indent, table_as_name)
    return data


def __create_xml_block_fuzzy_search_if(config: dict, indent: int, table="", key_word_index=""):
    # if .... and (a like #{keyWord} or b like #{keyword})
    tag = "\t"
    block_str = ""
    if config.get("fuzzySearch") == "true" and "keyWordList" in config and len(config["keyWordList"]) > 0:
        key_word_name = config.get("keyWord")
        if key_word_name is not None:
            key_word_name = key_word_name.strip()
        else:
            key_word_name = "keyWord"
        if key_word_name == "":
            key_word_name = "keyWord"
        code = ""
        j = 0
        block_str = f'{tag * indent}<if test="{key_word_name}{key_word_index}!=null">\n'
        for filed in config["keyWordList"]:
            if j == 0:
                code = f'{table}{filed} like #{{{key_word_name}{key_word_index}}}'
                j = 1
            else:
                code += f' or {table}{filed} like #{{{key_word_name}{key_word_index}}}'
        block_str += f'{tag * (indent + 1)}and ({code})\n'
        block_str += f'{tag * indent}</if>\n'
    return block_str
