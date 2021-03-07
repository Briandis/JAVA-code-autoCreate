# 创建POJO的文件
def create_pojo(config: dict) -> str:
    tag = "\t"
    # 打开本包并换行
    data = f'package {config["path_pojo"]};\n'
    data += '\n'
    data += f'public class {config["className"]} extends {config["className"]}Auto<{config["className"]}>{{\n\n}}'
    return data
