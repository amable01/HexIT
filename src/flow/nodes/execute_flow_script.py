# src/flow/nodes/execute_flow_script.py
import os
import json
import logging
from src.models.state import FlowState
from src.services.script_executor import run_script

async def execute_flow_script(state: FlowState) -> FlowState:
    """
    Executes the current script in the workflow and updates the FlowState accordingly.
    Only executes .ps1, .py, and .js files; skips others silently.
    """
    logging.debug("Executing current action.")
    
    idx = state["action_index"]
    actions = state["actions_list"]
    additional_vars = state["additional_variables"]
    task_response = state["task_response"]
    flow_name = state["flow_name"]
    
    action_name = actions[idx]
    action_path = os.path.join("UseCases", flow_name, action_name)
    logging.debug(f"Checking action script: {action_path}")
    
    allowed_extensions = ('.ps1', '.py', '.js')
    
    # Skip non-script files silently
    if not action_path.lower().endswith(allowed_extensions):
        logging.debug(f"Skipping {action_name}: Not a script file")
        state["action_index"] = idx + 1
        return state
    
    try:
        logging.debug(f"Running action script: {action_path}")
        ps_result = await run_script(action_path, additional_vars, task_response)
        
        state["execution_log"].append({
            "script": action_name,
            "Status": ps_result["Status"],
            "OutputMessage": ps_result["OutputMessage"],
            "ErrorMessage": ps_result["ErrorMessage"]
        })
        
        if ps_result["Status"] == "Error":
            logging.error(f"Error executing {action_name}: {ps_result['ErrorMessage']}")
            state["worknote_content"] = f"Error in {action_name}: {ps_result['ErrorMessage']}"
            state["error_occurred"] = True
        else:
            output = ps_result["OutputMessage"]
            if isinstance(output, str):
                try:
                    output = json.loads(output)
                except json.JSONDecodeError:
                    state["worknote_content"] = output
                    state["error_occurred"] = False
                else:
                    if output.get("Status") == "Success":
                        state["additional_variables"].update(output)
                        state["worknote_content"] = output.get("OutputMessage", "Execution Successful")
                        state["error_occurred"] = False
                    else:
                        state["worknote_content"] = f"{output.get('OutputMessage', '')}\n{output.get('ErrorMessage', '')}"
                        state["error_occurred"] = True
            elif isinstance(output, dict):
                if output.get("Status") == "Success":
                    state["additional_variables"].update(output)
                    state["worknote_content"] = output.get("OutputMessage", "Execution Successful")
                    state["error_occurred"] = False
                else:
                    state["worknote_content"] = f"{output.get('OutputMessage', '')}\n{output.get('ErrorMessage', '')}"
                    state["error_occurred"] = True
            else:
                state["worknote_content"] = str(output)
                state["error_occurred"] = False
    
    except Exception as e:
        logging.error(f"Execution failed for {action_name}: {e}")
        state["worknote_content"] = f"Execution failed for {action_name}: {e}"
        state["error_occurred"] = True
    
    state["action_index"] = idx + 1
    
    return state