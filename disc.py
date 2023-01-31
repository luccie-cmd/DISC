from sys import argv, exit

iota_counter = 0
def iota(reset: bool=False) -> int:
    global iota_counter
    if reset:
        iota_counter = 0
    result = iota_counter
    iota_counter += 1
    return result

OP_PLUS=iota(True)
OP_MINUS=iota()
OP_DUMP=iota()
OP_PUSH=iota()
COUNT_OPS=iota()

def plus():
    return (OP_PLUS, )
def minus():
    return (OP_MINUS, )
def dump():
    return (OP_DUMP, )
def push(x):
    return (OP_PUSH, x)

def load_program_from_file(file):
    try:
        with open(file, "r") as f:
            return [parse_token_as_op(word) for word in f.read().split()]
    except FileNotFoundError:
        print("Not a valid file only files with the exstension .disc are allowed")
        exit()

def parse_token_as_op(token):
    assert COUNT_OPS == 4, "Exhaustive handeling in parse_token_as_op(token)"
    if token == '+':
        return plus()
    elif token == '-':
        return minus()
    elif token == 'print':
        return dump()
    else:
        try:
            return push(int(token))
        except ValueError:
            print("Unknown token named: " + token)
            exit()

def simulate_program(program):
    stack = []
    for op in program:
        assert COUNT_OPS == 4, "Exhaustive handeling in simulate_program(program)"
        if op[0] == OP_PLUS:
            a = stack.pop()
            b = stack.pop()
            stack.append(a+b)
        elif op[0] == OP_MINUS:
            a = stack.pop()
            b = stack.pop()
            stack.append(b-a)
        elif op[0] == OP_DUMP:
            print(stack.pop())
        else:
            try:
                stack.append(int(op[1]))
            except ValueError:
                assert False, "Unreachable"

def usage():
    print("disc [SUBCOMMAND] <ARGS>")
    print("SUBBCOMMANDS: ")
    print("sim: simulate program")

if __name__ == '__main__':
    if len(argv) < 3:
        usage()
        print("No subbcommand or args")
        exit()
    subcommand = argv[1]
    file = argv[2]
    program = load_program_from_file(file=file)
    if subcommand == 'sim':
        simulate_program(program)
    elif subcommand == 'com':
        assert False, "Not implemented yet"
    else:
        assert False, "Invalid subcommand named: " + subcommand
    