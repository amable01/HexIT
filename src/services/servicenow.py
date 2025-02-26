# src/services/servicenow.py
import httpx
import json
import logging
from src.models.state import FlowState, TicketState
from src.utils.env import user, pwd, endpoint

async def update_ticket_state(state: FlowState, task_state: TicketState) -> FlowState:
    """
    Update the ticket state in ServiceNow using the given task_state and log the change.
    """
    try:
        task_response = state["task_response"]
        state_request = {"state": str(task_state.value)}
        updated_state_json = json.dumps(state_request)
 
        table_name = task_response["result"][0]["sys_class_name"]
        sys_id = task_response["result"][0]["sys_id"]
 
        url = f"{endpoint}/api/now/table/{table_name}/{sys_id}"
        async with httpx.AsyncClient() as client:
            auth = (user, pwd)
            resp = await client.put(
                url,
                auth=auth,
                headers={"Content-Type": "application/json", "Accept": "application/json"},
                content=updated_state_json
            )
            if resp.status_code != 200:
                raise Exception(f"Failed to update state: {resp.json()}")
 
        state["worknote_content"] = "Worknotes updated successfully"
        state["execution_log"].append({
            "action": "update_ticket_state",
            "ticket_state_value": task_state.value,
            "ticket_state_name": task_state.name,
            "description": f"Ticket state successfully updated to {task_state.name} ({task_state.value})."
        })
    except Exception as e:
        raise RuntimeError(f"Error updating state: {e}")
    return state

async def update_servicenow_assignment_group(state: FlowState):
    try:
        task_response = state["task_response"]
        reassignment_group_sys_id = state["reassignment_group"]
        data = {"assignment_group": reassignment_group_sys_id}
 
        table_name = task_response["result"][0]["sys_class_name"]
        sys_id = task_response["result"][0]["sys_id"]
        url = f"{endpoint}/api/now/table/{table_name}/{sys_id}"
 
        async with httpx.AsyncClient() as client:
            auth = (user, pwd)
            resp = await client.put(
                url,
                auth=auth,
                headers={"Content-Type": "application/json", "Accept": "application/json"},
                data=json.dumps(data)
            )
            if resp.status_code != 200:
                raise Exception(f"Failed to update assignment group: {resp.json()}")
 
        state["worknote_content"] = "Worknotes updated successfully"
        state["execution_log"].append({
            "action": "update_servicenow_assignment_group",
        })
    except Exception as e:
        raise RuntimeError(f"Error updating assignment group: {e}")
    return state