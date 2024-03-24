def terminal(text):
    return text

def math(num1, num2, action, result=True):
    if action == "plus":
        if result == True:
            print(num1 + num2)
        else:
            return num1 + num2
    if action == "minus":
        if result == True:
            print(num1 - num2)
        else:
            return num1 - num2
    if action == "divide":
        if result == True:
            print(num1 / num2)
        else:
            return num1 / num2
    if action == "multipicate":
        if result == True:
            print(num1 * num2)
        else:
            return num1 * num2
