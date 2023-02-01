import sys

iota_counter=0
def iota(reset=False):
    global iota_counter
    if reset:
        iota_counter = 0
    result = iota_counter
    iota_counter+=1
    return result

OP_PUSH=iota(True)
OP_PLUS=iota() 
OP_MINUS=iota()
OP_TIMES=iota()
OP_DIVIDE=iota()
OP_INTDIV=iota()
OP_MOD=iota()
OP_DUMP=iota()
OP_BOOLDUMP=iota()
OP_EQUAL=iota()
OP_IF=iota()
OP_END=iota()
COUNT_OPS=iota()

def uncos(xs):
    return (xs[0], xs[1:])

def plus():
    return (OP_PLUS, )
def minus():
    return (OP_MINUS, )
def times():
    return (OP_TIMES, )
def divide():
    return (OP_DIVIDE, )
def int_dev():
    return (OP_INTDIV, )
def mod():
    return (OP_MOD, )
def dump():
    return (OP_DUMP, )
def booldump():
    return (OP_BOOLDUMP, )
def push(x):
    return (OP_PUSH, x)
def equal():
    return (OP_EQUAL, )
def iif():
    return (OP_IF, )
def end():
    return (OP_END, )


def parse_word_as_op(word):
    if word == '+':
        return plus()
    elif word == '-':
        return minus()
    elif word == '*':
        return times()
    elif word == '/':
        return divide()
    elif word == '//':
        return int_dev()
    elif word == '%':
        return mod()
    elif word == "=":
        return equal()
    elif word == "end":
        return end()
    elif word == "if":
        return iif()
    elif word == 'print':
        return dump()
    elif word == 'boolprint':
        return booldump()
    else:
        try:
            return push(int(word))
        except ValueError:
            print("invalid word at parse_word_as_op() named: %s" %word)
            exit(1)
def load_file_from_path(path_to_file):
    try:
        with open(path_to_file, "r") as file:
            return cross_reference_program([parse_word_as_op(word) for word in file.read().split()])
    except FileNotFoundError:
        print("Invalid file type or file name\nOnly file types of *.disc are alowed %s is not a valid file" %path_to_file)
        exit(1)

def simulate_program(program):
    stack=[]
    ip=0
    while ip < len(program):
        assert COUNT_OPS == 12, "exhaustive handeling at simulate_program()"
        op = program[ip]
        if op[0] == OP_PUSH:
            stack.append(op[1])
            ip+=1
        elif op[0] == OP_PLUS:
            a = stack.pop()
            b = stack.pop()
            stack.append(a + b)
            ip+=1
        elif op[0] == OP_MINUS:
            a = stack.pop()
            b = stack.pop()
            stack.append(b - a)
            ip+=1
        elif op[0] == OP_TIMES:
            a = stack.pop()
            b = stack.pop()
            stack.append(a * b)
            ip+=1
        elif op[0] == OP_DIVIDE:
            a = stack.pop()
            b = stack.pop()
            stack.append(b / a)
            ip+=1
        elif op[0] == OP_INTDIV:
            a = stack.pop()
            b = stack.pop()
            stack.append(b // a)
            ip+=1
        elif op[0] == OP_MOD:
            a = stack.pop()
            b = stack.pop()
            stack.append(b % a)
            ip+=1
        elif op[0] == OP_EQUAL:
            a = stack.pop()
            b = stack.pop()
            stack.append(int(a == b))
            ip += 1
        elif op[0] == OP_IF:
            a = stack.pop()
            if a == 0:
                assert len(op) >= 2, "`if` blocks need `end` blocks"
                ip = op[1]
            else:
                ip+=1
        elif op[0] == OP_END:
            ip += 1
        elif op[0] == OP_DUMP:
            print(stack.pop())
            ip+=1
        elif op[0] == OP_BOOLDUMP:
            a = stack.pop()
            if a == 0:
                print("False")
            else:
                print("True")
            ip+=1
        else:
            assert False, "Unrecheable"

def compile_program(program):
    print("Not implemented yet")

def cross_reference_program(program):
    stack = []
    for ip in range(len(program)):
        op = program[ip]
        assert COUNT_OPS == 12, "exhaustive handeling at cross_reference_program() remember not everything needs to be handeld in here only that that form blocks"
        if op[0] == OP_IF:
            stack.append(ip)
        elif op[0] == OP_END:
            if_ip = stack.pop()
            assert program[if_ip][0] == OP_IF, "`End` blocks can only close `if` blocks for now"
            program[if_ip] = (OP_IF, ip)
    return program

def usage(program):
    print('usage: %s [SUBCOMMAND] <ARGS>' %program)
    print('subcommands are: ')
    print('sim    simulate the program')
    print('com    compile  the program')

if __name__ == '__main__':
    argv = sys.argv
    assert len(argv) >= 1
    (program, argv) = uncos(argv)
    if len(argv) < 1:
        usage(program)
        assert False, "no subcommand provided"
    (subcommand, argv) = uncos(argv)

    if subcommand == 'sim':
        (input_file, argv) = uncos(argv)
        program = load_file_from_path(input_file)
        simulate_program(program)
    elif subcommand == 'com':
        (input_file, argv) = uncos(argv)
        program = load_file_from_path(input_file)
        compile_program(program)
    else:
        assert False, "Invalid subcommand"