这是我制作的安全+agent智能体的模板框架
```
├── main.py              项目入口，一键启动 Mock API 服务 + Gradio 界面
├── config.py            集中管理所有配置项（API Key、端口、模型名等）
├── requirements.txt     Python 依赖包列表
├── .env        环境变量模板（存敏感信息，提交Git前记得检查，防止泄露敏感信息）
│
├── agent/               Agent 模块
│   ├── __init__.py          包声明，对外暴露类
│   ├── agent_core.py        Agent 核心：接收告警→CoT推理→调工具→输出报告
│   └── multi_turn_manager.py 多轮对话管理：维护上下文记忆，支持连续分析
│
├── prompt/              Prompt 模块
│   ├── __init__.py          包声明
│   └── base_prompts.py      安全场景专用Prompt + ReAct模板 + 自动场景检测
│
├── tools/               工具模块
│   ├── __init__.py          包声明
│   ├── main.py              FastAPI Mock API服务，3个模拟接口
│   └── tool_adapter.py      @tool装饰器包装，让Agent能调用上述接口
│
├── knowledge/           知识库模块
│   ├── __init__.py          包声明
│   ├── chroma_client.py     ChromaDB 连接管理，存取向量数据
│   ├── embedding_manager.py 文本转向量（BGE模型），让文本可被检索
│   ├── rag_retriever.py     RAG检索器：查询→检索→融入Prompt
│   └── data_ingestion.py    入库脚本：Excel→分块→向量化→写入ChromaDB
│
├── ui/                  界面模块
│   ├── __init__.py          包声明
│   └── app.py               Gradio Web界面，串联所有模块
│
└── data/                数据目录
    └── vulnerabilities.xlsx 示例安全知识数据
   ```
以下是分工对应的文件，有不同的意见可以直接和我说

agent模块负责人--->agent文件夹

prompt负责人--->prompt文件夹

工具模拟负责人--->tools文件夹

数据采集--->data/vulnerabilities.xlsx（项目模板内未包含）— 安全知识数据采集与维护

RAG检索--->knowledge/rag_retriever

ChromaDB管理+Embedding管理--->knowledge/embedding_manager，chroma_client，data_ingestion
                
Gradio界面负责人--->ui文件夹+main
