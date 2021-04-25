import json
import os
from src.pojo import pojoAutoCreate
from src.pojo import pojoCreate
from src.service import serviceCreate
from src.controller import controllerCreate
from src.service import serviceImplCreate
from src.mapper import JAVAAutoMapperCreate, XMLMapperCreate, JAVAMapperCreate
from src.mapper import XMLAutoMapperCreate


def is_not_dir_create(path, dir):
    path = os.path.join(path, dir)
    if not os.path.exists(path):
        os.mkdir(path)
    return path


def create_dir(packet_name: str) -> str:
    lists = packet_name.split(".")
    path = os.getcwd()

    path = is_not_dir_create(path, "data")
    path = is_not_dir_create(path, "src")
    for i in lists:
        path = os.path.join(path, i)
        if not os.path.exists(path):
            os.mkdir(path)
    return path


def save_file(path, file_name, suffix, data):
    path = create_dir(path)
    if "." not in suffix:
        suffix = "." + suffix
    with open(os.path.join(path, file_name + suffix), "w") as file:
        file.write(data)


class Generate:

    def __init__(self):
        path = "config"
        path = os.path.join(os.getcwd(), path)
        if not os.path.exists(path):
            raise FileNotFoundError("config文件夹不存在！！！！")
        list_file = os.listdir(path)
        self.data = []
        for file in list_file:
            if ".json" in file:
                print(f"发现{file}")
                self.data.append(json.load(open(os.path.join(path, file))))
        print(f"总共{len(self.data)}个文件")

    def generate(self):
        print("开始准备解析")
        for i in self.data:
            self.__parsing(i)

    def __parsing(self, data: dict):
        create_file = ["controller", "service", "serviceImpl", "JAVAMapper", "XMLMapper", "POJO", "POJOAuto",
                       "JAVAAutoMapper", "XMLAutoMapper"]
        if "createFile" in data and isinstance(data["createFile"], list) and len(data["createFile"]) > 0:
            create_file = data["createFile"]
        for i in range(len(create_file)):
            create_file[i] = create_file[i].lower()
        not_create_file = []
        if "notCreateFile" in data and isinstance(data["notCreateFile"], list) and len(data["notCreateFile"]) > 0:
            not_create_file = data["notCreateFile"]
        create_file = set(create_file)
        # 生成实体类文件
        if "pojo".lower() in create_file and "pojo".lower() not in not_create_file:
            string = pojoCreate.create_pojo(data)
            save_file(data["path_pojo"], data["className"], "java", string)

        # 生成自动生成实体类文件
        if "POJOAuto".lower() in create_file and "POJOAuto".lower() not in not_create_file:
            string = pojoAutoCreate.create_pojo(data)
            save_file(data["path_pojo"], f'{data["className"]}Auto', "java", string)

        # 生成service接口件
        if "service".lower() in create_file and "service".lower() not in not_create_file:
            string = serviceCreate.create_service(data)
            # print(string)
            save_file(data["path_service"], data["serviceName"], "java", string)

        # 生成serviceImpl实现类文件
        if "serviceImpl".lower() in create_file and "serviceImpl".lower() not in not_create_file:
            string = serviceImplCreate.create_service_impl(data)
            # print(string)
            save_file(data["path_service_impl"], data["serviceImplName"], "java", string)

        # 生成Controller文件
        if "controller".lower() in create_file and "controller".lower() not in not_create_file:
            string = controllerCreate.create(data)
            # print(string)
            save_file(data["path_controller"], data["controllerName"], "java", string)

        # 生成mapper.java文件
        if "JAVAMapper".lower() in create_file and "JAVAMapper".lower() not in not_create_file:
            string = JAVAMapperCreate.create_java_mapper(data)
            save_file(data["path_java_mapper"], data["javaMapperName"], "java", string)

        # 生成自动生成的mapper.java文件
        if "JAVAAutoMapper".lower() in create_file and "JAVAAutoMapper".lower() not in not_create_file:
            string = JAVAAutoMapperCreate.create_java_mapper(data)
            save_file(data["path_java_mapper"], data["javaAutoMapperName"], "java", string)

        # 生成Mapper.xml文件
        if "XMLMapper".lower() in create_file and "XMLMapper".lower() not in not_create_file:
            string = XMLMapperCreate.create_xml_mapper(data)
            save_file(data["path_xml_mapper"], data["XMLMapperName"], "xml", string)

        # 生成自动生成的XML文件
        if "XMLAutoMapper".lower() in create_file and "XMLAutoMapper".lower() not in not_create_file:
            string = XMLAutoMapperCreate.create_xml_mapper(data)
            save_file(data["path_xml_mapper"], data["XMLAutoMapperName"], "xml", string)
