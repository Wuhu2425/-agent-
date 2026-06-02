
from fastapi import FastAPI, HTTPException

app=fastAPI()

#可以调用数据模型规范API的输出
#class 数据模型

#这里单独调用需要API的安全工具
#按照下面格式创建数据模型
#class 数据模型名(BaseModel):
#这里用小明举例
#class xiaoming(baseModel):
#   name:str
#   age:int
#   school:str
#   grade:double

#@app.get("路由定义", responce_model=按要求填入参数):
#def 工具函数名(最好可以说明工具作用，动词+名词形式) (ip:工具对应的FastAPI的ip)-> 返回数据类型
#   """这里填入上工具的详细说明"""
#   函数体
#   return 数据模型(传入参数)

@app.get("/")
def root():
    return {"service": "样例代码","version":"0.0.1"}


#下面这段可以在测试时判断服务是否可用
#访问时可以用浏览器访问http://127.0.0.1:8801加上上面每个工具的路由定义
if __name__ == "__main__":#判断是否单独运行这个python文件
    import uvicorn
    uvicorn.run(
            app,#fastAPI应用对象
            host="127.0.0.1",#监听地址
            port=8801#监听端口
            )