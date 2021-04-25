from src.util import stringUtil


def create_java_mapper(config: dict):
    data = f'package {config["extradimensionalData"]["path_java_mapper"]};\n\n'
    data += "import java.util.List;\n"
    data += f'import {config["path_util"]}.Page;\n'
    data += f'import org.apache.ibatis.annotations.Mapper;\n'
    data += "import org.apache.ibatis.annotations.Param;\n"
    data += f'import {config["path_pojo"]}.{config["className"]};\n'

    data += f'import {config["path_java_mapper"]}.{config["javaMapperName"]};\n'

    method_str = __create_method(config)

    data += f'\n@Mapper\n'
    data += f'public interface {config["extradimensionalData"]["javaMapperName"]} extends {config["javaMapperName"]} {{\n\n{method_str}\n}}'
    return data


def __create_method(config: dict):
    # SQL注入项
    temp_sql = ""
    if config.get("SQLInjection") == "true":
        temp_sql = ' ,@Param("SQLInjection") String SQLInjection'
    tag = "\t"
    # 添加
    method_str = f''
    key_word_str = ""
    select_low_param_class_name = f'@Param("{stringUtil.low_str_first(config["className"])}") '
    if config.get("fuzzySearch") == "true" and "keyWordList" in config and len(config["keyWordList"]) > 0:
        key_word_name = config.get("keyWord")
        if key_word_name is not None:
            key_word_name = key_word_name.strip()
        else:
            key_word_name = "keyWord"
        if key_word_name == "":
            key_word_name = "keyWord"
        key_word_str = f', @Param("{key_word_name}") String {key_word_name}'
    # 普通查
    method_str += f'{tag}public List<{config["extradimensionalData"]["className"]}> select{config["extradimensionalData"]["className"]}({select_low_param_class_name}{config["className"]} {stringUtil.low_str_first(config["className"])}{key_word_str}, @Param("page") Page page{temp_sql});\n\n'
    # 普通计数

    return method_str
