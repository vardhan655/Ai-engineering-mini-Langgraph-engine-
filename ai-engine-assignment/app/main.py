import sys
import os

# --- FIX: Auto-detect folder paths ---
# This forces Python to look in the right place, no matter where you run the command from.
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
# -------------------------------------

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any

# Now we can safely import using the 'app.' prefix
try:
    from app.schemas import GraphCreateRequest, RunResponse
    from app.engine import WorkflowEngine
    from app.workflow_impl import register_all_tools
except ImportError:
    # Fallback if running from inside the app folder
    from schemas import GraphCreateRequest, RunResponse
    from engine import WorkflowEngine
    from workflow_impl import register_all_tools

app = FastAPI(title="Mini LangGraph Engine")
engine = WorkflowEngine()

# Pre-register our sample workflow tools so they are available
register_all_tools(engine)

# 1. Create Graph Endpoint
@app.post("/graph/create")
async def create_graph(request: GraphCreateRequest):
    graph_id = engine.create_graph(request)
    return {"graph_id": graph_id, "message": "Graph created successfully"}

# 2. Run Graph Endpoint
class RunRequest(BaseModel):
    graph_id: str
    initial_state: Dict[str, Any] = {}

@app.post("/graph/run", response_model=RunResponse)
async def run_graph(request: RunRequest):
    try:
        run_id = await engine.run_graph(request.graph_id, request.initial_state)
        # Fetch the result from memory
        final_state = engine.runs[run_id]
        
        return RunResponse(
            run_id=run_id,
            status="completed",
            final_state=final_state.data,
            logs=final_state.execution_log 
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# 3. Get State Endpoint
@app.get("/graph/state/{run_id}")
async def get_state(run_id: str):
    if run_id not in engine.runs:
        raise HTTPException(status_code=404, detail="Run ID not found")
    
    state = engine.runs[run_id]
    return {
        "run_id": run_id,
        "current_state": state.data,
        "logs": state.execution_log
    }

# Seed the data for testing
@app.on_event("startup")
async def seed_sample_workflow():
    sample_graph = GraphCreateRequest(
        name="Code Review Agent",
        start_node="extract",
        nodes=[
            {"id": "extract", "function_name": "extract_functions"},
            {"id": "check", "function_name": "check_complexity"},
            {"id": "detect", "function_name": "detect_basic_issues"},
            {"id": "suggest", "function_name": "suggest_improvements"},
        ],
        edges=[
            {"source": "extract", "target": "check"},
            {"source": "check", "target": "detect"},
            {"source": "detect", "target": "suggest"},
            {"source": "suggest", "target": "check", "condition": "needs_improvement"},
        ]
    )
    gid = engine.create_graph(sample_graph)
    print(f"\n✅ SUCCESS! Server is running.")
    print(f"👉 COPY THIS ID for your test: {gid}\n")