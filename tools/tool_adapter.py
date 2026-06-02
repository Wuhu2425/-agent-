from langchain_core.tools import tool

#创建工具
@tool
def get_current_time() ->str:
    """查询当前时间"""
    from datetime import datetime
    return datetime.now().isoformat()

#可以按照格式在下面创建更多工具
#def 工具函数名(最好可以说明工具作用，动词+名词形式) -> 返回数据类型
#   """这里填入上工具的详细说明"""
#   函数体
#   return 返回数据

#将工具导入工具集
def create_tools()->list:
    """创建工具集"""
    return [get_current_time]