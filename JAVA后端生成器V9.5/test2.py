from src.generate.generateAnalysis import Generate
import traceback

# 纯生成器
try:
    g = Generate()
    g.generate()
    input("随意输入后退出")
except Exception:
    traceback.print_exc()
    input(f"生成器发生错误")
