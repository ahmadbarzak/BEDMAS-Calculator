from sys import exit

# Whenever is_number(x) exists, it is checking to see if x is a number.


def is_number(item):
    try:
        float(item)
        return True
    except ValueError:
        return False


def set_up_list():

    # First we get the string and delete any spaces

    string = input("Calculation: ")
    string = string.replace(" ", "")

    # Then we check if there are any invalid characters in the string

    for item in string:
        if item not in "0123456789+-*/.()":
            print("Invalid Character: " + item)
            exit()

    # We then create a list that adds each character to the list allowing us to concatenate numbers

    expression_list = []
    for item in string:
        expression_list.append(item)
    count = 0

    # We concatenate the numbers that are directly next to each other and test for other criteria
    # e.g decimal places and parenthesis locations

    while count < len(expression_list) - 1:
        if is_number(expression_list[count]) and expression_list[count + 1] == "(":
            print("Program does not accept parenthesis directly after number, must have operator in between.")
            exit()

        if is_number(expression_list[count]) and is_number(expression_list[count + 1]):
            expression_list[count] += expression_list[count + 1]
            del expression_list[count + 1]
        elif is_number(expression_list[count]) and expression_list[count + 1] == ".":
            try:
                expression_list[count + 2]
            except IndexError:
                print("Your formatting is due to an Index Error.")
                exit()
            if is_number(expression_list[count + 2]):
                expression_list[count] += expression_list[count+1] + expression_list[count+2]
                del expression_list[count + 2]
                del expression_list[count + 1]
        else:
            count += 1

    return expression_list


def perform_operation(n1, operand, n2):
    if operand == "+":
        return str(float(n1) + float(n2))
    elif operand == "-":
        return str(float(n1) - float(n2))
    elif operand == "*":
        return str(float(n1) * float(n2))
    elif operand == "/":
        try:
            n = str(float(n1)/float(n2))
            return n
        except ZeroDivisionError:
            print("You tried to divide by 0.")
            print("Just for that I am going to terminate myself")
            exit()


def expression_evaluator(expression):
    emergency_count = 0

    p = "()"

    # Expressions with a length of 1 is already the answer

    while len(expression) != 1:

        # check for parenthesis and eliminate parenthesis surrounding only one number

        count = 0
        while count < len(expression) - 1:
            if expression[count] == "(":
                if expression[count + 2] == ")":
                    del expression[count + 2]
                    del expression[count]
            count += 1

        # look for Multiply and Divide operators and perform any available operations

        count = 0
        while count < len(expression) - 1:
            if expression[count] in "*/" and not (expression[count + 1] in p or expression[count - 1] in p):
                expression[count - 1] = perform_operation(expression[count - 1], expression[count], expression[count + 1])
                del expression[count + 1]
                del expression[count]
            count += 1

        # look for Addition and Subtraction operators and perform any available operations

        count = 0
        while count < len(expression) - 1:
            if expression[count] in "+-" and not (expression[count + 1] in p or expression[count - 1] in p):
                expression[count - 1] = perform_operation(expression[count - 1], expression[count], expression[count + 1])
                del expression[count + 1]
                del expression[count]
            count += 1

        # Loop through until one number is left, the expression is evaluated.
        # If unexpected infinite loop occurs, emergency count will detect and exit the operation

            emergency_count += 1
        if emergency_count >= 1000:
            print("Operation was too long or was bugged")
            exit()

    return expression[0]


math_expression = set_up_list()

# what do we do when we have the expression?
# we look for closed (   ) brackets with no parenthesis inside them
# finds the first ( and saves the index number
# if there's no ( then evaluate the whole expression
# if you find it and you have the index number, scan through the rest until you find the first )
# and save that index number
# if you find another ( before you find the ), update the index number
# we evaluate the expression in the parenthesis by plugging it into expression_evaluator
# we replace the (    ) with the evaluated number
# this process loops
# in the instance that we can't find any closed brackets,
# we evaluate this expression in the evaluator, this is our answer

count = 0

while len(math_expression) != 1 and count < len(math_expression) - 1:

    if math_expression[count] == "(":

        first_count = count

    if math_expression[count] == ")":

        second_count = count

        expression = math_expression[first_count:second_count + 1]
        number = expression_evaluator(expression)
        math_expression[first_count] = number
        del math_expression[first_count + 1: second_count + 1]
        count = -1

    count += 1

    # evaluates the closed parenthesis

answer = expression_evaluator(math_expression)
print(float(answer))

