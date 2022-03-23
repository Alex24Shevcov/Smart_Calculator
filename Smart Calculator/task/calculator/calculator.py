# write your code here
import re
from collections import deque

dict_of_variables = dict()


def is_comand(elem) -> bool:
    if elem == "/exit":
        print("Bye!")
        exit(0)
    elif elem == "/help":
        print("The program calculates the sum of numbers")
        return True
    elif elem[0] == "/":
        raise Exception("Unknown command")


def is_correct_expression(arr: tuple()) -> bool:
    lol_ok = False
    if len(arr) == 0:
        lol_ok = True
    else:
        for i in arr:
            if re.search("^[-+]+$", i):
                lol_ok = True
            elif re.search("^\d+$", i):
                lol_ok = True
            elif re.search("^[A-z]+$", i):
                lol_ok = True
            elif re.search("^=$", i):
                lol_ok = True
            elif re.search("^[A-z]*\d+[A-z]*$", i):
                lol_ok = False
                print("Invalid identifier")
                break

            elif re.search("^[A-z]+ *=? *[A-z]*$", i):
                variable = i.split()[-1]
                for key in dict_of_variables.keys():
                    if key == variable:
                        dict_of_variables[key] = dict_of_variables[variable]
                        lol_ok = True
                        break

                if lol_ok == False:
                    print("Unknown variable")


            elif re.search("^[A-z]+ *= *\d+$", i):
                lol_ok = True

            elif re.search("^[A-z]*\d+[A-z]* *=? *[A-z]*\d+[A-z]*$", i):
                print("Invalid identifier")
                lol_ok = False
                break

            else:
                lol_ok = False
                break

    return lol_ok


def from_expr_to_arr(expression: str) -> list():
    if is_invalid_expression(expression):
        raise Exception("Invalid expression")

    for i in re.findall("[-+]+", expression):
        if len(i) % 2 == 0:
            expression = expression.replace(i, "+", 1)
        elif re.search("-+", i):
            expression = expression.replace(i, "-", 1)
        else:
            expression = expression.replace(i, "+", 1)

    arr = re.split("[-+*/^)(]", expression)
    index_insert = 1
    for i in expression:
        if re.search("[-+*/)(]", i):
            arr.insert(index_insert, i)
            index_insert += 2

    return [i.strip() for i in arr if i != '' and i != " "]


def is_invalid_expression(expression: str) -> bool:
    if re.search(".+[*/^]{2,}.+", expression):
        return True

    my_tmp_stack = deque()
    for i in expression:
        try:
            if i == "(":
                my_tmp_stack.append(i)
            elif i == ")":
                my_tmp_stack.pop()
        except Exception:
            return True

    if len(my_tmp_stack) > 0:
        return True

    return False


def is_var_or_num_or_oper_or_brack(elem):
    if re.search("^[A-z]+$", elem):
        for key in dict_of_variables.keys():
            if key == elem:
                return dict_of_variables[key]
    elif re.search("^\d+$", elem):
        return int(elem)
    elif re.search("^[-+*/)(]+$", elem):
        return elem
    print("Unknown variable")


def calculating_the_result(arr_expr: list):
    dict_operations_priority = {"+": 1, "-": 1, "*": 2, "/": 2, "^": 3}
    my_stack_oper_and_brac = deque()
    arr_postfix = []

    for i in range(len(arr_expr)):
        item = is_var_or_num_or_oper_or_brack(arr_expr[i])
        if item is None:
            return False
        elif isinstance(item, int):
            arr_postfix.append(item)
        elif len(my_stack_oper_and_brac) == 0 \
                or my_stack_oper_and_brac[-1] == "(" or item == "(":
            my_stack_oper_and_brac.append(item)
        elif item == ")":
            while my_stack_oper_and_brac[-1] != "(":
                arr_postfix.append(my_stack_oper_and_brac.pop())
            my_stack_oper_and_brac.pop()

        elif dict_operations_priority[my_stack_oper_and_brac[-1]] < dict_operations_priority[item]:
            my_stack_oper_and_brac.append(item)
        elif dict_operations_priority[my_stack_oper_and_brac[-1]] >= dict_operations_priority[item]:
            while len(my_stack_oper_and_brac) > 0 \
                    and dict_operations_priority[my_stack_oper_and_brac[-1]] >= dict_operations_priority[item]:
                if my_stack_oper_and_brac[-1] == "(":
                    break

                try:
                    arr_postfix.append(my_stack_oper_and_brac.pop())
                except IndexError:
                    break
            my_stack_oper_and_brac.append(item)

    while len(my_stack_oper_and_brac) > 0:
        arr_postfix.append(my_stack_oper_and_brac.pop())

    i = 0
    my_stack_unswer = deque()

    while i < len(arr_postfix):
        if isinstance(arr_postfix[i], int):
            my_stack_unswer.append(arr_postfix[i])
        else:
            first_num = my_stack_unswer.pop()
            second_num = my_stack_unswer.pop()
            if arr_postfix[i] == "+":
                my_stack_unswer.append(second_num + first_num)
            elif arr_postfix[i] == "-":
                my_stack_unswer.append(second_num - first_num)
            elif arr_postfix[i] == "*":
                my_stack_unswer.append(second_num * first_num)
            elif arr_postfix[i] == "/":
                my_stack_unswer.append(second_num // first_num)
        i += 1

    return my_stack_unswer[-1]


def create_variable(arr):
    for i in range(len(arr)):
        if arr[i] == "=":
            if re.search("^[A-z]+$", arr[i + 1]):
                try:
                    dict_of_variables[arr[i - 1]] = int(dict_of_variables[arr[i + 1]])
                except KeyError:
                    print("Unknown variable")
            elif re.search("^-?\d+$", arr[i + 1]):
                dict_of_variables[arr[i - 1]] = int(arr[i + 1])

            break


def main():
    while True:
        user_input = input().strip()

        if re.search("^.*=.*=.*$", user_input):
            print("Invalid assignment")
            continue

        elif re.search("^[A-z\d]* *= *(\d+|[A-z]+)$", user_input):
            arr_nums_and_sings = [i.strip() for i in user_input.split("=")]
            arr_nums_and_sings.insert(1, "=")
            arr_nums_and_sings = tuple(arr_nums_and_sings)
            if is_correct_expression(arr_nums_and_sings):
                create_variable(arr_nums_and_sings)
            else:
                continue
        else:
            try:

                if user_input == "":
                    continue

                elif is_comand(user_input):
                    continue

                arr_nums_and_sings = from_expr_to_arr(user_input)
                print(calculating_the_result(arr_nums_and_sings))
            except Exception as e:
                print(e)
                continue


if __name__ == "__main__":
    main()
