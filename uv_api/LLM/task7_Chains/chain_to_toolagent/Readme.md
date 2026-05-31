## Project Overview: Multi-Task Text Analysis Agent
This project implements an intelligent, tool-calling AI agent using LangChain Ollama and LangGraph. The agent automatically analyzes input text to summarize content, extract keywords, or generate titles based on natural language user requests.
Instead of writing complex routing logic, the system leverages a ReAct (Reasoning and Acting) agent framework to dynamically select and execute the appropriate text-processing function.
------------------------------
## 🚀 Quick Start Guide## Prerequisites

* Python: Version 3.10 or higher.
* Ollama: Installed and running locally.
* LLM Model: llama3.2 pulled locally via Ollama (ollama run llama3.2).

## Installation
Install the required dependencies using pip:

pip install langchain-ollama langgraph

## Running the Application
Save the core logic into a file named app.py and run it:

python app.py

------------------------------
## 🛠️ System Architecture
The architecture decouples the primary orchestration engine from the underlying specialized task logic.

                  ┌───────────────────────┐
                  │   User Text Request   │
                  └───────────┬───────────┘
                              │
                              ▼
                ┌───────────────────────────┐
                │   LangGraph ReAct Agent   │
                └─────────────┬─────────────┘
                              │
         ┌────────────────────┼────────────────────┐
         │ (Auto-Route based on tool descriptions) │
         ▼                    ▼                    ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│ Tool: Summarize │  │ Tool: Keywords  │  │  Tool: Title    │
└────────┬────────┘  └────────┬────────┘  └────────┬────────┘
         │                    │                    │
         ▼                    ▼                    ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│ Summary Prompt  │  │ Keyword Prompt  │  │  Title Prompt   │
└────────┬────────┘  └────────┬────────┘  └────────┬────────┘
         └────────────────────┼────────────────────┘
                              │
                              ▼
                  ┌───────────────────────┐
                  │ Local Llama 3.2 Model │
                  └───────────────────────┘

------------------------------
## 📘 Developer Documentation## 1. Code Structure

from langchain_ollama.chat_models import ChatOllamafrom langchain.tools import toolfrom langgraph.prebuilt import create_react_agent
# ==========================================# 1. MODEL INITIALIZATION# ==========================================def llm_creation():
    """Initializes the local ChatOllama instance with standard configs."""
    return ChatOllama(
        model="llama3.2",
        temperature=0,       # Deterministic outputs for structured tasks
        max_tokens=1000,
    )
llm = llm_creation()
# ==========================================# 2. ISOLATED TASK PROMPTS# ==========================================summary_prompt = """You are a helpful assistant for summarizing text.
Summarize the text concisely. Do not include opinions.
TEXT: {text}
SUMMARY:"""
keyword_extraction_prompt = """You are a helpful assistant for extracting keywords.
Extract the main keywords from the text.
TEXT: {text}
KEYWORDS:"""
title_generation_prompt = """You are a helpful assistant for generating a title.
Generate a concise title between 5 to 10 words.
TEXT: {text}
TITLE:"""
# ==========================================# 3. AGENT TOOLS DEFINITION# ==========================================
@tool("summarize_text")def summarize_text(text: str) -> str:
    """Summarize the given text or article. Use this when the user asks for a summary."""
    prompt = summary_prompt.format(text=text)
    return llm.invoke(prompt).content

@tool("extract_keywords")def extract_keywords(text: str) -> str:
    """Extract keywords from the given text. Use this when the user asks for keywords or tags."""
    prompt = keyword_extraction_prompt.format(text=text)
    return llm.invoke(prompt).content

@tool("generate_title")def generate_title(text: str) -> str:
    """Generate a title for the given text. Use this when the user wants a heading or headline."""
    prompt = title_generation_prompt.format(text=text)
    return llm.invoke(prompt).content
tools = [summarize_text, extract_keywords, generate_title]
# ==========================================# 4. AGENT CREATION & INVOCATION# ==========================================# The prebuilt agent automatically builds system instructions from tool descriptions.agent = create_react_agent(model=llm, tools=tools)
def run_agent(user_query: str):
    response = agent.invoke({"messages": [{"role": "user", "content": user_query}]})
    return response["messages"][-1].content
# Example Executionif __name__ == "__main__":
    sample_text = "The COVID-19 pandemic has had a profound impact on global health..."
    query = f"Please summarize this article and extract keywords: {sample_text}"
    
    print("Result:\n", run_agent(query))

## 2. Core Concepts for Developers## The Power of Docstrings
The text inside the """triple quotes""" right below the tool function definition is compiled directly into the LLM's system instructions. If your agent fails to pick a tool accurately, clarify the text inside the docstring to explicitly describe the triggers.
## Zero-Prompt Orchestration
You do not need to build a master orchestration prompt template. create_react_agent handles state management, structural validation, loop tracking, and execution logic automatically under the hood.
## Input/Output State Schema
The modern LangGraph agent tracks its operational runtime via a list of standard message objects:

* Input Interface: Must accept a dictionary with a "messages" list containing standard user roles.
* Output Interface: Access the final tool output message safely using list indexing: response["messages"][-1].content.

------------------------------
