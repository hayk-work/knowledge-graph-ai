# LangGraph Overview

LangGraph is a library for building stateful, multi-step AI workflows as graphs. It extends
LangChain with explicit nodes, edges, and shared state—ideal for agents, RAG pipelines, and
any logic that needs conditional routing or cycles.

## Why Graphs?

Linear chains break down when you need:

- Conditional branches (e.g. relevant docs vs. web search fallback)
- Loops (retry retrieval, refine an answer)
- Multiple actors or steps sharing state
- Human-in-the-loop checkpoints

LangGraph models these as a directed graph where each node reads and updates state.

## Core Building Blocks

### State

State is a typed dictionary (often a `TypedDict`) holding fields like `question`, `context`,
`answer`, or `messages`. Every node receives the current state and returns partial updates.

### Nodes

A node is a function that performs one unit of work: rewrite a query, retrieve documents,
grade relevance, call an LLM, or invoke a tool.

### Edges

Edges connect nodes. Normal edges always go to the next node. Conditional edges route based
on a function’s return value—for example, `"relevant"` → generate, `"irrelevant"` → search web.

### Compilation

You build a `StateGraph`, add nodes and edges, then `compile()` to get a runnable graph.
The compiled graph supports `.invoke()`, streaming, and LangSmith tracing.

## Example RAG Flow

```text
START → rewrite_query → retrieve → grade_documents
                                      ├─ relevant → generate → END
                                      └─ irrelevant → web_search → generate → END
```

## Persistence and Memory

LangGraph supports checkpointing so conversations can resume across requests. Thread IDs tie
runs to a user session. This enables durable agents and long-running workflows.

## LangGraph vs LangChain Chains

| LangChain chains | LangGraph |
|------------------|-----------|
| Mostly linear | Branching and cycles |
| Implicit flow | Explicit graph structure |
| Simple pipelines | Agents and complex orchestration |

LangGraph is the recommended approach for production agentic systems built on LangChain
components.
