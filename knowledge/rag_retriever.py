#检索数据库并增强prompt
from typing import Optional

from config import RAG_TOP_K
from prompt.base_prompts import get_scenario_prompt



class RAGRetriever:
    #RAG 检索器 — 从知识库检索相关内容，增强 LLM 回答的准确性
    #对外暴露标准化接口: retrieve(query) -> list
    def __init__(self, chroma_manager, embedding_manager):
        self.chroma = chroma_manager
        self.embedding = embedding_manager
        self.top_k = RAG_TOP_K

    def retrieve(self, query: str, top_k: Optional[int] = None) -> list[dict]:

        #检索标准接口

        #Args:
        #    query: 查询文本
        #    top_k: 返回结果数

        #Returns:
        #    [{"content": str, "metadata": dict, "score": float}, ...]
        return list