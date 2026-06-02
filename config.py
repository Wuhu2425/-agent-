from plistlib import load
import os
from  dotenv import load_dotenv

load_dotenv()

LLM_API_KEY=os.getenv("LLM_API_KEY","API_KEY")
LLM_BASE_URL=os.getenv("LLM_BASE_URL","https://api.deepseek.com/v1")
LLM_MODEL=os.getenv("LLM_MODEL","deepseek-v4-flash")

AGENT_MAX_RETIES=3
AGENT_MAX_TURNS=10
AGENT_TEMPERATURE=0.1

TOOLS_HOST = os.getenv("TOOLS_HOST", "127.0.0.1")
TOOLS_PORT = int(os.getenv("TOOLS_PORT", "8801"))


# ChromaDB 知识库配置

CHROMA_PERSIST_DIR = os.path.join()
CHROMA_COLLECTION_NAME = "模板代码"
EMBEDDING_MODEL = os.getenv()
EMBEDDING_DEVICE = os.getenv()

# RAG 检索配置

RAG_TOP_K = 5
RAG_CHUNK_SIZE = 500
RAG_CHUNK_OVERLAP = 50

# 安全场景定义

SECURITY_SCENARIOS = [
    "sql_injection",       # SQL 注入告警

]


# Gradio 配置

GRADIO_HOST= "127.0.0.1"
GRADIO_PORT = 7860
GRADIO_TITLE = "模板代码"
