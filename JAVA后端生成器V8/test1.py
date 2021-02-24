from src.analysis.analysis import SQLLinkUtil
import json
import traceback
import os

# 纯配置生成器
try:
    if not os.path.exists(os.path.join(os.getcwd(), "config.json")):
        raise FileNotFoundError("config.json不存在！！！！！")
    data = json.load(open("config.json", encoding="utf-8"))
    analysis = SQLLinkUtil(data)
    analysis.get_all_table()
    analysis.mapping_relations()
    analysis.save_model_json()
    input("随意输入后退出")
except Exception:
    traceback.print_exc()
    input(f"解析器发生错误")
