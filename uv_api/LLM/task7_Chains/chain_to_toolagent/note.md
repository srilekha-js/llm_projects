
When you set:

```python
@tool("summarize_text", return_direct=True)
def summarize_text(text: str):
    ...
```

you're telling the agent:

> "If this tool is called, stop the agent loop and return the tool's output immediately."

---

### Without `return_direct=True`

Agent flow:

```text
User
 ↓
Agent
 ↓
Call summarize_text
 ↓
Tool Output
 ↓
Agent observes output
 ↓
Agent thinks again
 ↓
May call another tool
 ↓
Final Answer
```

Example:

```text
User: Analyze this article
```

Agent:

```text
Thought: Need summary
Action: summarize_text
```

Tool:

```text
COVID-19 impacted health...
```

Agent:

```text
Thought: Need keywords too
Action: extract_keywords
```

Tool:

```text
COVID-19, vaccines...
```

Agent:

```text
Final Answer...
```

---

### With `return_direct=True`

Agent flow:

```text
User
 ↓
Agent
 ↓
Call summarize_text
 ↓
Tool Output
 ↓
RETURN TO USER
```

No further reasoning.

No additional tools.

No final LLM response.

---

Example:

```python
@tool(return_direct=True)
def calculator(x: str):
    return str(eval(x))
```

User:

```text
What is 5 * 10?
```

Agent:

```text
Action: calculator
```

Tool:

```text
50
```

Returned directly:

```text
50
```

Instead of:

```text
The answer is 50.
```

---

### Think of it as

```python
if tool.return_direct:
    return tool_output
else:
    observation = tool_output
    continue_agent_loop()
```

---

### For your article workflow

If you do:

```python
@tool(return_direct=True)
def summarize_text(...):
```

then:

```text
User:
Analyze this article and give keywords and title
```

Agent:

```text
Calls summarize_text
```

Tool:

```text
Summary...
```

Agent stops immediately.

It never reaches:

```text
extract_keywords()
generate_title()
```

So for multi-step agent workflows, **don't use `return_direct=True`** unless you intentionally want that tool's result to be the final answer.

A common use case is a calculator tool:

```python
@tool(return_direct=True)
def calculator(x: str):
    ...
```

because the raw result (`157320`) is often all you need. For tools that are intermediate steps in a larger workflow, leave `return_direct=False` (the default).


CHAINING VS TOOLS 
Yes. What you've written is **chaining**, not an agent.

Your code is essentially:

```text
Article
   ↓
Summarize
   ↓
Extract Keywords
   ↓
Generate Title
```

The flow is fixed by you, the programmer.

```python
summary = llm.invoke(summary_prompt)
keywords = llm.invoke(keyword_prompt)
title = llm.invoke(title_prompt)
```

The LLM has no choice. It simply executes the steps you coded.

---

## Chain vs Agent

### Chain

You decide the workflow.

```text
User Input
    ↓
Step 1: Summarize
    ↓
Step 2: Extract Keywords
    ↓
Step 3: Generate Title
```

Code:

```python
summary = summarize(article)
keywords = extract_keywords(summary)
title = generate_title(summary)
```

Characteristics:

* Fixed sequence
* Deterministic flow
* No decision making
* Faster
* Easier to debug

---

### Agent

The LLM decides the workflow.

User:

```text
Analyze this article
```

Agent thinks:

```text
Should I summarize first?
Yes.

Need keywords?
Yes.

Need title?
Yes.
```

Another user:

```text
Just give me keywords.
```

Agent thinks:

```text
No need to summarize.
Call keyword tool directly.
```

The workflow changes dynamically.

---

## Your chain converted into tools

```python
@tool
def summarize(text: str) -> str:
    """Summarize the given article."""
    ...

@tool
def extract_keywords(text: str) -> str:
    """Extract keywords from text."""
    ...

@tool
def generate_title(text: str) -> str:
    """Generate a title from text."""
    ...
```

Register:

```python
tools = [
    summarize,
    extract_keywords,
    generate_title
]
```

Create agent:

```python
agent = create_agent(
    model=llm,
    tools=tools
)
```

---

User asks:

```text
Analyze this article and give keywords and title.
```

Possible agent trace:

```text
Thought:
Need summary first.

Action:
summarize(article)

Observation:
COVID-19 impacted health, economy...

Thought:
Need keywords.

Action:
extract_keywords(summary)

Observation:
COVID-19, pandemic, vaccines...

Thought:
Need title.

Action:
generate_title(summary)

Observation:
Global Impact of COVID-19

Final Answer:
Summary...
Keywords...
Title...
```

Notice:

**You didn't write the sequence.**

The agent decided it.

---

## What you currently have

```python
article
 ↓
summary
 ↓
keywords
 ↓
title
```

This is:

```text
LLM Chain
```

or in modern LangChain:

```python
prompt | llm
```

and multiple chains connected together.

---

## What an Agent would look like

```python
User Query
    ↓
Agent
    ↓
Chooses Tool
    ↓
Executes Tool
    ↓
Observes Result
    ↓
Chooses Next Tool
    ↓
Final Answer
```

The key difference:

| Chain               | Agent                      |
| ------------------- | -------------------------- |
| You define workflow | LLM defines workflow       |
| Fixed steps         | Dynamic steps              |
| No reasoning loop   | Think → Act → Observe loop |
| Predictable         | Flexible                   |

Your current article summarizer is a perfect example of a **chain**. To make it an **agent**, you would convert each operation (summarize, keyword extraction, title generation) into tools and let the LLM decide which tools to call and in what order.


AGENTS WORK

agent will decide which tool to select and execture based on the user question
if user question contains summarize word then it route to summarize tool

if user question contains extract keywords then it route to extract_keywords tool
if user question contains generate title then it route to generate_title tool

similarly for all the applications

how to deploy using docker
with fast api backend

