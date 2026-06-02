这是我制作的安全+agent智能体的模板
以下是分工对应文件夹的文件，有不同的意见可以直接和我说

agent模块负责人--->agent文件夹

prompt负责人--->prompt文件夹

工具模拟负责人--->tools文件夹

数据采集--->data/vulnerabilities.xlsx（项目内未包含）— 安全知识数据采集与维护

RAG检索--->knowledge/rag_retriever

ChromaDB管理+Embedding管理--->knowledge/embedding_manager，chroma_client，knowledge/data_ingestion
                
Gradio界面负责人--->ui文件夹
