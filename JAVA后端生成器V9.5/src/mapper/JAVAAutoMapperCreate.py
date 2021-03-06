from src.util import stringUtil


# 创建Mapper.java


def create_java_mapper(config: dict):
    data = f'package {config["path_java_mapper"]};\n\n'
    data += "import java.util.List;\n"
    data += f'import {config["path_util"]}.Page;\n'
    data += f'import org.apache.ibatis.annotations.Mapper;\n'
    data += "import org.apache.ibatis.annotations.Param;\n"

    method_str, import_str = __create_method(config)
    data += import_str + '\n'
    data += f'@Mapper\n'
    data += f'public interface {config["javaAutoMapperName"]}{{\n{method_str}\n}}'
    return data


def __create_method(config: dict):
    # SQL注入项
    temp_sql = ""
    if config.get("SQLInjection") == "true":
        temp_sql = ' ,@Param("SQLInjection") String SQLInjection'
    tag = "\t"
    # 添加
    method_str = f'{tag}public Integer insert{config["className"]}({config["className"]} {stringUtil.low_str_first(config["className"])});\n\n'
    # 添加多个
    method_str += f'{tag}public Integer insert{config["className"]}List(@Param("list") List<{config["className"]}> list);\n\n'
    # 保存或更新，唯一索引方式
    method_str += f'{tag}public Integer saveOrUpdate{config["className"]}ByUnique({config["className"]} {stringUtil.low_str_first(config["className"])});\n\n'
    # 保存或更新条件式
    method_str += f'{tag}public Integer saveOrUpdate{config["className"]}ByWhere(@Param("save{config["className"]}") {config["className"]} save{config["className"]}, @Param("condition{config["className"]}") {config["className"]} condition{config["className"]});\n\n'
    # 仅条件插入
    method_str += f'{tag}public Integer insert{config["className"]}ByWhereOnlySave(@Param("save{config["className"]}") {config["className"]} save{config["className"]}, @Param("condition{config["className"]}") {config["className"]} condition{config["className"]});\n\n'
    # 主键删除
    method_str += f'{tag}public Integer delete{config["className"]}By{stringUtil.upper_str_first(config["key"]["attr"])}({config["key"]["type"]} {config["key"]["attr"]});\n\n'
    # 主键假删
    if "falseDelete" in config:
        method_str += f'{tag}public Integer falseDelete{config["className"]}By{stringUtil.upper_str_first(config["key"]["attr"])}({config["key"]["type"]} {config["key"]["attr"]});\n\n'
    # 搜索过滤
    key_word_str = ""
    low_param_class_name = ""
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
        low_param_class_name = f'@Param("{stringUtil.low_str_first(config["className"])}") '
    # 主键条件删
    method_str += f'{tag}public Integer delete{config["className"]}By{stringUtil.upper_str_first(config["key"]["attr"])}AndWhere(@Param("{config["key"]["attr"]}") {config["key"]["type"]} {config["key"]["attr"]}, @Param("{stringUtil.low_str_first(config["className"])}") {config["className"]} {stringUtil.low_str_first(config["className"])}{key_word_str});\n\n'
    # 条件删除
    method_str += f'{tag}public Integer delete{config["className"]}({low_param_class_name}{config["className"]} {stringUtil.low_str_first(config["className"])}{key_word_str});\n\n'

    # 一对一，一度多关系删除
    # 预留
    # 改
    method_str += f'{tag}public Integer update{config["className"]}By{stringUtil.upper_str_first(config["key"]["attr"])}({config["className"]} {stringUtil.low_str_first(config["className"])});\n\n'
    # 不重复条件改
    method_str += f'{tag}public Integer update{config["className"]}ByNotRepeatWhere(@Param("save{config["className"]}") {config["className"]} save{config["className"]}, @Param("condition{config["className"]}") {config["className"]} condition{config["className"]});\n\n'
    # 条件改
    method_str += f'{tag}public Integer update{config["className"]}(@Param("save{config["className"]}") {config["className"]} save{config["className"]}, @Param("condition{config["className"]}") {config["className"]} condition{config["className"]});\n\n'
    # 条件更新ID
    method_str += f'{tag}public Integer update{config["className"]}By{stringUtil.upper_str_first(config["key"]["attr"])}AndWhere(@Param("save{config["className"]}") {config["className"]} save{config["className"]}, @Param("condition{config["className"]}") {config["className"]} condition{config["className"]});\n\n'
    # 设置空字段
    method_str += f'{tag}public Integer update{config["className"]}SetNullBy{stringUtil.upper_str_first(config["key"]["attr"])}({config["className"]} {stringUtil.low_str_first(config["className"])});\n\n'

    # 主键查
    method_str += f'{tag}public {config["className"]} select{config["className"]}By{stringUtil.upper_str_first(config["key"]["attr"])}({config["key"]["type"]} {config["key"]["attr"]});\n\n'
    # 多字段单查
    method_str += f'{tag}public {config["className"]} selectOne{config["className"]}({select_low_param_class_name}{config["className"]} {stringUtil.low_str_first(config["className"])}{key_word_str}, @Param("index")Integer index{temp_sql});\n\n'
    # 普通查
    method_str += f'{tag}public List<{config["className"]}> select{config["className"]}({select_low_param_class_name}{config["className"]} {stringUtil.low_str_first(config["className"])}{key_word_str}, @Param("page") Page page{temp_sql});\n\n'
    # 普通计数
    method_str += f'{tag}public Integer count{config["className"]}({low_param_class_name}{config["className"]} {stringUtil.low_str_first(config["className"])}{key_word_str});\n\n'

    # 一对一内联
    import_set = set()
    if "oneToOne" in config:
        for obj in config["oneToOne"]:
            temp_key_word = ""
            if "keyWord" in obj and "keyWordList" in obj and len(obj["keyWordList"]) > 0:
                temp_key_word = f', @Param("{obj["keyWord"]}1") String {obj["keyWord"]}1'
            method_str += f'{tag}public List<{config["className"]}> find{config["className"]}OneToOne{obj["className"]}({select_low_param_class_name}{config["className"]} {stringUtil.low_str_first(config["className"])}{key_word_str}, @Param("{stringUtil.low_str_first(obj["className"])}") {obj["className"]} {stringUtil.low_str_first(obj["className"])}{temp_key_word}, @Param("page") Page page{temp_sql});\n\n'
            method_str += f'{tag}public Integer countFind{config["className"]}OneToOne{obj["className"]}({select_low_param_class_name}{config["className"]} {stringUtil.low_str_first(config["className"])}{key_word_str}, @Param("{stringUtil.low_str_first(obj["className"])}") {obj["className"]} {stringUtil.low_str_first(obj["className"])}{temp_key_word});\n\n'
            import_set.add(f'import {obj["path_pojo"]}.{obj["className"]};\n')

    # 一对多内联
    if "oneToMany" in config:
        for obj in config["oneToMany"]:
            temp_key_word = ""
            if "keyWord" in obj and "keyWordList" in obj and len(obj["keyWordList"]) > 0:
                temp_key_word = f', @Param("{obj["keyWord"]}1") String {obj["keyWord"]}1'
            method_str += f'{tag}public List<{config["className"]}> find{config["className"]}OneToMany{obj["className"]}({select_low_param_class_name}{config["className"]} {stringUtil.low_str_first(config["className"])}{key_word_str}, @Param("{stringUtil.low_str_first(obj["className"])}") {obj["className"]} {stringUtil.low_str_first(obj["className"])}{temp_key_word}, @Param("page") Page page, @Param("page1") Page page1{temp_sql});\n\n'
            method_str += f'{tag}public Integer countFind{config["className"]}OneToMany{obj["className"]}({select_low_param_class_name}{config["className"]} {stringUtil.low_str_first(config["className"])}{key_word_str}, @Param("{stringUtil.low_str_first(obj["className"])}") {obj["className"]} {stringUtil.low_str_first(obj["className"])}{temp_key_word}, @Param("page") Page page, @Param("page1") Page page1);\n\n'
            import_set.add(f'import {obj["path_pojo"]}.{obj["className"]};\n')

    # 一对一外联
    if "oneToOne" in config:
        for obj in config["oneToOne"]:
            temp_key_word = ""
            if "keyWord" in obj and "keyWordList" in obj and len(obj["keyWordList"]) > 0:
                temp_key_word = f', @Param("{obj["keyWord"]}1") String {obj["keyWord"]}1'
            method_str += f'{tag}public List<{config["className"]}> query{config["className"]}OneToOne{obj["className"]}({select_low_param_class_name}{config["className"]} {stringUtil.low_str_first(config["className"])}{key_word_str}, @Param("{stringUtil.low_str_first(obj["className"])}") {obj["className"]} {stringUtil.low_str_first(obj["className"])}{temp_key_word}, @Param("page") Page page{temp_sql});\n\n'
            # 左外连无需计数，总次数为左表
            # method_str += f'{tag}public Integer countQuery{config["className"]}OneToOne{obj["className"]}({select_low_param_class_name}{config["className"]} {stringUtil.low_str_first(config["className"])}{key_word_str}, @Param("{stringUtil.low_str_first(obj["className"])}") {obj["className"]} {stringUtil.low_str_first(obj["className"])});\n\n'

    # 一对多外联
    if "oneToMany" in config:
        for obj in config["oneToMany"]:
            temp_key_word = ""
            if "keyWord" in obj and "keyWordList" in obj and len(obj["keyWordList"]) > 0:
                temp_key_word = f', @Param("{obj["keyWord"]}1") String {obj["keyWord"]}1'
            method_str += f'{tag}public List<{config["className"]}> query{config["className"]}OneToMany{obj["className"]}({select_low_param_class_name}{config["className"]} {stringUtil.low_str_first(config["className"])}{key_word_str}, @Param("{stringUtil.low_str_first(obj["className"])}") {obj["className"]} {stringUtil.low_str_first(obj["className"])}{temp_key_word}, @Param("page") Page page, @Param("page1") Page page1{temp_sql});\n\n'
            # 左外连无需计数
            # 左外联最终条数有左表决定
            # method_str += f'{tag}public Integer countQuery{config["className"]}OneToMany{obj["className"]}({select_low_param_class_name}{config["className"]} {stringUtil.low_str_first(config["className"])}{key_word_str}, @Param("{stringUtil.low_str_first(obj["className"])}") {obj["className"]} {stringUtil.low_str_first(obj["className"])});\n\n'

    # 多对多内联
    if "manyToMany" in config:
        for obj in config["manyToMany"]:
            method_str += f'{tag}public List<{config["className"]}> find{config["className"]}ManyToManyLink{obj["to"]["className"]}On{obj["many"]["className"]}({select_low_param_class_name}{config["className"]} {stringUtil.low_str_first(config["className"])}{key_word_str}, @Param("page") Page page{temp_sql});\n\n'

    # 多对多内联
    if "manyToMany" in config:
        for obj in config["manyToMany"]:
            method_str += f'{tag}public List<{config["className"]}> query{config["className"]}ManyToManyLink{obj["to"]["className"]}On{obj["many"]["className"]}({select_low_param_class_name}{config["className"]} {stringUtil.low_str_first(config["className"])}{key_word_str}, @Param("page") Page page{temp_sql});\n\n'

    import_str = ""
    for temp_str in import_set:
        import_str += temp_str
    return method_str, import_str
