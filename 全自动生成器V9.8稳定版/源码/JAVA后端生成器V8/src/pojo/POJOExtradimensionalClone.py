from src.util import stringUtil


# 创建POJO的文件
def create_pojo(config: dict) -> str:
    tag = "\t"
    # 打开本包并换行
    data = f'package {config["extradimensionalData"]["path_pojo"]};\n\n'
    # 导包区域
    data += f'import java.util.ArrayList;\n'
    data += f'import com.alibaba.fastjson.JSON;\n'
    data += f'import java.util.List;\n'
    data += f'import {config["path_pojo"]}.{config["className"]};\n'
    # 装配类型和属性名称
    attrs = [config["extradimensionalData"]["key"]]
    for attr in config["extradimensionalData"]["attr"]:
        attrs.append(attr)

    # 封装私有属性字符串
    attr_str = ""
    date_flag = False
    for attr in attrs:
        attr_str += f'{tag}private {attr["type"]} {attr["attr"]};\n'
        if attr["type"] == "Date":
            date_flag = True
    attr_str += "\n"
    if date_flag:
        data += f'import java.util.Date;\n'

    # 封装get/set方法
    method_str = ""
    for attr in attrs:
        temp = f'{tag * 2}return {attr["attr"]};\n'
        method_str += f'{tag}public {attr["type"]} get{stringUtil.upper_str_first(attr["attr"])}() {{\n{temp}\t}}\n\n'
        temp = f'{tag * 2}this.{attr["attr"]} = {attr["attr"]};\n'
        temp += f'{tag * 2}return this;\n'
        method_str += f'{tag}public {config["extradimensionalData"]["className"]} set{stringUtil.upper_str_first(attr["attr"])}({attr["type"]} {attr["attr"]}) {{\n{temp}\t}}\n\n'
    # 封装toString方法
    temp = f'{tag * 2}return JSON.toJSONString(this);\n'
    method_str += f'{tag}@Override\n'
    method_str += f'{tag}public String toString() {{\n{temp}\t}}'

    temp = f'{tag * 2}if ({config["extradimensionalData"]["key"]["attr"]} == null) {{\n{tag * 3}throw new NullPointerException();\n{tag * 2}}}\n{tag * 2}this.{config["extradimensionalData"]["key"]["attr"]} = {config["extradimensionalData"]["key"]["attr"]};\n'
    construction_method = f'{tag}public {config["extradimensionalData"]["className"]}() {{\n{tag}}}\n\n'
    construction_method += f'{tag}public {config["extradimensionalData"]["className"]}({config["extradimensionalData"]["key"]["type"]} {config["extradimensionalData"]["key"]["attr"]}) {{\n{temp}{tag}}}\n\n'
    temp = f''
    for attr in config["extradimensionalData"]["attr"]:
        if attr.get("inAttr") != None and attr.get("inAttr") != "null":
            temp += f'{tag * 3}{attr["attr"]} = {stringUtil.low_str_first(config["className"])}.get{stringUtil.upper_str_first(attr["inAttr"])}();\n'
    temp += f'{tag * 3}{config["extradimensionalData"]["key"]["attr"]} = {stringUtil.low_str_first(config["className"])}.get{stringUtil.upper_str_first(config["extradimensionalData"]["key"]["inAttr"])}();\n'
    construction_method += f'{tag}public {config["extradimensionalData"]["className"]}({config["className"]} {stringUtil.low_str_first(config["className"])}) {{\n{tag * 2}if ({stringUtil.low_str_first(config["className"])} != null) {{\n{temp}{tag * 2}}}\n{tag}}}\n\n'

    temp = f'{tag * 2}{config["className"]} {stringUtil.low_str_first(config["className"])} = new {config["className"]}();\n'
    for attr in config["extradimensionalData"]["attr"]:
        if attr.get("inAttr") != None and attr.get("inAttr") != "null":
            temp += f'{tag * 2}{stringUtil.low_str_first(config["className"])}.set{stringUtil.upper_str_first(attr["inAttr"])}({attr["attr"]});\n'
    temp += f'{tag * 2}{stringUtil.low_str_first(config["className"])}.set{stringUtil.upper_str_first(config["extradimensionalData"]["key"]["inAttr"])}({config["extradimensionalData"]["key"]["attr"]});\n'
    temp += f'{tag * 2}return {stringUtil.low_str_first(config["className"])};\n'
    construction_method += f'{tag}public {config["className"]} to{config["className"]}() {{\n{temp}{tag}}}\n\n'

    temp = f'{tag * 2}if (lists == null) {{\n{tag * 3}return null;\n{tag * 2}}}\n'
    temp += f'{tag * 2}List<{config["extradimensionalData"]["className"]}> list = new ArrayList<{config["extradimensionalData"]["className"]}>();\n'
    temp += f'{tag * 2}for ({config["className"]} {stringUtil.low_str_first(config["className"])} : lists) {{\n{tag * 3}list.add(new {config["extradimensionalData"]["className"]}({stringUtil.low_str_first(config["className"])}));\n{tag * 2}}}\n'
    temp += f'{tag * 2}return list;\n'
    construction_method += f'{tag}public static List<{config["extradimensionalData"]["className"]}> toList(List<{config["className"]}> lists) {{\n{temp}{tag}}}\n\n'

    data += '\n'
    data += f'public class {config["extradimensionalData"]["className"]} {{\n{attr_str}{construction_method}{method_str}\n}}'
    return data
