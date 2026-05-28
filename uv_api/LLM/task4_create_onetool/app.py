from calc import calculator

from llm import llm_creation

def decide_tool(user_input):
    if "calculate" in user_input:
        return "calculator"
    else:
        return "llm"
    
def run_agent(user_input):
    tool = decide_tool(user_input) #calculator or llm
    if tool == "calculator":
        user_input = user_input.replace("calculate", "").strip() #remove the word "calculate" from the user input
        return calculator(user_input) #eval
    else:
        llm = llm_creation()
        return llm.invoke(user_input) #call the llm with the user input
    
print(run_agent("calculate 2 + 3 * 4")) # Output: 14
print(run_agent("calculate 10/0")) # tool output: Error: division by zero

print(run_agent("help me study statistics")) # ;llm output