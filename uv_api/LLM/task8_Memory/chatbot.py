# Task 8: Chatbot

# Conversation:

# User: My name is John

# AI: Nice to meet you

# User: What is my name?
# Learn
# Chat history
# Context


#create a chatbot
from llm import llm_creation

llm = llm_creation()

def run_chatbot(greetings):
    print("AI:", greetings)
    while True:
        user_input = input("User: ")
        # print("User:", user_input)
        if user_input.lower() == "exit" or user_input.lower() == "quit" or user_input.lower() == "bye" or user_input.lower() == "q":
            print("Goodbye!")
            break
        response = llm.invoke(user_input)
        print("AI:", response.content)

if __name__ == "__main__":
    run_chatbot("Good Morning!!! I am doing great")
