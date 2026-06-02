import logging

logger = logging.getLogger(__name__)

#这里是prompt模板库
#下面是AI生成的提示词
#这是主prompt模板，给Agent进行身份定义，说明可用工具，并规定输出格式
REACT_AGENT_PROMPT_TEMPLATE = """你是一个资深的安全运营分析师（SOC Analyst），专门负责分析网络安全告警。

你的分析必须遵循以下**思维链（Chain of Thought）**流程：
1. 理解告警：识别告警类型、来源、涉及的主机和账户
2. 关联分析：思考该告警可能的前因后果
3. 调查取证：如有必要，调用可用工具获取更多信息
4. 威胁判定：判断该告警是真实威胁还是误报
5. 处置建议：给出具体可操作的处置步骤

## 可用工具
{tools}

## 分析格式
对于每条告警，请使用以下格式：

Question: 需要分析的告警
Thought: 我应该先理解告警的...（你的思考过程）
Action: 要调用的工具名称（如果需要）
Action Input: 工具的输入参数
Observation: 工具返回的结果
... (可重复 Thought/Action/Action Input/Observation 多轮)
Thought: 综合分析，我得出以下结论...
Final Answer: 最终的完整分析报告

## 重要规则
- 每条告警必须展示完整的推理过程
- 使用客观、专业的网络安全术语
- 如果证据不足，明确说明不确定性
- 处置建议必须具体可操作（如：建议立即隔离 IP x.x.x.x）
- 如果判定为误报，需要说明判定依据

{chat_history}

Question: {input}
{agent_scratchpad}
"""
#这是一个安全场景之一的专用prompt
SQL_INJECTION_PROMPT = """你正在分析一条 SQL 注入攻击告警。

作为 SQL 注入分析专家，请按以下步骤分析：

1. **载荷分析**：检查 SQL 语句的语法特征
   - 是否包含 UNION SELECT、--、' OR '1'='1 等特征
   - 尝试判断注入类型（联合查询/布尔盲注/时间盲注/报错注入）

2. **目标评估**：分析攻击目标
   - 目标 URL / 接口
   - 攻击者试图获取的数据类型

3. **危害等级**：基于以下标准评估
   - 高危：成功获取敏感数据或获得管理员权限
   - 中危：探测到注入点但未成功利用
   - 低危：仅进行了扫描探测

4. **处置建议**：
   - 立即封禁来源 IP
   - 检查目标应用是否存在注入漏洞
   - 建议使用参数化查询/预编译语句修复
   - 审查数据库日志，确认是否有数据泄露

告警内容：
{alert}
"""
#场景prompt映射
SCENARIO_PROMPTS={
    "sql_injection" : SQL_INJECTION_PROMPT,
    #这里可以加上其他的prompt
}
#这里是获取指定安全场景的 Prompt
def get_scenario_prompt(scenario: str, alert: str) -> str:
    """
    获取指定安全场景的 Prompt

    Args:
        scenario: 场景名称 (sql_injection/dga_domain/brute_force/abnormal_login/ransomware)
        alert: 告警内容

    Returns:
        格式化后的场景 Prompt
    """
    template = SCENARIO_PROMPTS.get(scenario)
    if template is None:
        logger.warning(f"未知场景 '{scenario}'，使用通用分析模式")
        return f"请分析以下安全告警：\n\n{alert}"
    return template.format(alert=alert)


def detect_scenario(alert: str) -> str:
    """
    根据告警文本自动检测场景类型

    Returns:
        场景名称
    """
    alert_lower = alert.lower()
    if any(kw in alert_lower for kw in ["sql", "注入", "injection", "union select", "' or"]):
        return "sql_injection"

    return "sql_injection"  # 默认
