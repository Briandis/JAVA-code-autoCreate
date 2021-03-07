from src.util import stringUtil


def create_service(config: dict):
    tag = "\t"
    # 打开包
    data = f'package {config["path_service"]};\n\n'
    # 导包区
    data += 'import java.util.List;\n'
    data += f'import {config["path_util"]}.Page;\n'
    data += "\n"
    method_str = ""

    temp_str = ""
    if config.get("fuzzySearch") == "true" and "keyWordList" in config and len(config["keyWordList"]) > 0:
        key_word_name = config.get("keyWord")
        if key_word_name is not None:
            key_word_name = key_word_name.strip()
        else:
            key_word_name = "keyWord"
        if key_word_name == "":
            key_word_name = "keyWord"
        temp_str = f', String {key_word_name}'

    if config.get("userAPI") == "true":
        # 添加方法
        method_str += f'{tag}public boolean add{config["className"]}({config["className"]} {stringUtil.low_str_first(config["className"])});\n\n'
        # 删除方法主键
        method_str += f'{tag}public boolean delete{config["className"]}By{stringUtil.upper_str_first(config["key"]["attr"])}({config["key"]["type"]} {config["key"]["attr"]});\n\n'
        # 更新
        method_str += f'{tag}public boolean update{config["className"]}({config["className"]} {stringUtil.low_str_first(config["className"])});\n\n'
        # 单个查询
        method_str += f'{tag}public {config["className"]} select{config["className"]}By{stringUtil.upper_str_first(config["key"]["attr"])}({config["key"]["type"]} {config["key"]["attr"]});\n\n'
        # 多个查询
        method_str += f'{tag}public List<{config["className"]}> select{config["className"]}({config["className"]} {stringUtil.low_str_first(config["className"])}{temp_str}, Page page);\n\n'
    if config.get("adminAPI") == "true":
        # 后台添加方法
        method_str += f'{tag}public boolean adminAdd{config["className"]}({config["className"]} {stringUtil.low_str_first(config["className"])});\n\n'
        # 后台删除方法主键
        method_str += f'{tag}public boolean adminDelete{config["className"]}By{stringUtil.upper_str_first(config["key"]["attr"])}({config["key"]["type"]} {config["key"]["attr"]});\n\n'
        # 后台更新
        method_str += f'{tag}public boolean adminUpdate{config["className"]}({config["className"]} {stringUtil.low_str_first(config["className"])});\n\n'
        # 后台单个查询
        method_str += f'{tag}public {config["className"]} adminSelect{config["className"]}By{stringUtil.upper_str_first(config["key"]["attr"])}({config["key"]["type"]} {config["key"]["attr"]});\n\n'
        # 后台多个查询
        method_str += f'{tag}public List<{config["className"]}> adminSelect{config["className"]}({config["className"]} {stringUtil.low_str_first(config["className"])}{temp_str}, Page page);\n\n'

    data += f'public interface {config["serviceName"]} {{\n{method_str}}}'
    return data
