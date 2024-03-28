def ai1():
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

def ai2():
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

def ai4():
    # Code 4
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

def ai5():
    # Code 5
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

def ai6():
    # Code 6
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

def ai7():
    # Code 7
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

def ai8():
    # Code 8
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

def dbms1():
    queries = [
        "1) \n\n"
        "SELECT GRADE,COUNT(DISTINCT CUST_ID)\n"
        "FROM CUST\n"
        "GROUP BY GRADE\n"
        "HAVING GRADE>(SELECT AVG(GRADE)\n"
        "FROM CUST\n"
        "WHERE CITY='BANGALORE');",

        "2) \n\n"
        "SELECT SAL_ID,NAME\n"
        "FROM SALE S\n"
        "WHERE (SELECT COUNT(*)\n"
        "FROM CUST C\n"
        "WHERE C.SAL_ID=S.SAL_ID)>1;",

        "3) \n\n"
        "SELECT S.SAL_ID,S.NAME,C.CUST_NAME,S.COMMISSION\n"
        "FROM SALE S,CUST C\n"
        "WHERE S.CITY=C.CITY\n"
        "UNION\n"
        "SELECT S.SAL_ID,S.NAME,'NO MATCH',S.COMMISSION\n"
        "FROM SALE S\n"
        "WHERE CITY NOT IN\n"
        "(SELECT CITY\n"
        "FROM CUST)\n"
        "ORDER BY 1 ASC;",

        "4) \n\n"
        "CREATE VIEW V_SALESMAN AS\n"
        "SELECT O.ODER_DATE,S.SAL_ID,S.NAME\n"
        "FROM SALE S,ORDR O\n"
        "WHERE S.SAL_ID=O.SAL_ID\n"
        "AND O.PUR_AMT=(SELECT MAX(PUR_AMT)\n"
        "FROM ORDR C\n"
        "WHERE C.ODER_DATE=O.ODER_DATE);\n\n"
        "VIEW CREATED\n"
        "SELECT * FROM V_SALESMAN;",

        "5) \n\n"
        "DELETE FROM SALESMAN\n"
        "WHERE SALE_ID=1000;"
    ]

    for query in queries:
        print(query)


def dbms2():
    queries = [
        "1. Display the youngest player (in terms of age) Name, Team name, age in which he belongs of the tournament.\n\n"
        "SELECT pname, tname, age\n"
        "FROM player p, team t\n"
        "WHERE p.tid = t.tid AND age = (SELECT min(age) FROM player);",

        "2. List the details of the stadium where the maximum number of matches were played.\n\n"
        "SELECT * FROM stadium\n"
        "WHERE sid IN\n"
        "\t(SELECT sid FROM match\n"
        "\tGROUP BY sid\n"
        "\tHAVING count(sid) = (SELECT max(count(sid)) FROM match GROUP BY sid));",

        "3. List the details of the player who is not a captain but got the man_of_match award atleast in two matches.\n\n"
        "SELECT * FROM player\n"
        "WHERE pid NOT IN\n"
        "\t(SELECT captain_pid FROM team)\n"
        "AND pid IN\n"
        "\t(SELECT man_of_match FROM match\n"
        "\tGROUP BY man_of_match\n"
        "\tHAVING count(man_of_match) >= 2);",

        "4. Display the teams details who won the maximum matches.\n\n"
        "SELECT * FROM team\n"
        "WHERE tid IN\n"
        "\t(SELECT winning_team_id FROM match\n"
        "\tGROUP BY winning_team_id\n"
        "\tHAVING count(winning_team_id) = (SELECT max(count(winning_team_id)) FROM match GROUP BY winning_team_id));",

        "5. Display the team name where all its won matches played in the same stadium.\n\n"
        "SELECT m.winning_team_id, t.tname, m.sid\n"
        "FROM match m, team t, stadium s\n"
        "WHERE m.winning_team_id = t.tid AND m.sid = s.sid\n"
        "GROUP BY (m.winning_team_id, t.tname, m.sid)\n"
        "HAVING count(m.sid) > 1;"
    ]

    for query in queries:
        print(query)

def dbms3():
    queries = [
        "1. List the movie titles of all movies directed by ‘Hitchcock’.\n\n"
        "SELECT MOV_TITLE \n"
        "FROM MOVIES\n"
        "WHERE DIR_ID IN (SELECT DIR_ID\n"
        "\tFROM DIRECTOR\n"
        "\tWHERE DIR_NAME = 'HITCHCOCK');",

        "2. Find the movie names where one or more actors acted in two or more movies.\n\n"
        "SELECT MOV_TITLE\n"
        "FROM MOVIES M, MOVIE_CAST MV\n"
        "WHERE M.MOV_ID = MV.MOV_ID AND\n"
        "\tMV.ACT_ID IN (SELECT ACT_ID\n"
        "\t\tFROM MOVIE_CAST\n"
        "\t\tGROUP BY ACT_ID\n"
        "\t\tHAVING COUNT(ACT_ID) > 1)\n"
        "GROUP BY MOV_TITLE\n"
        "HAVING COUNT(*) > 1;",

        "3. List all actors who acted in a movie before 2000 and also in a movie after 2015 (use JOIN operation).\n\n"
        "SELECT A.ACT_NAME, M.MOV_TITLE, M.MOV_YEAR\n"
        "FROM ACTOR A\n"
        "JOIN MOVIE_CAST C ON A.ACT_ID = C.ACT_ID\n"
        "JOIN MOVIES M ON C.MOV_ID = M.MOV_ID\n"
        "WHERE M.MOV_YEAR NOT BETWEEN 2000 AND 2015;",

        "4. Find the title of movies and number of stars for each movie that has at least one rating and find the highest number of stars that movie received. Sort the result by movie title.\n\n"
        "SELECT MOV_TITLE, MAX(REV_STARS)\n"
        "FROM MOVIES\n"
        "INNER JOIN RATING USING (MOV_ID)\n"
        "GROUP BY MOV_TITLE\n"
        "HAVING MAX(REV_STARS) > 0\n"
        "ORDER BY MOV_TITLE;",

        "5. Update rating of all movies directed by ‘Steven Spielberg’ to 5\n\n"
        "UPDATE RATING SET REV_STARS = 5\n"
        "WHERE MOV_ID IN (SELECT MOV_ID\n"
        "\t\t\tFROM MOVIES\n"
        "\t\t\tWHERE DIR_ID IN (SELECT DIR_ID\n"
        "\t\t\t\t\tFROM DIRECTOR\n"
        "\t\t\t\t\tWHERE DIR_NAME = 'STEVEN SPILBERGE'));"
    ]

    for query in queries:
        print(query)

def dbms4():
    queries = [
        "-- List all the student details studying in fourth semester 'C' section.\n\n"
        "SELECT S.*, SS.SEM, SS.SEC\n"
        "FROM STUDENT S, SEMSEC SS, CLASS C\n"
        "WHERE S.USN = C.USN AND\n"
        "SS.SSID = C.SSID AND\n"
        "SS.SEM = 4 AND SS.SEC='C';",

        "-- Compute the total number of male and female students in each semester and in each section.\n\n"
        "SELECT SS.SEM, SS.SEC, S.GENDER, COUNT(S.GENDER) AS COUNT\n"
        "FROM STUDENT S, SEMSEC SS, CLASS C\n"
        "WHERE S.USN = C.USN AND\n"
        "SS.SSID = C.SSID\n"
        "GROUP BY SS.SEM, SS.SEC, S.GENDER\n"
        "ORDER BY SEM;",

        "-- Create a view of Test1 marks of student USN ‘1BI15CS101’ in all Courses.\n\n"
        "CREATE VIEW STUDENT_TEST1_MARKS_V AS\n"
        "SELECT TEST1, SUBCODE\n"
        "FROM IAMARKS\n"
        "WHERE USN = '3BR15CS101';\n"
        "SELECT * FROM STUDENT_TEST1_MARKS_V;",

        "-- Calculate the FinalIA (average of best two test marks) and update the corresponding table for all students.\n\n"
        "UPDATE IAMARKS SET FINALIA= (GREATEST(TEST1+TEST2,TEST2+TEST3,TEST3+TEST1))/2;\n"
        "SELECT * FROM IAMARKS;",

        "-- Categorize students based on the following criterion:\n"
        "-- If FinalIA = 17 to 20 then CAT = 'Outstanding'\n"
        "-- If FinalIA = 12 to 16 then CAT = 'Average'\n"
        "-- If FinalIA < 12 then CAT = 'Weak'\n"
        "-- Give these details only for 8th semester A, B, and C section students.\n\n"
        "SELECT S.USN, S.SNAME, S.ADDRESS, S.PHONE, S.GENDER, IA.SUBCODE,\n"
        "(CASE\n"
        "\tWHEN IA.FINALIA BETWEEN 17 AND 20 THEN 'OUTSTANDING'\n"
        "\tWHEN IA.FINALIA BETWEEN 12 AND 16 THEN 'AVERAGE'\n"
        "\tELSE 'WEAK'\n"
        "END) AS CAT\n"
        "FROM STUDENT S, SEMSEC SS, IAMARKS IA, SUBJECT SUB\n"
        "WHERE S.USN = IA.USN AND\n"
        "SS.SSID = IA.SSID AND\n"
        "SUB.SUBCODE = IA.SUBCODE AND\n"
        "SUB.SEM = 8;"
    ]

    for query in queries:
        print(query)

def dbms5():
    queries = [
        "-- List the details of the candidates who are contesting from more than one constituency which are belongs to different states.\n\n"
        "select c.cand_id,cd.name,count(c.cons_id) from contest c,candidates cd where\n"
        "c.cand_id=cd.cand_id group by(cd.name,c.cand_id) having count(c.cons_id)>1;\n\n",

        "-- Display the state name having maximum number of constituencies.\n\n"
        "select csstate,count(cons_id) from constituency group by csstate order by\n"
        "count(cons_id);\n\n",

        "-- Create a stored procedure to insert the tuple into the voter table by checking the voter age. If voter’s age is at least 18 years old, then insert the tuple into the voter else display the “Not an eligible voter msg”.\n\n"
        "create procedure agechecking ( id in number,age in number)\n"
        "as\n"
        "BEGIN\n"
        "if age>18 then\n"
        "insert into voter(vid,vage) values (id,age);\n"
        "else\n"
        "dbms_output.put_line('age should be high');\n"
        "end if;\n"
        "end agechecking;\n"
        "/\n"
        "set serveroutput on;\n"
        "exec agechecking (25,21);\n"
        "exec agechecking (20,15);\n"
        "select * from voter;\n\n",

        "-- Display the constituency name, state and number of voters in each state in descending order using rank() function\n\n"
        "SELECT csname, csstate, no_of_voters,\n"
        "RANK () OVER (partition BY csstate order by no_of_voters desc) AS Rank_No\n"
        "FROM constituency;\n\n",

        "-- Create a TRIGGER to UPDATE the count of 'Number_of_voters' of the respective constituency in 'CONSTITUENCY' table, AFTER inserting a tuple into the 'VOTERS' table.\n\n"
        "create trigger count\n"
        "after insert on voter\n"
        "for each row\n"
        "begin\n"
        "update constituency\n"
        "set no_of_voters = no_of_voters + 1\n"
        "where cons_id=:new.cons_id;\n"
        "end count;\n"
        "/\n"
        "select * from constituency;\n"
        "insert into voter values(399,'nagesh',30,'mandya',111,199);\n"
        "select * from constituency;\n\n"
    ]

    for query in queries:
        print(query)
