from src.util import stringUtil


def create_service_impl(config: dict):
    data = f'package {config["path_service_impl"]};\n\n'
    # 导包区
    data += "import java.util.List;\n"
    data += f'import {config["path_util"]}.Page;\n'
    data += "import org.springframework.beans.factory.annotation.Autowired;\n"
    data += "import org.springframework.stereotype.Service;\n"
    if config["path_service_impl"] != config["path_java_mapper"]:
        data += f'import {config["path_java_mapper"]}.{config["javaMapperName"]};\n'

    data += "\n"
    data += '@Service\n'
    data += f'public class {config["serviceImplName"]} implements {config["serviceName"]} {{\n\n{__create_method_impl(config)}}}'
    return data


def __create_method_impl(config: dict):
    tag = "\t"
    data = f'{tag}@Autowired\n'
    data += f'{tag}private {config["javaMapperName"]} {stringUtil.low_str_first(config["javaMapperName"])};\n'
    data += "\n"
    if config.get("userAPI") == "true":
        data += __method_add(config)
        data += __method_delete_by_id(config)
        data += __method_update(config)
        data += __method_select_by_id(config)
        data += __method_select(config)
    if config.get("adminAPI") == "true":
        data += __method_admin_add(config)
        data += __method_admin_delete_by_id(config)
        data += __method_admin_update(config)
        data += __method_admin_select_by_id(config)
        data += __method_admin_select(config)
    return data


def __method_add(config: dict):
    tag = "\t"
    method_code = f'{tag * 2}return {stringUtil.low_str_first(config["javaMapperName"])}.insert{config["className"]}({stringUtil.low_str_first(config["className"])}) > 0;\n'
    method_str = f'{tag}@Override\n'
    method_str += f'{tag}public boolean add{config["className"]}({config["className"]} {stringUtil.low_str_first(config["className"])}) {{\n{method_code}{tag}}}\n\n'
    return method_str


def __method_admin_add(config: dict):
    tag = "\t"
    method_code = f'{tag * 2}return {stringUtil.low_str_first(config["javaMapperName"])}.insert{config["className"]}({stringUtil.low_str_first(config["className"])}) > 0;\n'
    method_str = f'{tag}@Override\n'
    method_str += f'{tag}public boolean adminAdd{config["className"]}({config["className"]} {stringUtil.low_str_first(config["className"])}) {{\n{method_code}{tag}}}\n\n'
    return method_str


def __method_delete_by_id(config: dict):
    tag = "\t"
    method_str = f'{tag}@Override\n'
    method_code = f'{tag * 2}return {stringUtil.low_str_first(config["javaMapperName"])}.delete{config["className"]}By{stringUtil.upper_str_first(config["key"]["attr"])}({config["key"]["attr"]}) > 0;\n'
    method_str += f'{tag}public boolean delete{config["className"]}By{stringUtil.upper_str_first(config["key"]["attr"])}({config["key"]["type"]} {config["key"]["attr"]}) {{\n{method_code}{tag}}}\n\n'
    return method_str


def __method_admin_delete_by_id(config: dict):
    tag = "\t"
    method_str = f'{tag}@Override\n'
    method_code = f'{tag * 2}return {stringUtil.low_str_first(config["javaMapperName"])}.delete{config["className"]}By{stringUtil.upper_str_first(config["key"]["attr"])}({config["key"]["attr"]}) > 0;\n'
    method_str += f'{tag}public boolean adminDelete{config["className"]}By{stringUtil.upper_str_first(config["key"]["attr"])}({config["key"]["type"]} {config["key"]["attr"]}) {{\n{method_code}{tag}}}\n\n'
    return method_str


def __method_update(config: dict):
    tag = "\t"
    method_str = f'{tag}@Override\n'
    method_code = f'{tag * 2}return {stringUtil.low_str_first(config["javaMapperName"])}.update{config["className"]}By{stringUtil.upper_str_first(config["key"]["attr"])}({stringUtil.low_str_first(config["className"])}) > 0;\n'
    method_str += f'{tag}public boolean update{config["className"]}({config["className"]} {stringUtil.low_str_first(config["className"])}) {{\n{method_code}{tag}}}\n\n'
    return method_str


def __method_admin_update(config: dict):
    tag = "\t"
    method_str = f'{tag}@Override\n'
    method_code = f'{tag * 2}return {stringUtil.low_str_first(config["javaMapperName"])}.update{config["className"]}By{stringUtil.upper_str_first(config["key"]["attr"])}({stringUtil.low_str_first(config["className"])}) > 0;\n'
    method_str += f'{tag}public boolean adminUpdate{config["className"]}({config["className"]} {stringUtil.low_str_first(config["className"])}) {{\n{method_code}{tag}}}\n\n'
    return method_str


def __method_select_by_id(config: dict):
    tag = "\t"
    method_str = f'{tag}@Override\n'
    method_code = f'{tag * 2}return {stringUtil.low_str_first(config["javaMapperName"])}.select{config["className"]}By{stringUtil.upper_str_first(config["key"]["attr"])}({config["key"]["attr"]});\n'
    method_str += f'{tag}public {config["className"]} select{config["className"]}By{stringUtil.upper_str_first(config["key"]["attr"])}({config["key"]["type"]} {config["key"]["attr"]}) {{\n{method_code}{tag}}}\n\n'
    return method_str


def __method_admin_select_by_id(config: dict):
    tag = "\t"
    method_str = f'{tag}@Override\n'
    method_code = f'{tag * 2}return {stringUtil.low_str_first(config["javaMapperName"])}.select{config["className"]}By{stringUtil.upper_str_first(config["key"]["attr"])}({config["key"]["attr"]});\n'
    method_str += f'{tag}public {config["className"]} adminSelect{config["className"]}By{stringUtil.upper_str_first(config["key"]["attr"])}({config["key"]["type"]} {config["key"]["attr"]}) {{\n{method_code}{tag}}}\n\n'
    return method_str


def __method_select(config: dict):
    tag = "\t"
    method_str = f'{tag}@Override\n'
    temp_sql = ""
    if config.get("SQLInjection") == "true":
        temp_sql = ", null"
    key_word, key_attr, key_str = "", "", ""
    if config.get("fuzzySearch") == "true" and "keyWordList" in config and len(config["keyWordList"]) > 0:
        key_word_name = config.get("keyWord")
        if key_word_name is not None:
            key_word_name = key_word_name.strip()
        else:
            key_word_name = "keyWord"
        if key_word_name == "":
            key_word_name = "keyWord"
        key_word = f', String {key_word_name}'
        key_attr = f", {key_word_name}"
        temp_str = f'{tag * 3}{key_word_name} = "%" + {key_word_name} + "%";\n'
        key_str += f'{tag * 2}if ({key_word_name} != null) {{\n{temp_str}{tag * 2}}}\n'
    method_code = key_str
    method_code += f'{tag * 2}if (page != null) {{\n{tag * 3}page.setMax({stringUtil.low_str_first(config["javaMapperName"])}.count{config["className"]}({stringUtil.low_str_first(config["className"])}{key_attr}));\n{tag * 2}}}\n'
    method_code += f'{tag * 2}return {stringUtil.low_str_first(config["javaMapperName"])}.select{config["className"]}({stringUtil.low_str_first(config["className"])}{key_attr}, page{temp_sql});\n'
    method_str += f'{tag}public List<{config["className"]}> select{config["className"]}({config["className"]} {stringUtil.low_str_first(config["className"])}{key_word}, Page page) {{\n{method_code}{tag}}}\n\n'
    return method_str


def __method_admin_select(config: dict):
    tag = "\t"
    method_str = f'{tag}@Override\n'
    temp_sql = ""
    if config.get("SQLInjection") == "true":
        temp_sql = ", null"
    key_word, key_attr, key_str = "", "", ""
    if config.get("fuzzySearch") == "true" and "keyWordList" in config and len(config["keyWordList"]) > 0:
        key_word_name = config.get("keyWord")
        if key_word_name is not None:
            key_word_name = key_word_name.strip()
        else:
            key_word_name = "keyWord"
        if key_word_name == "":
            key_word_name = "keyWord"
        key_word = f', String {key_word_name}'
        key_attr = f", {key_word_name}"
        temp_str = f'{tag * 3}{key_word_name} = "%" + {key_word_name} + "%";\n'
        key_str += f'{tag * 2}if ({key_word_name} != null) {{\n{temp_str}{tag * 2}}}\n'
    method_code = key_str
    method_code += f'{tag * 2}if (page != null) {{\n{tag * 3}page.setMax({stringUtil.low_str_first(config["javaMapperName"])}.count{config["className"]}({stringUtil.low_str_first(config["className"])}{key_attr}));\n{tag * 2}}}\n'
    method_code += f'{tag * 2}return {stringUtil.low_str_first(config["javaMapperName"])}.select{config["className"]}({stringUtil.low_str_first(config["className"])}{key_attr}, page{temp_sql});\n'
    method_str += f'{tag}public List<{config["className"]}> adminSelect{config["className"]}({config["className"]} {stringUtil.low_str_first(config["className"])}{key_word}, Page page) {{\n{method_code}{tag}}}\n\n'
    return method_str
