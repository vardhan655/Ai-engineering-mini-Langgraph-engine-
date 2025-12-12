import random

# --- Node Functions  ---

def extract_functions(state: dict):
    # Simulating code extraction
    return {"functions": ["func_a", "func_b"], "quality_score": 0, "reviews_count": 0}

def check_complexity(state: dict):
    # Simulating complexity check
    # In a real app, this might calculate Cyclomatic complexity
    current_score = state.get("quality_score", 0)
    return {"complexity_metric": "low", "quality_score": current_score + 10}

def detect_basic_issues(state: dict):
    # Simulating finding issues
    issues = ["unused_import"] if state.get("quality_score") < 50 else []
    return {"issues": issues}

def suggest_improvements(state: dict):
    # This node attempts to 'fix' the code, increasing score
    current_score = state.get("quality_score", 0)
    new_score = current_score + 20
    # Increment loop counter to show progress
    count = state.get("reviews_count", 0) + 1
    return {"quality_score": new_score, "reviews_count": count, "latest_suggestion": "Refactor func_b"}

# --- Condition Functions (for Branching/Looping) [cite: 20, 21] ---

def needs_improvement(state: dict) -> bool:
    # Loop condition: continue if score is low
    return state.get("quality_score", 0) < 80

def passes_quality(state: dict) -> bool:
    # Exit condition
    return state.get("quality_score", 0) >= 80

def register_all_tools(engine):
    engine.register_function("extract_functions", extract_functions)
    engine.register_function("check_complexity", check_complexity)
    engine.register_function("detect_basic_issues", detect_basic_issues)
    engine.register_function("suggest_improvements", suggest_improvements)
    engine.register_function("needs_improvement", needs_improvement)
    engine.register_function("passes_quality", passes_quality)