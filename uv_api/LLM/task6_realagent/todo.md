
Tools:
calculator
text summarizer
search mock tool

Agent setup (conceptual next step):
LLM decides which tool to use
executes tool
returns final answer


Good plan—using Ollama locally is one of the best ways to learn GenAI + Agentic AI without worrying about API limits.

I’ll structure this like a **step-by-step learning roadmap + repo tasks**, so you can implement one concept at a time in your `app.py` or split files.

---

# 🧠 Phase 1 — Basic LLM usage (DONE by you)

You already did:

1. Created LLM instance (Ollama)
2. Ran 1 prompt in Python

---

# 🧱 Phase 2 — Prompt Engineering Foundation

## ✅ Task 3: Prompt Template System (IMPORTANT)

### Goal:

Stop hardcoding prompts. Use reusable templates.

### What to build:

Create `prompts.py`

```python
from langchain_core.prompts import PromptTemplate

summary_prompt = PromptTemplate(
    input_variables=["text"],
    template="""
You are a helpful assistant.
Summarize the following text in simple bullet points:

Text:
{text}

Summary:
"""
)
```

### In `app.py`

```python
from prompts import summary_prompt

prompt = summary_prompt.format(text="Long article here...")
response = llm.invoke(prompt)
print(response)
```

✔ Learnings:

* Prompt structuring
* Reusability
* Separation of logic

---

# 🧾 Phase 3 — Text Summarizer App (DONE + IMPROVE)

## Upgrade Task:

Turn it into a function-based mini app:

```python
def summarize(text):
    prompt = summary_prompt.format(text=text)
    return llm.invoke(prompt)
```

## Add:

* file input (`.txt`)
* or user input loop

---

# 🧠 Phase 4 — Structured Output (VERY IMPORTANT)

## Task 4: JSON Output Generator

### Goal:

Force LLM to output structured data

```python
json_prompt = PromptTemplate(
    input_variables=["text"],
    template="""
Extract key information from the text below.

Return ONLY valid JSON with:
- title
- summary
- key_points (list)

Text:
{text}
"""
)
```

✔ Learn:

* structured prompting
* foundation for agents + APIs

---

# 🔧 Phase 5 — Tool Calling (First Agent Step)

## Task 5: Create ONE tool

Example tool: calculator

```python
def calculator(expression: str):
    return eval(expression)
```

---

## Now connect LLM → tool manually

### Step 1: detect intent

```python
def decide_tool(user_input):
    if "calculate" in user_input:
        return "calculator"
    return "llm"
```

### Step 2: routing logic

```python
def run_agent(user_input):
    tool = decide_tool(user_input)

    if tool == "calculator":
        expr = user_input.replace("calculate", "")
        return calculator(expr)
    else:
        return llm.invoke(user_input)
```

✔ Learn:

* very first “agent-like behavior”
* routing logic

---

# 🤖 Phase 6 — REAL Agent Framework (LangChain style)

## Task 6: Use Tool abstraction

You move to:

* Tools
* Agent executor
* tool calling LLM

### Tools:

* calculator
* text summarizer
* search mock tool

---

## Example tool format:

```python
from langchain_core.tools import tool

@tool
def calculator(x: str) -> str:
    return str(eval(x))
```

---

## Agent setup (conceptual next step):

* LLM decides which tool to use
* executes tool
* returns final answer

---

# 🧠 Phase 7 — Memory (VERY IMPORTANT for Agentic AI)

## Task 7: Chat memory

Build:

* conversation history buffer

Example:

```python
memory = []
```

Add:

* last 5 messages context

✔ Learn:

* contextual agents
* chat continuity

---

# 🔍 Phase 8 — RAG (Retrieval Augmented Generation)

## Task 8: Mini knowledge base

Create:

* `docs.txt`
* embed + search (later FAISS or Chroma)

Flow:
User question → retrieve relevant text → send to LLM

✔ Learn:

* enterprise GenAI systems
* real-world AI apps

---

# 🧩 Phase 9 — Multi-Agent System (Advanced)

## Task 9:

Create 2 agents:

* Research agent
* Summary agent

Flow:
User → Agent 1 → Agent 2 → Final answer

✔ Learn:

* orchestration
* agent collaboration

---

# 🚀 Phase 10 — Final Project (Capstone)

## Build:

👉 “AI Assistant CLI”

Features:

* summarizer
* calculator tool
* document Q&A (RAG)
* memory chat
* tool routing agent

---

# 📁 Suggested Repo Structure

```
project/
│── app.py
│── llm.py
│── prompts.py
│── tools.py
│── agents.py
│── memory.py
│── rag.py
│── data/
│     └── docs.txt
```

---

# 🧭 Your Next Step (do this now)

Since you already completed step 1–2:

👉 Next task for you:

### ✔ TASK:

1. Create `prompts.py`
2. Add **summarizer prompt template**
3. Modify your app.py to use it

---

When you finish that, tell me:

>“done prompts”

Then I’ll give you the **next step: Tool creation + first real agent routing system (calculator agent)**.
