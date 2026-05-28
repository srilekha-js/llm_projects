def calculator(expression):
    try:
        result = eval(expression)
        return result   
    except Exception as e:
        return f"Error: {str(e)}"
    

#testing the calculator function    
    
# print(calculator("2 + 3 * 4"))  # Output: 14
# print(calculator("10 / 0"))       # Output: Error: division by zero


# print(eval("2 + 3 * 4"))  # Output: 14

# print(eval("10 / 0"))       # Output: Error: division by zero