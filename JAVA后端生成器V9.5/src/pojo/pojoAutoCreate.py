from src.util import stringUtil


# 创建POJO的文件
def create_pojo(config: dict) -> str:
    tag = "\t"
    # 打开本包并换行
    data = f'package {config["path_pojo"]};\n\n'
    # 导包区域
    data += f'import com.alibaba.fastjson.JSON;\n'
    # 装配类型和属性名称
    attrs = [config["key"]]
    for attr in config["attr"]:
        attrs.append(attr)
    # 封装一对一关系
    if config.get("oneToOne"):
        for attr in config["oneToOne"]:
            attrs.append({"attr": stringUtil.low_str_first(attr["className"]), "type": attr["className"]})
            data += f'import {attr["path_pojo"]}.{attr["className"]};\n'
    # 封装一对多
    one_to_many_attr = set()
    list_flag = False
    if config.get("oneToMany"):
        for attr in config["oneToMany"]:
            attrs.append({"attr": "list" + attr["className"], "type": f'List<{attr["className"]}>'})
            data += f'import {attr["path_pojo"]}.{attr["className"]};\n'
            list_flag = True
            one_to_many_attr.add("list" + attr["className"])
        # 导list包

    if config.get("manyToMany"):
        for to_many in config["manyToMany"]:
            if "list" + to_many["many"]["className"] not in one_to_many_attr:
                one_to_many_attr.add("list" + to_many["many"]["className"])
                attrs.append(
                    {"attr": "list" + to_many["many"]["className"], "type": f'List<{to_many["many"]["className"]}>'}
                )
                data += f'import {to_many["many"]["path_pojo"]}.{to_many["many"]["className"]};\n'
                list_flag = True

    if list_flag:
        data += f'import java.util.List;\n'
    # 封装私有属性字符串
    attr_str = ""
    date_flag = False
    for attr in attrs:
        attr_str += f'{tag}private {attr["type"]} {attr["attr"]};\n'
        if attr["type"] == "Date":
            date_flag = True
    attr_str += "\n"

    # 如果存在日期类型，则导入日期
    if date_flag:
        data += f'import java.util.Date;\n'

    # 封装get/set方法
    method_str = ""
    for attr in attrs:
        temp = f'{tag * 2}return {attr["attr"]};\n'
        method_str += f'{tag}public {attr["type"]} get{stringUtil.upper_str_first(attr["attr"])}() {{\n{temp}\t}}\n\n'
        temp = f'{tag * 2}this.{attr["attr"]} = {attr["attr"]};\n'
        temp += f'{tag * 2}return (T) this;\n'
        method_str += f'{tag}public T set{stringUtil.upper_str_first(attr["attr"])}({attr["type"]} {attr["attr"]}) {{\n{temp}\t}}\n\n'
    # 封装toString方法
    temp = f'{tag * 2}return JSON.toJSONString(this);\n'
    method_str += f'{tag}@Override\n'
    method_str += f'{tag}public String toString() {{\n{temp}\t}}'

    data += '\n'
    data += '@SuppressWarnings("unchecked")\n'
    data += f'public abstract class {config["className"]}Auto<T> {{\n{attr_str}{method_str}\n}}'
    return data
