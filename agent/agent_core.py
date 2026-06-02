#agent核心模块
from typing import Optional
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent as create_react_agent
from langchain_core.messages import HumanMessage

from config import (
    LLM_API_KEY, LLM_BASE_URL, LLM_MODEL,
    AGENT_TEMPERATURE, AGENT_MAX_TURNS,
)
from  prompt.base_prompts import REACT_AGENT_PROMPT_TEMPLATE

class Agent:
    """智能体"""

    def __init__(
            self,
            tools:list,
            model:Optional[str]=None,
            temperature: float = AGENT_TEMPERATURE,
    ):
        self.llm = ChatOpenAI(
            api_key=LLM_API_KEY,
            base_url=LLM_BASE_URL,
            model=model or LLM_MODEL,
            temperature=temperature,
        )
        self.tools=tools
        self._graph = None
        self._build_agent()
    def _build_agent(self):
        """构建LangGraph ReAct Agent"""
        # 构建工具列表秒速文本
        tools_desc = "\n".join(
            f"- {t.name}: {t.description}" for t in self.tools
        )
        tool_name = ", ".join(t.name for t in self.tools)

        system_prompt = REACT_AGENT_PROMPT_TEMPLATE.replace(
            "{tools}",tools_desc
        ).replace(
            "{tool_names}",tool_name
        ).replace(
            "{chat_history}",""
        )

        self._graph = create_react_agent(
            model=self.llm,
            tools=self.tools,
            system_prompt=system_prompt,
        )
    def analyze(self,alert: str,context: Optional[str] = None)->dict:
        """
        分析安全告警

        Returns:
            {"alert", "reasoning", "conclusion", "actions", "intermediate_steps"}
        """
        input_text = f"请分析以下安全告警:\n\n{alert}"
        if context:
            input_text += f"\n\n补充上下文：{context}"

        config = {"recursion_limit": AGENT_MAX_TURNS*2+5}

        result = self._graph.invoke(
            {"messages":[HumanMessage(content=input_text)]},
            config=config,
        )

        messages = result.get("message",[])
        return {
            "alert": alert, #原始告警内容
            "reasoning": self._extract_thoughts(messages),      #agent推理过程
            "conclusion": self.extract_final_answer(messages),  #最终结论
            "action": self._extract_tool_calls(messages),       #工具调用记录
            "intermadiate_steps":messages,                      #原始消息列表
        }
    def _extract_thought(self,messages: list)->list:
        """从messages中提取COT思维链(思考 +工具调用)"""
        parts=[]
        for msg in messages:
            msg_type = type(msg).__name__                   #提取消息类名(AIMessage/HumanMessage/ToolMessage)
            if msg_type == "AIMessage":
                content = getattr(msg,content,"")           #提取msg的content属性，找不到则返回空字符串
                tool_calls = getattr(msg,tool_calls,"")     #提取LLM的工具调用记录

                if content:
                    parts.append(f"[思考] {content}")
                for tc in tool_calls:
                    parts.append(f"[调用工具] {tc.get('name','')}->参数：{tc.get('args','')}")
            elif msg_type == "ToolMessage":
                content = str(getattr(msg,"content",""))
                parts.append(f"[工具返回] {content[:500]}")   #截取工具返回内容前500个字符，防止文本过长导致难以阅读
        return "\n\n".join(parts)
    def _extract_final_answer(self,messages: list)->str:
        """从messages中提取最终答案(最后一条AIMessages的content)"""
        for msg in reversed(messages):                      #从后往前遍历消息列表
            if type(msg).__name__ == "AIMessage":
                content = getattr(msg,"content","")
                tool_calls = getattr(msg,"tool_calls",[])
                if content and not tool_calls:              #无工具调用记录时，仅返回content(无工具调用记录时，说明时最终结果)
                    return content
        for msg in reversed(messages):                      #当所有msg中都有工具调用记录时，以最后一个AIMessage的content为返回值
            if type(msg).__name__=="AIMessage":
                return  getattr(msg,"content","")
        return "无法生成分析结论"

    def _extract_tool_calls(self,message: list)->list:
        """提取工具调用记录"""
        action=[]
        for msg in message:
            if type(msg).__name__=="AIMessage":
                tool_calls = getattr(msg,"tool_calls","")
                for tc in tool_calls:
                    action.append({
                        "tool": tc.get("name","unkown"),    #记录工具名
                        "input": str(tc.get("args","")),    #记录传入的参数
                    })
        return action

    def reset(self):
        "重置Agent状态"
        self._build_agent()
