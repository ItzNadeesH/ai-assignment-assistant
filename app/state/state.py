from typing import TypedDict, List, Optional

class AgentState(TypedDict):
    input: str
    github_query: str
    plan: str
    solution: str
    evaluation: str
    logs: List[str]