# src/flow/nodes/update_servicenow_worknotes.py
import httpx
import logging
from src.models.state import FlowState
from src.utils.env import user, pwd, endpoint

async def update_servicenow_worknotes(state: FlowState) -> FlowState:
    """Update the ServiceNow record's worknotes with the result of the action."""
    logging.debug("Updating worknotes on ServiceNow.")
    try:
        task_response = state["task_response"]
        content = state["worknote_content"]
 
        table_name = task_response["result"][0]["sys_class_name"]
        sys_id = task_response["result"][0]["sys_id"]
        url = f"{endpoint}/api/now/table/{table_name}/{sys_id}"
 
        body = {"work_notes": content}
 
        async with httpx.AsyncClient() as client:
            auth = (user, pwd)
            resp = await client.put(
                url,
                auth=auth,
                headers={"Content-Type": "application/json", "Accept": "application/json"},
                json=body
            )
            if resp.status_code != 200:
                logging.error(f"Failed to update worknotes: {resp.json()}")
                raise Exception(f"Failed to update worknotes: {resp.json()}")
 
        state["worknote_content"] = "Worknotes updated successfully"
    except Exception as e:
        logging.error(f"Error updating worknotes: {e}")
        raise RuntimeError(f"Error updating worknotes: {e}")
 
    logging.debug(f"State after updating worknotes: {state}")
    return state