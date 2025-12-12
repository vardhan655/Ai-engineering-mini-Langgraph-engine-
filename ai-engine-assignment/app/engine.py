import asyncio
import uuid
from typing import Dict, Any, Callable
from app.schemas import WorkflowState, GraphCreateRequest  

class WorkflowEngine:
    def __init__(self):
        # In-memory storage for graphs and runs [cite: 39]
        self.graphs: Dict[str, GraphCreateRequest] = {}
        self.runs: Dict[str, WorkflowState] = {}
        self.function_registry: Dict[str, Callable] = {}

    def register_function(self, name: str, func: Callable):
        """Register tools/functions that nodes can use [cite: 24]"""
        self.function_registry[name] = func

    def create_graph(self, graph_def: GraphCreateRequest) -> str:
        graph_id = str(uuid.uuid4())
        self.graphs[graph_id] = graph_def
        return graph_id

    async def run_graph(self, graph_id: str, initial_state: Dict[str, Any]) -> str:
        if graph_id not in self.graphs:
            raise ValueError("Graph not found")

        run_id = str(uuid.uuid4())
        graph_def = self.graphs[graph_id]
        
        # Initialize state
        state = WorkflowState(data=initial_state)
        self.runs[run_id] = state # Store initial state [cite: 39]

        # Async execution of the workflow [cite: 42, 80]
        # We run this as a background task in a real app, 
        # but for this demo, we await it to return the result immediately 
        # or we could return run_id and let user poll.
        # I will await it to satisfy the output requirement of POST /graph/run [cite: 36]
        await self._execute_workflow(run_id, graph_def, state)
        
        return run_id

    async def _execute_workflow(self, run_id: str, graph_def: GraphCreateRequest, state: WorkflowState):
        current_node_id = graph_def.start_node
        
        # Safety break for infinite loops
        steps_count = 0
        max_steps = 20 

        while current_node_id and steps_count < max_steps:
            steps_count += 1
            
            # 1. Find the current node definition
            node_def = next((n for n in graph_def.nodes if n.id == current_node_id), None)
            if not node_def:
                break

            # 2. Execute the Node Function 
            func = self.function_registry.get(node_def.function_name)
            if func:
                state.execution_log.append(f"Executing {node_def.id} (Func: {node_def.function_name})")
                
                # Check if async or sync function
                if asyncio.iscoroutinefunction(func):
                    updates = await func(state.data)
                else:
                    updates = func(state.data)
                
                # Update shared state 
                if updates:
                    state.data.update(updates)
            else:
                state.execution_log.append(f"Error: Function {node_def.function_name} not found")

            # 3. Determine Next Node (Traversal & Branching) [cite: 19, 20]
            next_node_id = None
            
            # Get all edges starting from current node
            possible_edges = [e for e in graph_def.edges if e.source == current_node_id]
            
            for edge in possible_edges:
                if edge.condition:
                    # Evaluate condition
                    condition_func = self.function_registry.get(edge.condition)
                    if condition_func and condition_func(state.data):
                        next_node_id = edge.target
                        state.execution_log.append(f"Condition {edge.condition} met -> Transition to {edge.target}")
                        break
                else:
                    # Unconditional transition
                    next_node_id = edge.target
                    break
            
            current_node_id = next_node_id

        self.runs[run_id] = state # Final update