from langchain_core.tools import tool

# @tool
# def calculator_error(x: str) -> str:

#     try:
#         result = eval(x)
#         return str(result)
#     except Exception as e:
#         return f"Error: {e}"

# we didnt give description so it throws the error 
#     raise ValueError(msg)
# ValueError: Function must have a docstring if description not provided.

from langchain_core.tools import tool

@tool
def calculator(x: str) -> str:
    """Perform basic mathematical calculations."""
    try:
        result = eval(x)
        return str(result)
    except Exception as e:
        return f"Error: {e}"
    

# from langchain_core.tools import tool


# @tool
# def calculator(expression: str) -> str:
#     """
#     Calculate mathematical expressions.

#     Examples:
#     - 5+5
#     - 10*20
#     - 100/4
#     """

#     try:
#         result = eval(expression)
#         return str(result)

#     except Exception as e:
#         return f"Error: {e}"