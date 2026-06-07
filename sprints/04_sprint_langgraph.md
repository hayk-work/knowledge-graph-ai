# Sprint 4 — LangGraph Workflow

## Goal
Replace linear pipeline with LangGraph.

---

## Graph Flow

START
  ↓
Retrieve
  ↓
Generate
  ↓
END

---

## Tasks

### 1. Create state

```python
class State(TypedDict):
    question: str
    context: list
    answer: str
```

### 2. Create nodes
-  retrieve_node()
-  generate_node()

### 3. Build graph
-  StateGraph
-  add nodes
-  compile graph

### Done when
-  graph executes end-to-end
-  output returned from graph