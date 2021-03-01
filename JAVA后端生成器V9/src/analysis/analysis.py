import json
from src.util import mysqlUtil
from src.util import stringUtil
import os
import copy


class Attribute:
    def __init__(self):
        self.Field = None
        self.Type = None
        self.Null = None
        self.Key = None
        self.Default = None
        self.Extra = None

    def __str__(self):
        return str(self.__dict__)


class DataBase:
    pass


def mapper_dict_set(data: dict, key: str, value: str):
    if key not in data:
        data[key] = set()
    data[key].add(value)


def get_attribute_object(obj: Attribute, attr_name: str) -> dict:
    return {"attr": attr_name, "filed": obj.Field, "type": stringUtil.get_java_type(obj.Type)}


def set_project_model(model: str, table_name: str, bean_info: dict):
    if model is None:
        bean_info["path_pojo"] += "." + "pojo"
        bean_info["path_service"] += "." + "service"
        bean_info["path_service_impl"] += "." + "service.impl"
        bean_info["path_java_mapper"] += "." + "mapper"
        bean_info["path_xml_mapper"] += "." + "mapper"
        bean_info["path_controller"] += "." + "controller"
        return

    if model.lower() == "model".lower():
        suffix = table_name.replace("_", "").lower()
        bean_info["path_pojo"] += "." + suffix
        bean_info["path_service"] += "." + suffix
        bean_info["path_service_impl"] += "." + suffix
        bean_info["path_java_mapper"] += "." + suffix
        bean_info["path_xml_mapper"] += "." + suffix
        bean_info["path_controller"] += "." + suffix + ".controller"
    elif model.lower() == "superModel".lower():
        suffix = table_name.replace("_", ".").lower()
        bean_info["path_pojo"] += "." + suffix
        bean_info["path_service"] += "." + suffix
        bean_info["path_service_impl"] += "." + suffix
        bean_info["path_java_mapper"] += "." + suffix
        bean_info["path_xml_mapper"] += "." + suffix
        bean_info["path_controller"] += "." + suffix + ".controller"
    elif model.lower() == "XMLModel".lower():
        suffix = table_name.replace("_", "").lower()
        bean_info["path_pojo"] += "." + suffix
        bean_info["path_service"] += "." + suffix
        bean_info["path_service_impl"] += "." + suffix
        bean_info["path_java_mapper"] += "." + suffix
        bean_info["path_xml_mapper"] += "." + "mapper"
        bean_info["path_controller"] += "." + suffix + ".controller"
    elif model.lower() == "superXMLModel".lower():
        suffix = table_name.replace("_", ".").lower()
        bean_info["path_pojo"] += "." + suffix
        bean_info["path_service"] += "." + suffix
        bean_info["path_service_impl"] += "." + suffix
        bean_info["path_java_mapper"] += "." + suffix
        bean_info["path_xml_mapper"] += "." + "mapper"
        bean_info["path_controller"] += "." + suffix + ".controller"
    else:
        bean_info["path_pojo"] += "." + "pojo"
        bean_info["path_service"] += "." + "service"
        bean_info["path_service_impl"] += "." + "service.impl"
        bean_info["path_java_mapper"] += "." + "mapper"
        bean_info["path_xml_mapper"] += "." + "mapper"
        bean_info["path_controller"] += "." + "controller"


class SQLLinkUtil:

    def __init__(self, json_conf: dict):
        print("正则装在配置")
        # 数据库名
        self.database = json_conf["database"]
        # 如果是单表则提取表名，可选项，用于区分是生成全库还是单表
        self.table = json_conf.get("table")
        if "table" in json_conf and len(json_conf["table"]) < 1:
            self.table = None
        # 数据库链接相关
        host = json_conf.get("host")
        if host is None:
            host = "127.0.0.1"
        name = json_conf.get("name")
        if name is None:
            name = "root"
        password = json_conf.get("password")
        if password is None:
            password = "123456"
        port = json_conf.get("port")
        if port is None:
            port = "3306"
        port = int(port)
        # 项目根路径
        self.project = json_conf["project"]
        # 是否采用下划线替换
        self.underscoreReplace = False
        if json_conf.get("underscoreReplace") == "true":
            self.underscoreReplace = True
        # 其他杂项功能
        # 是否采用restful风格
        self.restful = False
        if json_conf.get("restful") == "true":
            self.restful = True
        # 是否自动装配模糊搜索
        self.fuzzySearch = False
        self.fuzzySearchList = None
        if json_conf.get("fuzzySearch") == "true":
            self.fuzzySearch = True
            if "fuzzySearchList" in json_conf:
                # 把列表中的全部变成字典
                self.fuzzySearchList={}
                for i in json_conf["fuzzySearchList"]:
                    if isinstance(i, dict):
                        self.fuzzySearchList.update(i)
                    else:
                        self.fuzzySearchList[i] = None
        # resultMap替换resultType
        self.resMap = False
        if json_conf.get("resMap") == "true":
            self.resMap = True
        # 自动映射表关系
        self.multiTable = False
        if json_conf.get("multiTable") == "true":
            self.multiTable = True
        # 完全替换重名
        self.multiName = False
        if json_conf.get("multiName") == "true":
            self.multiName = True
        # 生成的文件
        self.createFile = None
        if "createFile" in json_conf:
            self.createFile = json_conf["createFile"]
            if not isinstance(self.createFile, list):
                self.createFile = None
        # 不生成的文件
        self.notCreateFile = None
        if "notCreateFile" in json_conf:
            self.notCreateFile = json_conf["notCreateFile"]
            if not isinstance(self.notCreateFile, list):
                self.createFile = None
        # 假删相关
        self.falseDelete = False
        if json_conf.get("falseDelete"):
            self.falseDelete = True
            if self.underscoreReplace:
                self.falseDeleteFlag = "delete_flag"
            else:
                self.falseDeleteFlag = "deleteflag"
        if "falseDeleteFlag" in json_conf and len(json_conf["falseDeleteFlag"]) > 0 and isinstance(
                json_conf["falseDeleteFlag"], str):
            self.falseDeleteFlag = json_conf["falseDeleteFlag"]
        # 生成模式
        # 生成模式有多种
        # 不填，def，传统MVC三层模式
        # model，模块化模式，一个表对应一个模块包
        # superModel，超级模块化模式，如果表具有task,task_map,task_data,则生成,com.xxx.task,com.xxx.task.map.com.xxx.task.data
        # XMLModel,xml独立为一个模块，com.xxx.mapper，其余采用model模式
        # superXMLModel,在XMLModel的基础上，加入super模式
        self.pageModel = json_conf.get("pageModel")
        # 去除表的统一前缀进行生成
        self.tablePrefix = json_conf.get("tablePrefix")
        # 去除字段前表名的前缀
        self.attrPrefix = json_conf.get("attrPrefix")
        self.util = json_conf.get("util")
        if self.util is None or len(self.util) < 1:
            self.util = self.project + ".util"
        else:
            self.util = self.project + "." + self.util.strip(".")
        # 一对多，一对一相关
        self.oneToOne = json_conf.get("oneToOne")
        if self.oneToOne is None:
            self.oneToOne = {}
        self.oneToMany = json_conf.get("oneToMany")
        if self.oneToMany is None:
            self.oneToMany = {}
        self.noUserAPI = []
        if "noUserAPI" in json_conf:
            self.noUserAPI = json_conf["noUserAPI"]
        self.noAdminAIP = []
        if "noAdminAIP" in json_conf:
            self.noAdminAIP = json_conf["noAdminAIP"]
        # SQL注入项装配
        self.SQLInjection = json_conf.get("SQLInjection") == "true"
        print("装在完成")
        self.tables = {}
        print("正在链接数据库.....")
        self.mysql = mysqlUtil.MySql(self.database, host=host, name=name, password=password, port=port)
        print("链接成功！")

    def get_all_table(self):
        sql = "show full tables where Table_Type = 'BASE TABLE';"
        tables = self.mysql.execute_select(sql, DataBase)
        print(f"查询到表数量：{len(tables)}")
        temp = []
        for i in tables:
            temp.append(getattr(i, f'Tables_in_{self.database}'))
        tables = temp
        for i in tables:
            sql = f"desc {i}"
            attrs = self.mysql.execute_select(sql, Attribute)
            bean_info = dict()
            class_name = i
            # 去除表前缀，并且不区分大小写
            if self.tablePrefix:
                class_name = stringUtil.remove_prefix_not_case(class_name, self.tablePrefix)
            # 转大驼峰类名
            bean_info["className"] = stringUtil.underscore_to_big_hump(class_name)
            bean_info["tableName"] = i
            bean_info["attr"] = []
            # 属性封装
            for j in attrs:
                attr_name = j.Field
                # 去除字段的表名前缀，不区分大小写
                if self.attrPrefix == "true":
                    attr_name = stringUtil.remove_prefix_not_case(attr_name, class_name)
                # 下划线转驼峰
                if self.underscoreReplace:
                    attr_name = stringUtil.underscore_to_small_hump(attr_name)
                if j.Key == "PRI":
                    bean_info["key"] = get_attribute_object(j, attr_name)
                else:
                    bean_info["attr"].append(get_attribute_object(j, attr_name))
            # 文件路径封装
            bean_info["path_pojo"] = self.project
            bean_info["path_service"] = self.project
            bean_info["path_service_impl"] = self.project
            bean_info["path_java_mapper"] = self.project
            bean_info["path_xml_mapper"] = self.project
            bean_info["path_controller"] = self.project
            bean_info["path_util"] = self.util
            # 路径生成选择
            set_project_model(self.pageModel, class_name, bean_info)
            # 各个文件类名称
            bean_info["serviceName"] = f"{bean_info['className']}Service"
            bean_info["serviceImplName"] = f"{bean_info['className']}ServiceImpl"
            bean_info["javaMapperName"] = f"{bean_info['className']}Mapper"
            bean_info["XMLMapperName"] = f"{bean_info['className']}Mapper"
            # 自动生成的
            bean_info["javaAutoMapperName"] = f"{bean_info['className']}AutoMapper"
            bean_info["XMLAutoMapperName"] = f"{bean_info['className']}AutoMapper"

            bean_info["controllerName"] = f"{bean_info['className']}Controller"
            # 其他默认行为参数
            # 默认的resultMap名称
            bean_info["resultMapName"] = f'res{bean_info["className"]}'
            if self.multiName:
                bean_info["multiName"] = self.multiName
            # 模糊搜索
            if self.fuzzySearch:
                bean_info["fuzzySearch"] = "true"
                bean_info["keyWord"] = "keyWord"
                bean_info["keyWordList"] = []

                if self.fuzzySearchList is not None and bean_info["tableName"] in self.fuzzySearchList:
                    # 如果查询中没有列表，则默认全部查
                    if self.fuzzySearchList.get(bean_info["tableName"]) is None:
                        for attr in bean_info["attr"]:
                            if attr["type"] == "String":
                                bean_info["keyWordList"].append(attr["filed"])
                    else:
                        for attr1 in bean_info["attr"]:
                            for attr2 in self.fuzzySearchList[bean_info["tableName"]]:
                                if attr1["type"] == "String" and attr2 == attr1["filed"]:
                                    bean_info["keyWordList"].append(attr1["filed"])
                # 如果没有配置，则全部扫描
                elif self.fuzzySearchList is None or len(self.fuzzySearchList) == 0:
                    for attr in bean_info["attr"]:
                        if attr["type"] == "String":
                            bean_info["keyWordList"].append(attr["filed"])
                if len(bean_info["keyWordList"]) == 0:
                    # 如果查找不到字符类型，则删除，防止删除失败，设置模糊搜索不启用
                    bean_info["fuzzySearch"] = "false"
                    del bean_info["fuzzySearch"]
                    del bean_info["keyWord"]
                    del bean_info["keyWordList"]
            # restful是否启用？
            if self.restful:
                bean_info["restful"] = "true"
            # 默认开启res替换
            if self.resMap:
                bean_info["resultMap"] = "true"
            # 生成的文件
            if self.createFile:
                bean_info["createFile"] = self.createFile
            # 不生成的文件
            if self.notCreateFile:
                bean_info["notCreateFile"] = self.notCreateFile
            # SQL注入项
            if self.SQLInjection:
                bean_info["SQLInjection"] = "true"
            # 装配不生成接口
            bean_info["userAPI"] = "true"
            if i in self.noUserAPI:
                bean_info["userAPI"] = "false"
            bean_info["adminAPI"] = "true"
            if i in self.noAdminAIP:
                bean_info["adminAPI"] = "false"
            # 假删
            if self.falseDelete:
                for attr in bean_info["attr"]:
                    if stringUtil.equal_str_tail_not_case(attr["filed"], self.falseDeleteFlag):
                        bean_info["falseDelete"] = attr["filed"]
            # 保存至类中
            self.tables[i] = bean_info

    def mapping_relations(self):
        unknown_to_unknown = {}
        ont_to_many = {}
        ont_to_one = {}
        many_to_many = {}

        # 扫描表信息，开启关系擦或者
        if self.multiTable:
            for i in self.tables:
                key = self.tables[i].get("key").get("filed")
                # 标准id起名补全，和非id起名
                if key == "id":
                    if self.underscoreReplace:
                        key = f'{self.tables[i].get("tableName")}_{key}'
                    else:
                        key = f'{self.tables[i].get("tableName")}{key}'
                for j in self.tables:
                    bean_info = self.tables[j]
                    for attr in bean_info.get("attr"):
                        # 如果是主键在其他表中的字段出现，则键入待分类的关系中
                        if stringUtil.equal_str_tail_not_case(attr.get("filed"), key):
                            mapper_dict_set(unknown_to_unknown, f"{i}.{key}",
                                            f"{bean_info.get('tableName')}.{attr.get('filed')}")
        # 以上为自动扫描区
        # 转义配置中的一对一
        for i in self.oneToOne:
            mapper_dict_set(ont_to_one, i.split("->")[0], i.split("->")[1])
            mapper_dict_set(ont_to_one, i.split("->")[1], i.split("->")[0])
        # 转义配置中的一对多
        for i in self.oneToMany:
            mapper_dict_set(ont_to_many, i.split("->")[0], i.split("->")[1])
        # 以上为配置文件装配
        # 如果在一对一中一配置，则去除查找到的
        for i in ont_to_one:
            for j in ont_to_one[i]:
                if unknown_to_unknown.get(i) and j in unknown_to_unknown.get(i):
                    unknown_to_unknown[i].remove(j)
        # 添加查找到的至一对多
        for i in unknown_to_unknown:
            for j in unknown_to_unknown[i]:
                mapper_dict_set(ont_to_many, i, j)
                # 反向添加一对一
                mapper_dict_set(ont_to_one, j, i)
        # 装配至配置中
        # 根据列表中的关系描述，查找属性并封装，如果修改查找决策在上面修改
        # 下面代码仅仅是解析a.key=b.a_key的
        old_tables = copy.deepcopy(self.tables)
        for i in ont_to_one:
            k = i.split(".")[0]
            for j in ont_to_one[i]:
                v = j.split(".")[0]
                bean_info = self.tables.get(k)
                if bean_info.get("oneToOne") is None:
                    bean_info["oneToOne"] = []
                obj = old_tables.get(v).copy()
                obj["foreign_key"] = i.split(".")[1]
                bean_info["oneToOne"].append(obj)
        for i in ont_to_many:
            k = i.split(".")[0]
            for j in ont_to_many[i]:
                v = j.split(".")[0]
                bean_info = self.tables.get(k)
                if bean_info.get("oneToMany") is None:
                    bean_info["oneToMany"] = []
                obj = old_tables.get(v).copy()
                obj["foreign_key"] = j.split(".")[1]
                bean_info["oneToMany"].append(obj)
        # 多对多关系映射处理
        # 判断标准，在中间表存在两个以上一对一，即当作中间表
        for table in self.tables:
            obj = self.tables[table]
            if "oneToOne" in obj and len(obj["oneToOne"]) > 1:
                for i in obj["oneToOne"]:
                    for j in obj["oneToOne"]:
                        if i["tableName"] != j["tableName"]:
                            # Id补全
                            i_table = self.tables[i["tableName"]]
                            j_table = self.tables[j["tableName"]]
                            key = i_table.get("key").get("filed")
                            if key == "id":
                                if self.underscoreReplace:
                                    key = f'{i_table.get("tableName")}_{key}'
                                else:
                                    key = f'{i_table.get("tableName")}{key}'
                            continue_flag = False
                            for attr in j_table.get("attr"):
                                # 如果i主键在j表中的字段出现，则键无法构成多对多关系
                                if stringUtil.equal_str_tail_not_case(attr.get("filed"), key):
                                    continue_flag = True
                                    break
                            if continue_flag:
                                continue
                            key = j_table.get("key").get("filed")
                            if key == "id":
                                if self.underscoreReplace:
                                    key = f'{j_table.get("tableName")}_{key}'
                                else:
                                    key = f'{j_table.get("tableName")}{key}'
                            for attr in i_table.get("attr"):
                                # 如果j主键在i表中的字段出现，则键无法构成多对多关系
                                if stringUtil.equal_str_tail_not_case(attr.get("filed"), key):
                                    continue_flag = True
                                    break
                            if continue_flag:
                                continue
                            # print(f'{i["tableName"]} \t\t-> {table} <-\t\t {j["tableName"]}')
                            bean_info = self.tables.get(i["tableName"])
                            if bean_info.get("manyToMany") is None:
                                bean_info["manyToMany"] = []
                            to_obj = copy.deepcopy(old_tables.get(table))
                            to_obj["foreign_key"] = i["foreign_key"]
                            bean_info["manyToMany"].append(
                                {"to": to_obj, "many": copy.deepcopy(j)})

    def save_model_json(self):
        path = os.path.join(os.getcwd(), "config")
        if not os.path.exists(path):
            os.mkdir(path)
        if self.table:
            if isinstance(self.table, str) and self.table in self.tables:
                with open(os.path.join(path, f"{self.table}.json"), "w", encoding="utf-8") as file:
                    file.write(json.dumps(self.tables[self.table], indent=2))
                print(f"{self.table}.json已保存")
            elif isinstance(self.table, list):
                for i in self.table:
                    if i in self.tables:
                        with open(os.path.join(path, f"{i}.json"), "w", encoding="utf-8") as file:
                            file.write(json.dumps(self.tables[i], indent=2))
                        print(f"{i}.json已保存")
                    else:
                        print(f"{i}没有找到")
            else:
                print(f"table参数存在问题，type:{type(self.table)},value:{self.table}")
        else:
            for i in self.tables:
                with open(os.path.join(path, f"{i}.json"), "w", encoding="utf-8") as file:
                    file.write(json.dumps(self.tables[i], indent=2))
                print(f"{i}.json已保存")
