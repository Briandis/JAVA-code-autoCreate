def create_java_mapper(config: dict):
    data = f'package {config["extradimensionalData"]["path_java_mapper"]};\n\n'
    data += f'import org.apache.ibatis.annotations.Mapper;\n'
    data += f'import {config["path_java_mapper"]}.{config["javaMapperName"]};\n'
    data += f'\n@Mapper\n'
    data += f'public interface {config["extradimensionalData"]["javaMapperName"]} extends {config["javaMapperName"]} {{\n\n}}'
    return data
