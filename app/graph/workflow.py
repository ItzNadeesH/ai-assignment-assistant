# graph/workflow.py
from langgraph.graph import StateGraph, END
from state.state import AgentState

from agents.coordination_agent import coordination_agent
from agents.analysis_agent import analysis_agent
from agents.solution_agent import solution_agent
from agents.evaluation_agent import evaluation_agent

graph = StateGraph(AgentState)

graph.add_node("coordination", coordination_agent)
graph.add_node("analysis", analysis_agent)
graph.add_node("solution", solution_agent)
graph.add_node("evaluation", evaluation_agent)

graph.set_entry_point("coordination")

graph.add_edge("coordination", "analysis")
graph.add_edge("analysis", "solution")
graph.add_edge("solution", "evaluation")

graph.add_edge("evaluation", END)

app = graph.compile()