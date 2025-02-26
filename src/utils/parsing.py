# src/utils/parsing.py
import json
import logging
from src.utils.logging import logger  # Import the configured logger

def parse_powershell_output(powershell_response: dict, additional_variables: dict):
    """
    Parse JSON output from the PowerShell script and update additional_variables.
    Returns (updated_vars, worknote_content, error_occurred).
    """
    try:
        error_occurred = False
        if powershell_response["Status"] == "Success":
            # Try to load the output as JSON.
            try:
                powershell_output = json.loads(powershell_response["OutputMessage"] or "{}")
            except Exception as json_e:
                logger.error(f"JSON decode error: {json_e}")
                raise RuntimeError("Output is not valid JSON.")
 
            if not isinstance(powershell_output, dict):
                powershell_output = json.loads(powershell_output)
 
            if powershell_output.get("Status") == "Success":
                additional_variables.update(powershell_output)
                worknote_content = powershell_output.get("OutputMessage", "Execution Successful")
            else:
                OutputMessage = powershell_output.get("OutputMessage", "")
                ErrorMessage = powershell_output.get("ErrorMessage", "")
                worknote_content = f"{OutputMessage}\n{ErrorMessage}"
                error_occurred = True
        else:
            worknote_content = powershell_response["ErrorMessage"]
        return additional_variables, worknote_content, error_occurred
    except Exception as e:
        raise RuntimeError(f"Error parsing PowerShell execution: {e}")