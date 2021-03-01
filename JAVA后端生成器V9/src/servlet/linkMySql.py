import os
import shutil
import traceback

from src.analysis.analysis import DataBase, Attribute, SQLLinkUtil
from src.generate.generateAnalysis import Generate
from src.httpServer.server import Servlet, Request, Response
from src.util import mysqlUtil, stringUtil
import json


class LinkMySqlServlet(Servlet):

    def servlet(self, request: Request, response: Response):
        def get_attribute_object(obj: Attribute, attr_name: str) -> dict:
            return {"filed": obj.Field, "type": stringUtil.get_java_type(obj.Type)}

        host = request.get_param("host")
        name = request.get_param("name")
        password = request.get_param("password")
        port = request.get_param("port")
        database = request.get_param("database")
        port = int(port)
        try:
            mysql = mysqlUtil.MySql(database, host=host, name=name, password=password, port=port)
            sql = "show full tables where Table_Type = 'BASE TABLE';"
            tables = mysql.execute_select(sql, DataBase)
            print(f"查询到表数量：{len(tables)}")
            temp = []
            for i in tables:
                temp.append(getattr(i, f'Tables_in_{database}'))
            tables = temp
            res_table = []
            for i in tables:
                sql = f"desc {i}"
                attrs = mysql.execute_select(sql, Attribute)
                bean_info = dict()
                bean_info["tableName"] = i
                bean_info["attr"] = []
                for j in attrs:
                    attr_name = j.Field
                    if j.Key == "PRI":
                        bean_info["key"] = get_attribute_object(j, attr_name)
                    else:
                        bean_info["attr"].append(get_attribute_object(j, attr_name))
                res_table.append(bean_info)
            mysql.close()
            response.write_body(json.dumps({"code": 200, "data": res_table}))
        except:
            response.write_body('{"code":"-1"}')


class CreateConfigServlet(Servlet):
    def servlet(self, request: Request, response: Response):
        data = request.get_param("data")
        try:
            with open("config.json", "w", encoding="utf-8") as file:
                file.write(data)
            response.write_body(json.dumps({"code": 200}))
        except:
            response.write_body(json.dumps({"code": -1, "msg": "配置文件错误"}))


class CreateOneServlet(Servlet):
    def servlet(self, request: Request, response: Response):
        if os.path.exists(os.path.join(os.getcwd(), "config.json")):
            try:
                data = json.load(open("config.json", encoding="utf-8"))
                analysis = SQLLinkUtil(data)
                analysis.get_all_table()
                analysis.mapping_relations()
                analysis.save_model_json()
            except:
                response.write_body(json.dumps({"code": -1, "msg": "配置文件生成错误"}))
                return
            try:
                g = Generate()
                g.generate()
            except Exception:
                response.write_body(json.dumps({"code": -1, "msg": "代码生成错误"}))
            response.write_body(json.dumps({"code": 200}))
        else:
            response.write_body(json.dumps({"code": -1, "msg": "配置文件不存在"}))


class CreateTowServlet(Servlet):
    def servlet(self, request: Request, response: Response):
        if os.path.exists(os.path.join(os.getcwd(), "config")):
            try:
                data = json.load(open("config.json", encoding="utf-8"))
                analysis = SQLLinkUtil(data)
                analysis.get_all_table()
                analysis.mapping_relations()
                analysis.save_model_json()
                response.write_body(json.dumps({"code": 200}))
            except:
                response.write_body(json.dumps({"code": -1, "msg": "配置文件生成错误"}))
        else:
            response.write_body(json.dumps({"code": -1, "msg": "配置文件不存在"}))


class CreateThreeServlet(Servlet):
    def servlet(self, request: Request, response: Response):
        try:
            g = Generate()
            g.generate()
            response.write_body(json.dumps({"code": 200}))
        except:
            response.write_body(json.dumps({"code": -1, "msg": "代码生成依赖的config目录错误"}))


class GetInfoServlet(Servlet):
    def servlet(self, request: Request, response: Response):
        path = os.path.join(os.getcwd(), "config.json")
        a = os.path.exists(path)
        path = os.path.join(os.getcwd(), "config")
        b = os.path.exists(path)
        path = os.path.join(os.getcwd(), "data")
        c = os.path.exists(path)
        response.write_body(json.dumps({"code": 200, "data": {"a": a, "b": b, "c": c}}))


def del_file(filepath):
    del_list = os.listdir(filepath)
    for f in del_list:
        file_path = os.path.join(filepath, f)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)


class RemoveConfigServlet(Servlet):
    def servlet(self, request: Request, response: Response):
        path = os.path.join(os.getcwd(), "config")
        del_file(path)
        os.removedirs(path)
        response.write_body(json.dumps({"code": 200}))


class RemoveDataServlet(Servlet):
    def servlet(self, request: Request, response: Response):
        path = os.path.join(os.getcwd(), "data")
        del_file(path)
        os.removedirs(path)
        response.write_body(json.dumps({"code": 200}))
