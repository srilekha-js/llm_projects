# from langchain_ollama import ChatOllama
from langchain_ollama.chat_models import ChatOllama

# Create a ChatOllama instance
llm = ChatOllama(
    model="llama3.2",
    temperature=0,
    max_tokens=1000,
)

# Invoke the model with a prompt
response = llm.invoke("What is the capital of France?")
print(response)
# print(response.choices[0].message)