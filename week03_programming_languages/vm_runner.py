import sys

def run(bytecode, env=None):
    if isinstance(bytecode, str):
        # splitting instructions according to semicolons:
        bytecode = bytecode.replace(';', '\n')
        bytecode = bytecode.splitlines()
    stack = []
    if env is None:
        env = {}

    for instruct in bytecode:
        instruction = instruct.split()
        operation = instruction[0]
        if operation == '#':
            continue # comment
        if operation == "PUSH":
            stack.append(int(instruction[1]))
        elif operation in ("ADD", "SUB", "MUL", "DIV", "POW", "MOD"):
            right = stack.pop()
            left = stack.pop()
            if operation == "ADD":
                stack.append(left + right)
            elif operation == "SUB":
                stack.append(left - right)
            elif operation == "MUL":
                stack.append(left * right)
            elif operation == "DIV":
                stack.append(left // right)
            elif operation == "POW":
                stack.append(left ** right)
            elif operation == "MOD":
                stack.append(left % right)
        elif operation == "PRINT":
            print(stack.pop())
        elif operation == "LOAD":
            stack.append(env[instruction[1]])
        elif operation == "STORE":
            env[instruction[1]] = stack.pop()
        else:
            raise ValueError("Unknown instruction: " + operation)
    return env


sys.stdin = open(sys.argv[1])
program = sys.stdin.read()
run(program)
