import sys
import time
import psutil
import os

DELTA = 30
SCORES = {
    ('A','A'):0, ('A','C'):110, ('A','G'):48,  ('A','T'):94,
    ('C','A'):110,('C','C'):0,   ('C','G'):118, ('C','T'):48,
    ('G','A'):48, ('G','C'):118, ('G','G'):0,   ('G','T'):110,
    ('T','A'):94, ('T','C'):48,  ('T','G'):110, ('T','T'):0,
}

def pair_score(a,b):
    if a=='_' or b=='_': return DELTA
    return SCORES[(a,b)]

def parse_and_generate(path):
    with open(path, 'r') as f:
        lines=[ln.strip() for ln in f.readlines() if ln.strip()!='']
    s = lines[0]
    i=1
    while i<len(lines) and lines[i].isdigit():
        idx=int(lines[i])
        s = s[:idx+1] + s + s[idx+1:]
        i+=1

    t = lines[i]; i+=1
    while i<len(lines) and lines[i].isdigit():
        idx=int(lines[i])
        t = t[:idx+1] + t + t[idx+1:]
        i+=1
    return s,t

def full_dp(s,t):
    n,m=len(s),len(t)
    dp=[[0]*(m+1) for _ in range(n+1)]
    tb=[['']*(m+1) for _ in range(n+1)]

    for i in range(1,n+1):
        dp[i][0]=dp[i-1][0]+DELTA
        tb[i][0]='|'
    for j in range(1,m+1):
        dp[0][j]=dp[0][j-1]+DELTA
        tb[0][j]='-'

    for i in range(1,n+1):
        for j in range(1,m+1):
            dig = dp[i-1][j-1] + pair_score(s[i-1],t[j-1])
            up  = dp[i-1][j] + DELTA
            le  = dp[i][j-1] + DELTA
            if dig <= up and dig <= le:
                dp[i][j]=dig; tb[i][j]='\\'
            elif up < le:
                dp[i][j]=up; tb[i][j]='|'
            else:
                dp[i][j]=le; tb[i][j]='-'

    i,j=n,m
    a1=[]; a2=[]
    while i>0 or j>0:
        if tb[i][j]=='\\':
            a1.append(s[i-1]); a2.append(t[j-1]); i-=1; j-=1
        elif tb[i][j]=='|':
            a1.append(s[i-1]); a2.append('_'); i-=1
        elif tb[i][j]=='-':
            a1.append('_'); a2.append(t[j-1]); j-=1
        else:
            if i>0: a1.append(s[i-1]); a2.append('_'); i-=1
            else:   a1.append('_'); a2.append(t[j-1]); j-=1

    return dp[n][m], ''.join(reversed(a1)), ''.join(reversed(a2))

def main():
    if len(sys.argv)!=3:
        print("Usage: python3 basic.py input.txt output.txt")
        sys.exit(1)

    infile, outfile = sys.argv[1], sys.argv[2]
    s,t=parse_and_generate(infile)

    start = time.time()
    score,a1,a2 = full_dp(s,t)
    end = time.time()

    process = psutil.Process(os.getpid())
    memory_kb = process.memory_info().rss / 1024

    time_ms = (end-start)*1000

    with open(outfile,'w') as f:
        f.write(f"{int(score)}\n")
        f.write(a1+"\n")
        f.write(a2+"\n")
        f.write(f"{time_ms:.3f}\n")
        f.write(f"{memory_kb:.3f}\n")

if __name__=="__main__":
    main()
