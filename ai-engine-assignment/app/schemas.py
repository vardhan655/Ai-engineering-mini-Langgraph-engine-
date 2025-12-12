from typing import List, Dict, Any, Optional, Union
from pydantic import BaseModel, Field

# Represents the shared state passing between nodes
class WorkflowState(BaseModel):
    data: Dict[str, Any] = Field(default_factory=dict)
    execution_log: List[str] = Field(default_factory=list)

# Defines a single node in the graph
class NodeDefinition(BaseModel):
    id: str
    function_name: str  # References a registered function

# Defines the connection logic
class EdgeDefinition(BaseModel):
    source: str
    target: str
    condition: Optional[str] = None # Name of a condition function (returns boolean)

# Input for POST /graph/create
class GraphCreateRequest(BaseModel):
    name: str
    nodes: List[NodeDefinition]
    edges: List[EdgeDefinition]
    start_node: str

# Response for POST /graph/run
class RunResponse(BaseModel):
    run_id: str
    status: str
    final_state: Optional[Dict[str, Any]] = None
    logs: List[str] = []