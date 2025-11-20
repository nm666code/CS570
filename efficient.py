import sys
import time
import psutil
import os

DELTA = 30
SCORES = {
    ('A','A'):0, ('A','C'):110, ('A','G'):48,  ('A','T'):94,
    ('C','A'):110, ('C','C'):0,   ('C','G'):118, ('C','T'):48,
    ('G','A'):48,  ('G','C'):118, ('G','G'):0,   ('G','T'):110,
    ('T','A'):94,  ('T','C'):48,  ('T','G'):110, ('T','T'):0,
}

def pair_score(a, b):
    if a == '_' or b == '_':
        return DELTA
    return SCORES[(a, b)]

def parse_and_generate(path):
    with open(path, 'r') as f:
        lines = [ln.strip() for ln in f.readlines() if ln.strip() != ""]

    s = lines[0]
    i = 1
    while i < len(lines) and lines[i].isdigit():
        idx = int(lines[i])
        pos = idx + 1
        s = s[:pos] + s + s[pos:]
        i += 1

    t = lines[i]
    i += 1
    while i < len(lines) and lines[i].isdigit():
        idx = int(lines[i])
        pos = idx + 1
        t = t[:pos] + t + t[pos:]
        i += 1

    return s, t

def nw_score_row(a, b):
    m = len(b)
    prev = [0] * (m + 1)

    for j in range(1, m + 1):
        prev[j] = prev[j - 1] + DELTA

    for i in range(1, len(a) + 1):
        cur = [0] * (m + 1)
        cur[0] = prev[0] + DELTA
        ai = a[i - 1]

        for j in range(1, m + 1):
            cur[j] = min(
                prev[j] + DELTA,
                cur[j - 1] + DELTA,
                prev[j - 1] + pair_score(ai, b[j-1])
            )
        prev = cur
    return prev

def full_dp(s, t):
    n, m = len(s), len(t)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    tb = [[''] * (m + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        dp[i][0] = dp[i - 1][0] + DELTA
        tb[i][0] = '|'

    for j in range(1, m + 1):
        dp[0][j] = dp[0][j - 1] + DELTA
        tb[0][j] = '-'

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            dig = dp[i - 1][j - 1] + pair_score(s[i - 1], t[j - 1])
            up  = dp[i - 1][j] + DELTA
            le  = dp[i][j - 1] + DELTA

            if dig <= up and dig <= le:
                dp[i][j] = dig
                tb[i][j] = '\\'
            elif up < le:
                dp[i][j] = up
                tb[i][j] = '|'
            else:
                dp[i][j] = le
                tb[i][j] = '-'

    i, j = n, m
    a1, a2 = [], []
    while i > 0 or j > 0:
        if tb[i][j] == '\\':
            a1.append(s[i - 1])
            a2.append(t[j - 1])
            i -= 1
            j -= 1
        elif tb[i][j] == '|':
            a1.append(s[i - 1])
            a2.append('_')
            i -= 1
        elif tb[i][j] == '-':
            a1.append('_')
            a2.append(t[j - 1])
            j -= 1
        else:
            if i > 0:
                a1.append(s[i - 1]); a2.append('_'); i -= 1
            else:
                a1.append('_'); a2.append(t[j - 1]); j -= 1

    return dp[n][m], ''.join(reversed(a1)), ''.join(reversed(a2))

def hirschberg(a, b):
    if len(a) == 0:
        return 0, '_' * len(b), b
    if len(b) == 0:
        return 0, a, '_' * len(a)

    if len(a) == 1 or len(b) == 1:
        return full_dp(a, b)

    n = len(a)
    mid = n // 2

    scoreL = nw_score_row(a[:mid], b)
    scoreR = nw_score_row(a[mid:][::-1], b[::-1])

    m = len(b)
    best_k = 0
    best_val = None

    for k in range(m + 1):
        val = scoreL[k] + scoreR[m - k]
        if best_val is None or val < best_val:
            best_val = val
            best_k = k

    left_score, la, lb = hirschberg(a[:mid], b[:best_k])
    right_score, ra, rb = hirschberg(a[mid:], b[best_k:])

    return left_score + right_score, la + ra, lb + rb

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 efficient.py input.txt output.txt")
        sys.exit(1)

    infile, outfile = sys.argv[1], sys.argv[2]

    s, t = parse_and_generate(infile)

    start = time.time()
    score, A, B = hirschberg(s, t)
    end = time.time()

    process = psutil.Process(os.getpid())
    memory_kb = process.memory_info().rss / 1024
    time_ms = (end - start) * 1000

    with open(outfile, 'w') as f:
        f.write(f"{int(score)}\n")
        f.write(A + "\n")
        f.write(B + "\n")
        f.write(f"{time_ms:.3f}\n")
        f.write(f"{memory_kb:.3f}\n")


if __name__ == "__main__":
    main()
