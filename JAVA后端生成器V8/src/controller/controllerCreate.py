from src.util import stringUtil
import re


def create(config: dict):
    # 开包
    data = f'package {config["path_controller"]};\n\n'
    # 导包
    data += f'import {config["path_util"]}.Page;\n'
    data += f'import {config["path_util"]}.JsonUtil;\n'
    data += "import org.springframework.beans.factory.annotation.Autowired;\n"
    data += "import org.springframework.beans.factory.annotation.Qualifier;\n"
    data += "import org.springframework.stereotype.Controller;\n"
    data += "import org.springframework.web.bind.annotation.RequestMapping;\n"
    data += "import org.springframework.web.bind.annotation.ResponseBody;\n"
    # restful风格下依赖
    if config.get("restful") == "true":
        data += "import org.springframework.web.bind.annotation.RequestMethod;\n"
    data += "\n"
    # 采用以封装好的工具包
    data += f'import {config["path_pojo"]}.{config["className"]};\n'
    data += f'import {config["path_service"]}.{config["serviceName"]};\n'
    data += "\n"
    data += '@Controller\n'
    data += f'@RequestMapping(value = "/{stringUtil.low_str_first(config["className"])}", produces = "text/html;charset=utf-8")\n'
    data += f'public class {config["controllerName"]} {{\n\n{__create_method(config)}}}'
    return data


def __create_method(config: dict):
    tag = "\t"
    data = f'{tag}@Autowired\n'
    data += f'{tag}@Qualifier("{stringUtil.low_str_first(config["serviceImplName"])}")\n'
    data += f'{tag}private {config["serviceName"]} {stringUtil.low_str_first(config["serviceName"])};\n'
    data += "\n"
    data += __method_add(config) + "\n"
    data += __method_admin_add(config) + "\n"
    data += __method_delete_by_id(config) + "\n"
    data += __method_admin_delete_by_id(config) + "\n"
    data += __method_update(config) + "\n"
    data += __method_admin_update(config) + "\n"
    data += __method_get_by_id(config) + "\n"
    data += __method_admin_get_by_id(config) + "\n"
    data += __method_get(config) + "\n"
    data += __method_admin_get(config) + "\n"
    return data


def __method_add(config: dict):
    tag = "\t"
    method_str = f'{tag * 2}boolean b = {stringUtil.low_str_first(config["serviceName"])}.add{config["className"]}({stringUtil.low_str_first(config["className"])});\n'
    method_str += f'{tag * 2}JsonUtil.put(b);\n'
    method_str += f'{tag * 2}return JsonUtil.toJSONString();\n'
    if config.get("restful") == "true":
        data = f'{tag}@RequestMapping(value = "/{stringUtil.low_str_first(config["className"])}", method = RequestMethod.POST)\n'
    else:
        data = f'{tag}@RequestMapping("/add{config["className"]}")\n'
    data += f'{tag}@ResponseBody\n'
    data += f'{tag}public String add{config["className"]}({config["className"]} {stringUtil.low_str_first(config["className"])}) {{\n{method_str}\t}}\n'
    return data


def __method_admin_add(config: dict):
    tag = "\t"
    method_str = f'{tag * 2}boolean b = {stringUtil.low_str_first(config["serviceName"])}.adminAdd{config["className"]}({stringUtil.low_str_first(config["className"])});\n'
    method_str += f'{tag * 2}JsonUtil.put(b);\n'
    method_str += f'{tag * 2}return JsonUtil.toJSONString();\n'
    if config.get("restful") == "true":
        data = f'{tag}@RequestMapping(value = "/admin/{stringUtil.low_str_first(config["className"])}", method = RequestMethod.POST)\n'
    else:
        data = f'{tag}@RequestMapping("/admin/add{config["className"]}")\n'
    data += f'{tag}@ResponseBody\n'
    data += f'{tag}public String adminAdd{config["className"]}({config["className"]} {stringUtil.low_str_first(config["className"])}) {{\n{method_str}\t}}\n'
    return data


def __method_delete_by_id(config: dict):
    tag = "\t"
    method_str_temp = f'{tag * 3}b = {stringUtil.low_str_first(config["serviceName"])}.delete{config["className"]}By{stringUtil.upper_str_first(config["key"]["attr"])}({config["key"]["attr"]});\n'
    method_str = f'{tag * 2}boolean b = false;\n'
    method_str += f'{tag * 2}if ({config["key"]["attr"]} != null) {{\n{method_str_temp}{tag * 2}}}\n'
    method_str += f'{tag * 2}JsonUtil.put(b);\n'
    method_str += f'{tag * 2}return JsonUtil.toJSONString();\n'
    if config.get("restful") == "true":
        data = f'{tag}@RequestMapping(value = "/{stringUtil.low_str_first(config["className"])}", method = RequestMethod.DELETE)\n'
    else:
        data = f'{tag}@RequestMapping("/delete{config["className"]}By{stringUtil.upper_str_first(config["key"]["attr"])}")\n'
    data += f'{tag}@ResponseBody\n'
    data += f'{tag}public String delete{config["className"]}By{stringUtil.upper_str_first(config["key"]["attr"])}({config["key"]["type"]} {config["key"]["attr"]}) {{\n{method_str}\t}}\n'
    return data


def __method_admin_delete_by_id(config: dict):
    tag = "\t"
    method_str_temp = f'{tag * 3}b = {stringUtil.low_str_first(config["serviceName"])}.adminDelete{config["className"]}By{stringUtil.upper_str_first(config["key"]["attr"])}({config["key"]["attr"]});\n'
    method_str = f'{tag * 2}boolean b = false;\n'
    method_str += f'{tag * 2}if ({config["key"]["attr"]} != null) {{\n{method_str_temp}{tag * 2}}}\n'
    method_str += f'{tag * 2}JsonUtil.put(b);\n'
    method_str += f'{tag * 2}return JsonUtil.toJSONString();\n'
    if config.get("restful") == "true":
        data = f'{tag}@RequestMapping(value = "/admin/{stringUtil.low_str_first(config["className"])}", method = RequestMethod.DELETE)\n'
    else:
        data = f'{tag}@RequestMapping("/admin/delete{config["className"]}By{stringUtil.upper_str_first(config["key"]["attr"])}")\n'
    data += f'{tag}@ResponseBody\n'
    data += f'{tag}public String adminDelete{config["className"]}By{stringUtil.upper_str_first(config["key"]["attr"])}({config["key"]["type"]} {config["key"]["attr"]}) {{\n{method_str}\t}}\n'
    return data


# 条件删除接口
# 不采用
# 条件删除中携带模糊删除
def __method_delete(config: dict):
    tag = "\t"
    # 函数参数
    key_word = ""
    # 传入参数
    key_attr = ""
    if config.get("fuzzySearch") == "true" and "keyWordList" in config and len(config["keyWordList"]) > 0:
        key_word_name = config.get("keyWord").strip()
        if key_word_name == "":
            key_word_name = "keyWord"
        key_word = f', String {key_word_name}'
        key_attr = f', {key_word_name}'
    method_str = f'{tag * 2}int index = {stringUtil.low_str_first(config["serviceName"])}.delete{config["className"]}({stringUtil.low_str_first(config["className"])}{key_attr}) ? 200 : -1;\n'
    method_str += f'{tag * 2}JsonUtil.put(index);\n'
    method_str += f'{tag * 2}return JsonUtil.toJSONString();\n'
    if config.get("restful") == "true":
        data = f'{tag}@RequestMapping(value = "/many{config["className"]}", method = RequestMethod.DELETE)\n'
    else:
        data = f'{tag}@RequestMapping("/delete{config["className"]}")\n'
    data += f'{tag}@ResponseBody\n'
    data += f'{tag}public String delete{config["className"]}({config["className"]} {stringUtil.low_str_first(config["className"])}{key_word}) {{\n{method_str}\t}}\n'
    return data


def __method_update(config: dict):
    tag = "\t"
    method_str_temp = f'{tag * 3}b = {stringUtil.low_str_first(config["serviceName"])}.update{config["className"]}({stringUtil.low_str_first(config["className"])});\n'
    method_str = f'{tag * 2}boolean b = false;\n'
    method_str += f'{tag * 2}if ({stringUtil.low_str_first(config["className"])}.get{stringUtil.upper_str_first(config["key"]["attr"])}() != null) {{\n{method_str_temp}{tag * 2}}}\n'
    method_str += f'{tag * 2}JsonUtil.put(b);\n'
    method_str += f'{tag * 2}return JsonUtil.toJSONString();\n'
    if config.get("restful") == "true":
        data = f'{tag}@RequestMapping(value = "/{stringUtil.low_str_first(config["className"])}", method = RequestMethod.PUT)\n'
    else:
        data = f'{tag}@RequestMapping("/update{config["className"]}")\n'
    data += f'{tag}@ResponseBody\n'
    data += f'{tag}public String update{config["className"]}({config["className"]} {stringUtil.low_str_first(config["className"])}) {{\n{method_str}\t}}\n'
    return data


def __method_admin_update(config: dict):
    tag = "\t"
    method_str_temp = f'{tag * 3}b = {stringUtil.low_str_first(config["serviceName"])}.adminUpdate{config["className"]}({stringUtil.low_str_first(config["className"])});\n'
    method_str = f'{tag * 2}boolean b = false;\n'
    method_str += f'{tag * 2}if ({stringUtil.low_str_first(config["className"])}.get{stringUtil.upper_str_first(config["key"]["attr"])}() != null) {{\n{method_str_temp}{tag * 2}}}\n'
    method_str += f'{tag * 2}JsonUtil.put(b);\n'
    method_str += f'{tag * 2}return JsonUtil.toJSONString();\n'
    if config.get("restful") == "true":
        data = f'{tag}@RequestMapping(value = "/admin/{stringUtil.low_str_first(config["className"])}", method = RequestMethod.PUT)\n'
    else:
        data = f'{tag}@RequestMapping("/admin/update{config["className"]}")\n'
    data += f'{tag}@ResponseBody\n'
    data += f'{tag}public String adminUpdate{config["className"]}({config["className"]} {stringUtil.low_str_first(config["className"])}) {{\n{method_str}\t}}\n'
    return data


def __method_get_by_id(config: dict):
    tag = "\t"
    method_str = f'{tag * 2}JsonUtil.put({stringUtil.low_str_first(config["serviceName"])}.select{config["className"]}By{stringUtil.upper_str_first(config["key"]["attr"])}({config["key"]["attr"]}));\n'
    method_str += f'{tag * 2}return JsonUtil.toJSONString();\n'
    if config.get("restful") == "true":
        data = f'{tag}@RequestMapping(value = "/{stringUtil.low_str_first(config["className"])}", method = RequestMethod.GET)\n'
    else:
        data = f'{tag}@RequestMapping("/get{config["className"]}By{stringUtil.upper_str_first(config["key"]["attr"])}")\n'
    data += f'{tag}@ResponseBody\n'
    data += f'{tag}public String get{config["className"]}By{stringUtil.upper_str_first(config["key"]["attr"])}({config["key"]["type"]} {config["key"]["attr"]}) {{\n{method_str}\t}}\n'
    return data


def __method_admin_get_by_id(config: dict):
    tag = "\t"
    method_str = f'{tag * 2}JsonUtil.put({stringUtil.low_str_first(config["serviceName"])}.adminSelect{config["className"]}By{stringUtil.upper_str_first(config["key"]["attr"])}({config["key"]["attr"]}));\n'
    method_str += f'{tag * 2}return JsonUtil.toJSONString();\n'
    if config.get("restful") == "true":
        data = f'{tag}@RequestMapping(value = "/admin/{stringUtil.low_str_first(config["className"])}", method = RequestMethod.GET)\n'
    else:
        data = f'{tag}@RequestMapping("/admin/get{config["className"]}By{stringUtil.upper_str_first(config["key"]["attr"])}")\n'
    data += f'{tag}@ResponseBody\n'
    data += f'{tag}public String adminGet{config["className"]}By{stringUtil.upper_str_first(config["key"]["attr"])}({config["key"]["type"]} {config["key"]["attr"]}) {{\n{method_str}\t}}\n'
    return data


def __method_get(config: dict):
    tag = "\t"
    # 函数参数
    key_word = ""
    # 传入参数
    key_attr = ""
    # 相关代码块
    key_str = ""
    if config.get("fuzzySearch") == "true" and "keyWordList" in config and len(config["keyWordList"]) > 0:
        key_word_name = config.get("keyWord").strip()
        if key_word_name == "":
            key_word_name = "keyWord"
        key_word = f', String {key_word_name}'
        key_attr = f", {key_word_name}"
        # 去除首位空格
        temp = f'{tag * 3}{key_word_name} = {key_word_name}.trim();\n'
        # 判断是否为空
        temp += f'{tag * 3}{key_word_name} = {key_word_name}.equals("") ? null : {key_word_name};\n'
        key_str = f'{tag * 2}if({key_word_name} != null){{\n{temp}{tag * 2}}}\n'
    # 加入模糊搜索的判断
    method_str = key_str
    method_str += f'{tag * 2}JsonUtil.put({stringUtil.low_str_first(config["serviceName"])}.select{config["className"]}({stringUtil.low_str_first(config["className"])}{key_attr}, page));\n'
    method_str += f'{tag * 2}JsonUtil.put("page", page);\n'
    method_str += f'{tag * 2}return JsonUtil.toJSONString();\n'

    if config.get("restful") == "true":
        data = f'{tag}@RequestMapping(value = "/many{config["className"]}", method = RequestMethod.GET)\n'
    else:
        data = f'{tag}@RequestMapping("/get{config["className"]}")\n'
    data += f'{tag}@ResponseBody\n'
    data += f'{tag}public String get{config["className"]}({config["className"]} {stringUtil.low_str_first(config["className"])}{key_word}, Page page) {{\n{method_str}\t}}\n'
    return data


def __method_admin_get(config: dict):
    tag = "\t"
    # 函数参数
    key_word = ""
    # 传入参数
    key_attr = ""
    # 相关代码块
    key_str = ""
    if config.get("fuzzySearch") == "true" and "keyWordList" in config and len(config["keyWordList"]) > 0:
        key_word_name = config.get("keyWord").strip()
        if key_word_name == "":
            key_word_name = "keyWord"
        key_word = f', String {key_word_name}'
        key_attr = f", {key_word_name}"
        # 去除首位空格
        temp = f'{tag * 3}{key_word_name} = {key_word_name}.trim();\n'
        # 判断是否为空
        temp += f'{tag * 3}{key_word_name} = {key_word_name}.equals("") ? null : {key_word_name};\n'
        key_str = f'{tag * 2}if({key_word_name} != null){{\n{temp}{tag * 2}}}\n'
    # 加入模糊搜索的判断
    method_str = key_str
    method_str += f'{tag * 2}JsonUtil.put({stringUtil.low_str_first(config["serviceName"])}.adminSelect{config["className"]}({stringUtil.low_str_first(config["className"])}{key_attr}, page));\n'
    method_str += f'{tag * 2}JsonUtil.put("page", page);\n'
    method_str += f'{tag * 2}return JsonUtil.toJSONString();\n'

    if config.get("restful") == "true":
        data = f'{tag}@RequestMapping(value = "/admin/many{config["className"]}", method = RequestMethod.GET)\n'
    else:
        data = f'{tag}@RequestMapping("/admin/get{config["className"]}")\n'
    data += f'{tag}@ResponseBody\n'
    data += f'{tag}public String adminGet{config["className"]}({config["className"]} {stringUtil.low_str_first(config["className"])}{key_word}, Page page) {{\n{method_str}\t}}\n'
    return data
