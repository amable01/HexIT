# src/flow/decisions.py
from typing import Literal
from langgraph.graph import END  # Import the END constant
from src.models.state import FlowState

def determine_flow_outcome(state: FlowState) -> Literal["execute_flow_script", END]:  # Update type hint
    return "execute_flow_script" if state["next_action"] else END  # Return END constant, not "END" string
