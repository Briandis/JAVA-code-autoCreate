from src.analysis.analysis import SQLLinkUtil
from src.generate.generateAnalysis import Generate
import json
import os
import traceback

try:
    if not os.path.exists(os.path.join(os.getcwd(), "config.json")):
        raise FileNotFoundError("config.json不存在！！！！！")
    data = json.load(open("config.json", encoding="utf-8"))
    analysis = SQLLinkUtil(data)
    analysis.get_all_table()
    analysis.mapping_relations()
    analysis.save_model_json()
    input("config文件夹中可修改部分信息，随意输入继续")
except Exception:
    traceback.print_exc()
    input(f"解析器发生错误")

try:
    g = Generate()
    g.generate()
    input("随意输入后退出")
except Exception:
    traceback.print_exc()
    input(f"生成器发生错误")
