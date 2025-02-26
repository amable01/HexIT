# src/flow/decisions.py
from typing import Literal
from src.models.state import FlowState

def determine_flow_outcome(state: FlowState) -> Literal["execute_flow_script", "END"]:
    return "execute_flow_script" if state["next_action"] else "END"