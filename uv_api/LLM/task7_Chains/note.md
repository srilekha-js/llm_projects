**What is Chains?**
**The output of one LLM response becomes the input of another LLM. This is called chaining.**
**The output of one step becomes the input of the next step**

**Single LLM call**
```
    User Text
        ↓
       LLM
        ↓
    Summary
```

user text given to llm and response the summary of it 
summary = llm.invoke(
    "Summarize this article"
)

**Multi-Step Chain**

Instead of stopping at the summary: we are going to have multiple steps 
summary = llm.invoke(
    "Summarize this article" {article}
)
keywords = llm.invoke(
    "Extract keywords from this summary: {summary}"
)
title = llm.invoke(
    "Generate a title for this summary: {summary}"
)

User Text
    ↓
Summarizer
    ↓
Keyword Extractor
    ↓
Title Generator

example:
summary = summarize_llm.invoke(article)

keywords = keyword_llm.invoke(summary)

title = title_llm.invoke(summary)

This is a chain

Chain process
Article
   ↓
Summarizer
   ↓
Summary
   ↓
Keyword Extractor
   ↓
Keywords
   ↓
Title Generator
   ↓
Final Result
"""

this is not an agent, this is just a chain process 
