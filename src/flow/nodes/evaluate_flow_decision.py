# src/flow/nodes/evaluate_flow_decision.py
import logging
from src.models.state import FlowState, TicketState
from src.services.servicenow import update_ticket_state, update_servicenow_assignment_group

async def evaluate_flow_decision(state: FlowState) -> FlowState:
    """Decide whether to continue or end the flow."""
    logging.debug("Assistant node: deciding next step.")
    if state["error_occurred"]:
        state["next_action"] = False
        updated_state = await update_servicenow_assignment_group(state)
        logging.debug("Assistant: error_occured=True, will end flow.")
        return updated_state
 
    if state["action_index"] < len(state["actions_list"]):
        state["next_action"] = True
        state["current_action"] = state["actions_list"][state["action_index"]]
        logging.debug(f"Assistant: next_action=True. Next script: {state['current_action']}")
    else:
        state["next_action"] = False
        state["current_action"] = ""
        state = await update_ticket_state(state, TicketState.CLOSED_COMPLETE)
        logging.debug("Assistant: no more actions, ending flow.")
 
    return state