# src/flow/graph.py
from langgraph.graph import StateGraph, START, END
from src.flow.nodes.initialize_flow_state import initialize_flow_state
from src.flow.nodes.retrieve_flow_scripts import retrieve_flow_scripts
from src.flow.nodes.evaluate_flow_decision import evaluate_flow_decision
from src.flow.nodes.execute_flow_script import execute_flow_script
from src.flow.nodes.update_servicenow_worknotes import update_servicenow_worknotes
from src.flow.decisions import determine_flow_outcome
from src.models.state import FlowState

# Build the StateGraph
builder = StateGraph(FlowState)

builder.add_node("initialize_flow_state", initialize_flow_state)
builder.add_node("retrieve_flow_scripts", retrieve_flow_scripts)
builder.add_node("evaluate_flow_decision", evaluate_flow_decision)
builder.add_node("execute_flow_script", execute_flow_script)
builder.add_node("update_servicenow_worknotes", update_servicenow_worknotes)

builder.add_edge(START, "initialize_flow_state")
builder.add_edge("initialize_flow_state", "retrieve_flow_scripts")
builder.add_edge("retrieve_flow_scripts", "evaluate_flow_decision")
builder.add_conditional_edges("evaluate_flow_decision", determine_flow_outcome)
builder.add_edge("execute_flow_script", "update_servicenow_worknotes")
builder.add_edge("update_servicenow_worknotes", "evaluate_flow_decision")

# Global variable to store the compiled graph
_graph = None

async def init_graph():
    """
    Initialize and return the compiled StateGraph with the AsyncSqliteSaver.
    This will be called once in the FastAPI startup event.
    """
    global _graph
    if _graph is None:
        import aiosqlite
        from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
        from src.utils.env import db_path
        conn = await aiosqlite.connect(db_path, check_same_thread=False)
        memory = AsyncSqliteSaver(conn)
        _graph = builder.compile(checkpointer=memory)
    return _graph