import os
import subprocess
import csv

# All input files
input_files = [f"in{i}.txt" for i in range(1, 16)]

# Output file names
basic_out = lambda i: f"out_basic_{i}.txt"
eff_out = lambda i: f"out_efficient_{i}.txt"

results = []

for i, infile in enumerate(input_files, start=1):
    print(f"Running input {infile} ...")

    # Run basic version
    subprocess.run(
        ["python3", "basic.py", infile, basic_out(i)],
        check=True
    )

    # Run efficient version
    subprocess.run(
        ["python3", "efficient.py", infile, eff_out(i)],
        check=True
    )

    # Read outputs
    with open(basic_out(i)) as f:
        lines = f.read().splitlines()
        basic_time = float(lines[3])
        basic_mem = float(lines[4])

    with open(eff_out(i)) as f:
        lines = f.read().splitlines()
        eff_time = float(lines[3])
        eff_mem = float(lines[4])

    total_len = None
    # Estimate problem size = len(s) + len(t)
    # (we can re-parse the input file)
    with open(infile) as f:
        raw = [line.strip() for line in f.readlines() if line.strip() != ""]
        # Construct strings the same way parse_and_generate works
        s = raw[0]
        idx = 1
        while idx < len(raw) and raw[idx].isdigit():
            pos = int(raw[idx]) + 1
            s = s[:pos] + s + s[pos:]
            idx += 1
        t = raw[idx]
        idx += 1
        while idx < len(raw) and raw[idx].isdigit():
            pos = int(raw[idx]) + 1
            t = t[:pos] + t + t[pos:]
            idx += 1
        total_len = len(s) + len(t)

    results.append([
        i,
        infile,
        total_len,
        basic_time,
        basic_mem,
        eff_time,
        eff_mem
    ])

# Write to CSV
with open("results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "ID", "InputFile", "Size(m+n)",
        "BasicTime(ms)", "BasicMem(KB)",
        "EffTime(ms)", "EffMem(KB)"
    ])
    writer.writerows(results)

print("\nDone! results.csv generated.")
