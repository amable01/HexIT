# src/api/endpoints.py
import logging
from fastapi import FastAPI, HTTPException
from src.flow.graph import init_graph  # Import the graph initialization
from src.models.servicenow_api import APIResponse  # Import the APIResponse model

# Global variable to hold the graph (will be initialized on startup)
graph = None

@app.on_event("startup")
async def startup_event():
    """
    On application startup, initialize our StateGraph by calling init_graph().
    """
    global graph
    graph = await init_graph()  # This ensures the graph is compiled once.

@app.get("/")
async def read_root():
    return {"message": "LangGraph Assistant is Running (Async)!"}

@app.post("/api/task")
async def execute_flow(task_data: APIResponse):
    """
    Endpoint to handle the flow for a given "number" (e.g. the ServiceNow Task Number).
    We will parse the JSON, create a thread_id, and invoke the graph.
    """
    try:
        # Build the dict in the same format as the original code expects:
        task_response = task_data.model_dump()
        
        # Construct a unique thread_id. For example:
        thread_id = "task_" + task_response["result"][0]["number"]
 
        # Now invoke the graph asynchronously
        output = graph.ainvoke(
            {"task_response": task_response},
            config={"configurable": {"thread_id": thread_id}, "recursion_limit": 100}
        )
 
        # Since ainvoke returns an Awaitable, await it here as the route is async
        return await output
 
    except Exception as e:
        logging.error(f"Error executing flow: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Function to attach the app (used in main.py)
def setup_api(app: FastAPI):
    # No additional routing needed since endpoints are defined directly on the app
    pass