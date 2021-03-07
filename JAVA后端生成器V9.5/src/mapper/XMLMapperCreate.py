from src.util import stringUtil
import re


def create_xml_mapper(config: dict):
    data = __create_xml_head(config) + '\n'
    data += __check_res_filed_repeat(config) + '\n'
    data += __create_result_map(config) + '\n'
    data += __create_xml_tail() + '\n'
    return data


def __create_xml_head(config: dict):
    data = '<?xml version="1.0" encoding="UTF-8"?>\n'
    data += '<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "http://mybatis.org/dtd/mybatis-3-mapper.dtd">\n'
    data += f'<mapper namespace="{config["path_xml_mapper"]}.{config["XMLMapperName"]}">\n'
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
    if config.get("oneToOne") or config.get("oneToMany") or config.get("manyToMany"):
        data += f'{tag}<resultMap type="{config["path_pojo"]}.{config["className"]}" id="res{config["className"]}MultiTable" extends="{config["path_xml_mapper"]}.{config["XMLAutoMapperName"]}.res{config["className"]}MultiTable">\n'
        data += f'{tag}</resultMap>\n\n'
    data += f'{tag}<resultMap type="{config["path_pojo"]}.{config["className"]}" id="{config["resultMapName"]}" extends="{config["path_xml_mapper"]}.{config["XMLAutoMapperName"]}.{config["resultMapName"]}">\n'
    data += f'{tag}</resultMap>\n\n'
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
