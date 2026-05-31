from langchain_ollama.chat_models import ChatOllama

def llm_creation():
    # Create a ChatOllama instance
    llm = ChatOllama(
        model="llama3.2",
        temperature=0,
        max_tokens=1000,
    )
    return llm
