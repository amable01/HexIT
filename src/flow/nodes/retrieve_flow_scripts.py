# src/flow/nodes/retrieve_flow_scripts.py
import os
import logging
from src.models.state import FlowState

async def retrieve_flow_scripts(state: FlowState) -> FlowState:
    """Fetch only script files (.ps1, .py, .js) from UseCases/<flow_name>."""
    logging.debug("Fetching actions for the flow.")
    flow_dir = "UseCases"
    try:
        actions_dir = os.path.join(flow_dir, state["flow_name"])
        # Only include files with script extensions
        valid_extensions = ('.ps1', '.py', '.js')
        actions_list = [
            f for f in os.listdir(actions_dir)
            if os.path.isfile(os.path.join(actions_dir, f)) and f.lower().endswith(valid_extensions)
        ]
        state["actions_list"] = actions_list
        logging.debug(f"Actions found: {actions_list}")
    except Exception as e:
        logging.error(f"Error fetching actions: {e}")
        raise RuntimeError(f"Error fetching actions: {e}")
 
    return state