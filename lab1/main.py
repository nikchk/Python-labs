mem_size = 10
allocated = []


def help():
    print('''Available commands:
    help  - show this help
    exit  - exit this program
    print - print memory blocks map
    allocate <num> - allocate <num> cells. Returns block first cell number
    free <num> - free block with first cell number <num>
    ''')


def allocate(n):
    if n <= mem_size and len(allocated) == 0:
        allocated.append([0, n])
        return 0

    if allocated[0][0] >= n:
        allocated.insert(0, [0, n])
        return 0

    for i in range(len(allocated) - 1):
        index = allocated[i][0] + allocated[i][1]
        if allocated[i + 1][0] - index >= n:
            allocated.insert(i + 1, [index, n])
            return index

    index1 = allocated[-1][0] + allocated[-1][1]
    if mem_size - index1 >= n:
        allocated.append([index1, n])
        return index1
    return -1


def free(ind):
    for i in range(len(allocated)):
        if allocated[i][0] == ind:
            del allocated[i]
            return


def print_memory():
    if width > 0:
        cells_in_row = width
    else:
        cells_in_row = mem_size

    total_chars = mem_size * 2
    c = [" "] * total_chars

    for block in allocated:
        start = block[0]
        length = block[1]
        start_pos = start * 2
        block_len = length * 2
        s = str(start)
        for j in range(len(s)):
            if start_pos + j < total_chars and j < block_len:
                c[start_pos + j] = s[j]
        for k in range(start_pos + len(s), start_pos + block_len):
            if k < total_chars and c[k] == " ":
                c[k] = "x"

    block_ends = []
    for block in allocated:
        end_pos = (block[0] + block[1]) * 2
        block_ends.append(end_pos)

    row_len = cells_in_row * 2
    i = 0
    while i < total_chars:
        end_i = i + row_len
        if end_i > total_chars:
            end_i = total_chars

        segment = c[i:end_i]

        for b in block_ends:
            if i < b < end_i:
                p = b - i
                if p < len(segment):
                    segment[p - 1] = "|"

        seg = "".join(segment)
        if len(seg) < row_len:
            seg = seg + " " * (row_len - len(seg))
        print("|" + seg + "|")
        i = end_i

    if mem_size == 0:
        print("||")


while True:
    line = input().strip()
    if not line:
        print("Please enter two integers, e.g.: 30 10")
        continue
    parts = line.split()
    if len(parts) != 2 or not all(p.isdigit() for p in parts):
        print("Please set memory size and max output width:")
        continue
    mem_size = int(parts[0])
    width = int(parts[1])
    allocated = []
    break

print("Type 'help' for additional info.")

while True:
    line = input().strip()
    if not line:
        print("Type 'help' for additional info.")
        continue
    parts = line.split()

    if parts[0] == "help":
        help()

    elif parts[0] == "print":
        print_memory()

    elif parts[0] == "allocate":
        if len(parts) != 2 or not parts[1].isdigit():
            print("Usage: allocate <num>")
            continue
        n = int(parts[1])
        pos = allocate(n)
        print(pos)

    elif parts[0] == "free":
        if len(parts) != 2 or not parts[1].isdigit():
            print("Usage: free <block_id>")
            continue
        free(int(parts[1]))

    elif parts[0] == "exit":
        break

    else:
        print("No such command, type 'help'")
