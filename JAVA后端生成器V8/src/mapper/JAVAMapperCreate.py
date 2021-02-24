
def create_java_mapper(config: dict):
    data = f'package {config["path_java_mapper"]};\n\n'
    # data += "import java.util.List;\n"
    # data += f'import {config["path_util"]}.Page;\n'
    data += f'import org.apache.ibatis.annotations.Mapper;\n'
    # data += "import org.apache.ibatis.annotations.Param;\n\n"
    data += f'\n@Mapper\n'
    data += f'public interface {config["javaMapperName"]} extends {config["javaAutoMapperName"]} {{\n\n}}'
    return data
