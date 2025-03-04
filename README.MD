
# src/services/script_executor.py
import os
import json
import asyncio
import subprocess
import sys
import logging
from src.utils.parsing import parse_powershell_output

async def run_script(script_path: str, inputs: dict, task_response: dict) -> dict:
    """
    Execute a script based on its file extension asynchronously.
    Supports:
      - Python (.py): Runs with 'python' interpreter; inputs passed as a JSON string.
      - Node.js (.js): Runs with 'node' interpreter; inputs passed as a JSON string.
      - PowerShell (.ps1): Runs with 'powershell'; inputs passed as individual key-value arguments.

    Args:
        script_path (str): Path to the script file.
        inputs (dict): Input data for the script.
        task_response (dict): Task response data from ServiceNow.

    Returns:
        dict: Execution result containing:
            - Status: "Success" or "Error"
            - OutputMessage: Parsed outputs from the script (if available)
            - ErrorMessage: Any error message encountered
    """
    if not os.path.exists(script_path):
        error_msg = f"Script file not found: {script_path}"
        logging.error(error_msg)
        return {"Status": "Error", "OutputMessage": {}, "ErrorMessage": error_msg}

    ext = os.path.splitext(script_path)[1].lower()

    try:
        if ext == ".py":
            script_dir = os.path.dirname(script_path)
            venv_dir = os.path.join(script_dir, 'venv')
            venv_dir = os.path.abspath(venv_dir)
            python_executable = os.path.join(venv_dir, 'Scripts', 'python.exe')

            # Check if venv exists; create it if not
            if not os.path.exists(python_executable):
                logging.info(f"Virtual environment not found at {venv_dir}. Creating one...")
                try:
                    subprocess.run([sys.executable, "-m", "venv", venv_dir], check=True)
                    logging.info(f"Created virtual environment at {venv_dir}")
                except subprocess.CalledProcessError as e:
                    error_msg = f"Failed to create virtual environment at {venv_dir}: {e}"
                    logging.error(error_msg)
                    return {"Status": "Error", "OutputMessage": {}, "ErrorMessage": error_msg}

            logging.info(f"Using virtual environment at: {venv_dir}")

            if not os.path.exists(python_executable):
                return {"Status": "Error", "OutputMessage": {}, "ErrorMessage": f"Python executable not found at: {python_executable}"}

            inputs_json = json.dumps(inputs)
            command = [python_executable, os.path.abspath(script_path), inputs_json]
            logging.info(f"Executing command: {' '.join(command)}")

            process = await asyncio.create_subprocess_exec(
                *command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=script_dir
            )
            stdout, stderr = await process.communicate()

            print(stderr)
            print(stdout)

            if process.returncode == 0:
                try:
                    outputs = json.loads(stdout.decode().strip())
                except json.JSONDecodeError:
                    outputs = stdout.decode().strip()
                return {"Status": "Success", "OutputMessage": outputs, "ErrorMessage": ""}
            else:
                return {"Status": "Error", "OutputMessage": {}, "ErrorMessage": stderr.decode().strip()}
        
        elif ext == ".js":
            inputs_json = json.dumps(inputs)
            command = ["node", script_path, inputs_json]

            logging.info(f"Executing command: {' '.join(command)}")
            process = await asyncio.create_subprocess_exec(
                *command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()

            stdout_decoded = stdout.decode().strip().replace('\r\n',' ')
            stderr_decoded = stderr.decode().strip().replace('\r\n',' ')

            if process.returncode == 0:
                try:
                    outputs = json.loads(stdout_decoded)
                except json.JSONDecodeError:
                    outputs = stdout_decoded
                return {"Status": "Success", "OutputMessage": outputs, "ErrorMessage": ""}
            else:
                logging.error(f"Script execution error: {stderr_decoded}")
                return {"Status": "Error", "OutputMessage": {}, "ErrorMessage": stderr_decoded}

        elif ext == ".ps1":
            header = (
                f"$jsonObject = '{json.dumps(task_response)}' | ConvertFrom-Json; "
                f"$SCTASK_RESPONSE = $jsonObject.result; "
                f"$ADDITIONAL_VARIABLES = '{json.dumps(inputs)}' | ConvertFrom-Json; "
            )
            with open(script_path, 'r') as script_file:
                file_content = script_file.read()

            powershell_script = header + file_content

            return await run_powershell_command(powershell_script)
        else:
            error_msg = f"Unsupported script file type: {ext}"
            logging.error(error_msg)
            return {"Status": "Error", "OutputMessage": {}, "ErrorMessage": error_msg}

    except Exception as e:
        logging.error(f"Exception occurred during script execution: {e}")
        return {"Status": "Error", "OutputMessage": {}, "ErrorMessage": str(e)}

async def run_powershell_command(command: str):
    """Execute a PowerShell command and return status and output."""
    try:
        logging.debug(f"Executing PowerShell command: {command}")
        result = subprocess.run(
            ["powershell", "-Command", command],
            capture_output=True,
            text=True
        )
        return {
            "Status": "Success" if result.returncode == 0 else "Error",
            "OutputMessage": result.stdout.strip(),
            "ErrorMessage": result.stderr.strip(),
        }
    except Exception as e:
        return {
            "Status": "Error",
            "OutputMessage": "",
            "ErrorMessage": str(e)
        }
