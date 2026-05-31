#how to store chat history for chatbots


chathistory = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "My name is John"},
    {"role": "assistant", "content": "Nice to meet you"},
    {"role": "user", "content": "What is my name?"}
]
# This is called chathistory, which is a list of messages exchanged between the user and the assistant. Each message is represented as a dictionary with a "role" (system, user, or assistant) and "content" (the actual message). This chat history can be used to provide context for the [llm] assistant to generate more relevant responses based on the previous interactions.


chat_history = []

import json

from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.messages import SystemMessage
from llm import llm_creation

llm = llm_creation()

messages = []


while True:
    user_input = input("User: ")
    if user_input.lower() == "exit" or user_input.lower() == "quit" or user_input.lower() == "bye" or user_input.lower() == "q":
        print("Goodbye!")
        break

    messages.append(HumanMessage(content=user_input))

    # response = llm.invoke(messages)
    # to store only last 10 messages in the chat history
    if len(messages) > 10:
        messages = messages[-10:]
    response = llm.invoke(messages)
    
    messages.append(AIMessage(content=response.content))

    print("AI:", response.content)

    # how to store these chat history in a file or database for future reference and analysis. This can be useful for improving the chatbot's performance, understanding user behavior, and providing personalized experiences.
    
    with open("chat_history.json", "w") as f:
        json.dump(messages, f, indent=4)