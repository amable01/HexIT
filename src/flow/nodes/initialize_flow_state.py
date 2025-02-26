# src/flow/nodes/initialize_flow_state.py
import yaml
from src.models.state import FlowState, TicketState
from src.services.servicenow import update_ticket_state
import logging

async def initialize_flow_state(state: FlowState) -> FlowState:
    """
    Determine the flow name from the short_description and initialize the state.
    By reading from a YAML file.
    """
    logging.debug("Checking flow name.")
    task_response = state["task_response"]
    if "result" not in task_response or not task_response["result"]:
        raise ValueError("Task response is missing 'result' data.")
 
    short_description = task_response["result"][0].get("short_description")
    if not short_description:
        raise ValueError("Short description is missing in the task response.")
 
    # --- Load from YAML ---
    try:
        with open("config\flow_details.yml", "r", encoding="utf-8") as f:
            yaml_data = yaml.safe_load(f)
            flow_map = {
                item["short_description"]: {
                    "flow_name": item["flow_name"],
                    "reassignment_group": item["reassignment_group"],
                }
                for item in yaml_data.get("flows", [])
            }
    except FileNotFoundError:
        raise ValueError("flow_details.yml file not found.")
    except KeyError as e:
        raise ValueError(f"Missing key in flow_details.yml: {e}")
 
    if short_description not in flow_map:
        logging.error(f"No flow found for: {short_description}")
        raise ValueError(f"No flow found for short description: {short_description}")
 
    mapping_data = flow_map[short_description]
    state["flow_name"] = mapping_data["flow_name"]
    logging.debug(f"Flow name determined: {state['flow_name']}")
 
    state["reassignment_group"] = mapping_data["reassignment_group"]
 
    state["actions_list"] = []
    state["current_action"] = ""
    state["worknote_content"] = ""
    state["execution_log"] = []
    state["action_index"] = 0
    state["next_action"] = False
    state["error_occurred"] = False
    state["additional_variables"] = {}
 
    updated_state = await update_ticket_state(state, TicketState.WORK_IN_PROGRESS)
    return updated_state