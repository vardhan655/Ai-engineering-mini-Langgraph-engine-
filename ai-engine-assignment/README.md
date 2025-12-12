# How to run 
###  Installation
Clone the repository and install the dependencies:

# Navigate to the project root
cd ai-engine-assignment

# (Optional) Create a virtual environment
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
3. Start the Server
Run the application using Uvicorn from the root directory:

uvicorn app.main:app --reload

The server will start at http://127.0.0.1:8000.

### Testing the API
Open your browser and navigate to the interactive documentation: 
 https://www.google.com/search?q=http://127.0.0.1:8000/docs

# Mini Workflow Engine

A backend system design for a graph-based workflow engine. This application allows users to define DAGs (Directed Acyclic Graphs) and cyclic graphs (loops) to orchestrate complex tasks dynamically.

Built with **FastAPI**, **Python 3**, and **Pydantic**.
##  Features

* **Graph-Based Execution**: Nodes are functions, edges are transitions.
* **Cycles & Loops**: Supports looping workflows based on dynamic state conditions (e.g., "Loop until quality score > 80").
* **Async Execution**: The engine runs workflows asynchronously.
* **Type Safety**: Full Pydantic validation for inputs, outputs, and state management.
* **Extensible Tool Registry**: Functions are registered by name, keeping the API JSON-serializable.

##  Project Structure

```text
/
├── app/
│   ├── main.py          # FastAPI entry point & API routes
│   ├── engine.py        # Core WorkflowEngine logic (traversal, loops)
│   ├── schemas.py       # Pydantic data models
│   └── workflow_impl.py # Implementation of the "Code Review" agent functions
├── requirements.txt     # Project dependencies
└── README.md            # Documentation

