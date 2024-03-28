def p1():
    # Code 1
    print("""
def water(cap_x, cap_y, tar):
    stack = [(0, 0, [])]
    vis = set()
    while stack:
        x, y, path = stack.pop()
        if (x, y) in vis:
            continue
        vis.add((x, y))
        if x == tar or y == tar:
            return path + [(x, y)]
        ops = [
            ("x_full", cap_x, y),
            ("y_full", x, cap_y),
            ("x_emp", 0, y),
            ("y_emp", x, 0),
            ("x_to_y", max(0, x - (cap_y - y)), min(cap_y, y + x)),
            ("y_to_x", min(cap_x, y + x), max(0, y - (cap_x - x))),
        ]
        print(ops)
        for op, n1, n2 in ops:
            if 0 <= n1 <= cap_x and 0 <= n2 <= cap_y:
                stack.append((n1, n2, path + [(x, y, op)]))
    return None

cap_x = 4
cap_y = 3
tar = 2
res = water(cap_x, cap_y, tar)
for state in res:
    print(f"({state[0], state[1]})")
    """)

def p2():
    # Code 2
    print("""
tree = {
    1: [2, 9, 10],
    2: [3, 4],
    3: [],
    4: [5, 6, 7],
    5: [8],
    6: [],
    7: [],
    8: [],
    9: [],
    10: [],
}

def bfs(tree, start):
    q = [start]
    v = []
    while q:
        print("before", q)
        node = q.pop(0)
        v.append(node)
        for child in tree[node]:
            if child not in q and child not in v:
                q.append(child)
                print("after", q)
    return v

r = bfs(tree, 1)
print(r)
    """)

def p4():
    # Code 3
    print("""
n = int(input())
board = [[0] * n for _ in range(n)]

def attack(i, j):
    for k in range(0, n):
        if board[i][k] == 1 or board[k][j] == 1:
            return True
    for k in range(0, n):
        for l in range(0, n):
            if (k + l == i + j) or (k - l == i - j):
                if board[k][l] == 1:
                    return True
    return False

def nq(n):
    if n == 1:
        return True
    for i in range(0, n):
        for j in range(0, n):
            if (not attack(i, j)) and (board[i][j] != 1):
                board[i][j] = 1
                if nq(n - 1) == True:
                    return True
                board[i][j] = 0
    return False

nq(n)
for i in board:
    print(i)
    """)

def p5():
    # Code 4
    print("""
from itertools import permutations

def min_path(t, ds):
    ts = 0
    for i in range(len(t) - 1):
        ts += ds[t[i]][t[i + 1]]
    ts += ds[t[-1]][t[0]]
    return ts

def tsp(ds):
    c = list(range(len(ds)))
    m = float("inf")
    op = None
    for t in permutations(c):
        d = min_path(t, ds)
        if d < m:
            m = d
            op = t
    return op, m

ds = [[0, 10, 15, 20], [10, 0, 35, 25], [15, 35, 0, 30], [20, 25, 30, 0]]
op, m = tsp(ds)
print(op)
print(m)
    """)

def p6():
    # Code 5
    print("""
global r
global f
r = True
f = [["plant", "mango"], ["eat", "mango"], ["seed", "spourt"]]

def asse(fact):
    global f
    global r
    if not fact in f:
        f += [fact]
        r = True

while r:
    r = False
    for a in f:
        if a[0] == "seed":
            asse(["plant", a[1]])
        if a[0] == "plant":
            asse(["fruit", a[1]])
        if a[0] == "plant" and ["eat", a[1]] in f:
            asse(["human", a[1]])

print(f)
    """)

def p7():
    # Code 6
    print("""
from sympy import symbols, Not, Or, simplify

def r(nc1, nc2):
    ro = []
    for l1 in nc1:
        for l2 in nc2:
            if l1 == Not(l2) or l2 == Not(l1):
                ro.extend([l for l in (nc1 + nc2) if l != l1 and l != l2])
                print(ro)
    return list(set(ro))

def an(c):
    nec = list(c)
    while True:
        n = len(nec)
        pairs = [(nec[i], nec[j]) for i in range(n) for j in range(i + 1, n)]
        for (nc1, nc2) in pairs:
            rev = r(nc1, nc2)
            print(rev)
            if not rev:
                return True
            if rev not in nec:
                nec.append(rev)
        if n == len(nec):
            return False

if __name__ == "__main__":
    c1 = [symbols("p"), Not(symbols("q"))]
    c2 = [Not(symbols("p")), symbols("q")]
    c3 = [Not(symbols("p")), Not(symbols("q"))]
    c = [c1, c2, c3]

    r = an(c)
    if r:
        print("not")
    else:
        print("ok")
    """)

def p8():
    # Code 7
    print("""
board = [" " for _ in range(9)]

def pb():
    r1 = "|{}|{}|{}|".format(board[0], board[1], board[2])
    r2 = "|{}|{}|{}|".format(board[3], board[4], board[5])
    r3 = "|{}|{}|{}|".format(board[6], board[7], board[8])
    print()
    print(r1)
    print(r2)
    print(r3)
    print()

def ac(icon):
    if icon == "x":
        n = 1
    elif icon == "o":
        n = 2
    print("your turn palyer {}".format(n))
    c = int(input().strip())
    if board[c - 1] == " ":
        board[c - 1] = icon
    else:
        print("not")

def win(icon):
    if (board[0] == icon and board[1] == icon and board[2] == icon) or (
        board[0] == icon and board[4] == icon and board[8] == icon
    ):
        return True
    else:
        return False


def dra():
    if " " not in board:
        return True
    else:
        return False


while True:
    pb()
    ac("x")
    if win("x"):
        print("won")
        break
    elif dra():
        print("darw")
        break
    ac("o")
    if win("o"):
        print("won")
        break
    elif dra():
        print("darw")
        break
    """)
