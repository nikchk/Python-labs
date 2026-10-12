import re

with open("Pract/compiler.txt", "r") as f:
    lines = f.readlines()


def write_compiled_code(file):
    with open(file, 'w', encoding='utf-8') as output_file:
        for item in commands:
            print(item, file=output_file) 

src = "".join([l for l in lines if not l.strip().startswith("//")])

for s in ["\n", " ", "\t"]:
    src = src.replace(s, "")



text = src
memory = {}
index = 0

class Token:
    def __init__(self, lexeme):
        self.lexeme = lexeme

    def __repr__(self):
        return f"{self.lexeme!r}"

    lexeme: str

    def __getitem__(self, key):
        return self.lexeme[key]

def tokenize():
    pos = 0
    res = []
    markers = ";,>=+-*/()[]{}"
    
    while pos < len(src):
        if src[pos] in markers:
            res.append(Token(src[pos]))
            pos += 1
        else:
            start = pos
            while pos < len(src) and src[pos] not in markers:
                pos += 1
            if start < pos:
                res.append(Token(src[start:pos]))
    
    return res


tokens = tokenize()
index = 0
commands = []

class Node:
    def __init__(self, token, res_var, l=None, r=None):
        self.token = token
        self.res_var = res_var
        self.l = l
        self.r = r
        self.mark = 0
        self.inverse = False

def priority(t: str) -> int:
    return {
        "+": 1,
        "-": 1,
        "*": 2,
        "/": 2
    }.get(t, -1)

def is_op(t: str) -> bool:
    return priority(t) > 0


def gen_comm(args, ops):
    rhs = args.pop()
    lhs = args.pop()
    op = ops.pop()
    args.append(Node(op, None, lhs, rhs))



def compile_expr_to_tree():
    global index
    ops = []
    args = []
    while tokens[index].lexeme not in [";", "]"]:
        token = tokens[index]
        if is_op(token.lexeme):
            while len(ops) > 0 and is_op(ops[-1]) and priority(ops[-1]) >= priority(token.lexeme):
                gen_comm(args, ops)
            ops.append(token.lexeme)
        elif token.lexeme == "(":
            ops.append(token.lexeme)
        elif token.lexeme == ")":
            while len(ops) > 0 and ops[-1] != "(":
                gen_comm(args, ops)
            ops.pop()
        else:
            args.append(Node(token.lexeme, token.lexeme))
        index += 1
    while len(ops) > 0:
        gen_comm(args, ops)
    return args[0] if args else None


def label_tree(node):
    """Sethi-Ullman"""
    if node is None:
        return 0
    if node.l is None and node.r is None:
        node.mark = 1
        return 1
    
    left_label = label_tree(node.l)
    right_label = label_tree(node.r)
    
    if left_label == right_label:
        node.mark = left_label + 1
    else:
        node.mark = max(left_label, right_label)
    
    return node.mark


def generate_code_from_tree(node, temp_stack):
    if node is None:
        return None
    
    if node.l is None and node.r is None:
        return node.token
    
    op_name = {'+': "ADD", '-': "SUB", '*': "MUL", '/': "DIV"}[node.token]
    

    if node.l.mark >= node.r.mark:
        left_result = generate_code_from_tree(node.l, temp_stack)
        right_result = generate_code_from_tree(node.r, temp_stack)
    else:
        right_result = generate_code_from_tree(node.r, temp_stack)
        left_result = generate_code_from_tree(node.l, temp_stack)
    

    temp_var = f"t{temp_stack[0]}"
    temp_stack[0] += 1
    

    if temp_stack[0] > temp_stack[1]:
        temp_stack[1] = temp_stack[0]
    
    commands.append(f"{op_name} {left_result} {right_result} {temp_var}")
    node.res_var = temp_var
    
    return temp_var


def handleExpression(res_var=None):
    global index
    

    tree = compile_expr_to_tree()
    if not tree: return None


    if tree.l is None and tree.r is None:
        if res_var:
            commands.append(f"COPY {tree.token} {res_var}")
            return res_var
        return tree.token

    groups = {}
    group(tree, groups)      
    forest = decompose(tree, groups) 

  
    temp_stack = [1, 1]


    for k_var, sub_tree in sorted(forest.items()):
        label_tree(sub_tree)
        res = generate_code_from_tree(sub_tree, temp_stack)
        commands.append(f"COPY {res} {k_var}")

    label_tree(tree)
    result = generate_code_from_tree(tree, temp_stack)
    
    if res_var:
        parts = commands[-1].split()
        if parts[0] in ["ADD", "SUB", "MUL", "DIV", "COPY"] and parts[-1].startswith("t"):
            parts[-1] = res_var 
            commands[-1] = " ".join(parts)
        else:
            commands.append(f"COPY {result} {res_var}")
        return res_var
    
    return result


def handleCommand():
    global index
    if tokens[index].lexeme == "read":
        commands.append(f"READ {tokens[index+2].lexeme}")
        index += 4
    elif tokens[index].lexeme == "write":
        commands.append(f"WRITE {tokens[index+2].lexeme}")
        index += 4
    else:
        res_var = tokens[index].lexeme
        index += 2
        handleExpression(res_var)
        index +=1


def handleBlock():
    global index

    if tokens[index].lexeme == "{":
        index += 1

    while index < len(tokens) and tokens[index].lexeme != "}":
        if tokens[index].lexeme in ["if","while","else"]:
            handleOperatorBlock()
        else:
            handleCommand()

def handleOperatorBlock():
    global index
    is_loop = tokens[index].lexeme == "while"
    index += 2  
    
    loop_start_pos = 0
    if is_loop:
        loop_start_pos = len(commands)
    
    res_var = handleExpression()
    gotoifnot_pos = len(commands)
    commands.append(f"GOTOIFNOT {res_var} _")
    
    index += 2  
    handleBlock()
    index += 1  
    
    if is_loop:
        commands.append(f"GOTO {loop_start_pos + 1}")
        commands[gotoifnot_pos] = commands[gotoifnot_pos].replace("_", str(len(commands) + 1))


def compare(n1, n2):
    """Перевіряє, чи два дерева ідентичні"""
    if n1 is None and n2 is None: return True
    if n1 is None or n2 is None: return False
    if n1.token != n2.token: return None
    return compare(n1.l, n2.l) and compare(n1.r, n2.r)

def hash_node(n):
    """Створює унікальний рядок-підпис для виразу"""
    if not n: return None
    if n.l is None and n.r is None:
        return str(n.token)
    
    hl = hash_node(n.l)
    hr = hash_node(n.r)
    
    if n.token in ["+", "*"] and str(hl) > str(hr):
        hl, hr = hr, hl
    return f"({hl}){n.token}({hr})"

def group(n, res):
    """Знаходить всі однакові підвирази у дереві"""
    if not n: return
    if n.l is not None or n.r is not None:
        h = hash_node(n)
        if h not in res:
            res[h] = [n]
        else:
            res[h].append(n)
            
    group(n.l, res)
    group(n.r, res)

def copy_node(n):
    """Створює повну копію вузла"""
    if not n: return None
    new = Node(n.token, n.res_var, None, None) 
    new.l = copy_node(n.l)
    new.r = copy_node(n.r)
    return new

def decompose(n, res):
    """Виносить повторювані вузли в окремий 'ліс' (forest)"""
    forest = {}
    i = 0
    for h in res:
        if len(res[h]) < 2:
            continue
            
        k = f"k{i}"
         
        forest[k] = copy_node(res[h][0]) 
        
        for node in res[h]:
            node.l = None
            node.r = None
            node.token = k
            
        i += 1
    return forest


handleBlock()
write_compiled_code('Pract/compiled_code.txt')
