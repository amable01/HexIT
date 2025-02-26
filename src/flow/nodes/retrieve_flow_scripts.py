# src/flow/nodes/retrieve_flow_scripts.py
import os
import logging
from src.models.state import FlowState

async def retrieve_flow_scripts(state: FlowState) -> FlowState:
    """Fetch PowerShell scripts from UseCases/<flow_name>."""
    logging.debug("Fetching actions for the flow.")
    flow_dir = "UseCases"
    try:
        actions_dir = os.path.join(flow_dir, state["flow_name"])
        actions_list = os.listdir(actions_dir)
    except Exception as e:
        logging.error(f"Error fetching actions: {e}")
        raise RuntimeError(f"Error fetching actions: {e}")
 
    state["actions_list"] = actions_list
    logging.debug(f"Actions found: {actions_list}")
    return state