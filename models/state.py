# src/models/state.py
from typing_extensions import TypedDict
from enum import IntEnum

class FlowState(TypedDict):
    task_response: dict
    flow_name: str
    actions_list: list
    current_action: str
    additional_variables: dict
    worknote_content: str
    execution_log: list  # We'll store logs & updates here
    action_index: int
    next_action: bool
    error_occurred: bool
    reassignment_group: str

class TicketState(IntEnum):
    PENDING = 0
    OPEN = 1
    WORK_IN_PROGRESS = 2
    CLOSED_COMPLETE = 3
    CLOSED_INCOMPLETE = 4
    CLOSED_SKIPPED = 5
    RESOLVED = 6