with open("compiler/compiled_code.txt") as file:
    commands = [line.strip() for line in file.readlines()]
variables = {}

def get_var(var):
    if var.isdigit():
        return int(var)
    try:
        return float(var)
    except ValueError:
        return var

def check_var(var):
    if isinstance(var, (int, float)):
        return var
    else:
        return variables.get(var, None)


i = 0
while i < len(commands):
    command, *args = commands[i].split()
    args = [get_var(arg) for arg in args]

    if command == "READ":
        variables[args[0]] = get_var(input("> "))

    elif command == "WRITE":
        val = check_var(args[0])
        
        if val is not None:
            print(val)
        else:
            print(f"Undefined variable: {args[0]}")


    elif command in ("ADD", "SUB", "MUL", "DIV"):
        op1, op2, result_var = args
        op1_val = check_var(op1)
        op2_val = check_var(op2)
        if isinstance(op1_val, (int, float)) and isinstance(op2_val, (int, float)):
            if command == "ADD":
                variables[result_var] = op1_val + op2_val
            elif command == "SUB":
                variables[result_var] = op1_val - op2_val
            elif command == "MUL":
                variables[result_var] = op1_val * op2_val
            elif command == "DIV":
                if op2_val != 0:
                    variables[result_var] = op1_val / op2_val
                else:
                    print(f"Error: Division by zero at line {i+1}")

    elif command == "GOTOIFNOT":
        var, target_line = args
        if not bool(check_var(var)) or check_var(var) < 0:
            i = int(target_line) - 1
            continue

    elif command == "GOTOIF":
        var, target_line = args
        if bool(check_var(var)):
            i = int(target_line) - 1
            continue

    elif command == "GOTO":
        i = int(args[0]) - 1
        continue

    elif command == "COPY":
        variables[args[1]] = check_var(args[0])

    i += 1
