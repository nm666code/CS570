import csv
import matplotlib.pyplot as plt

sizes = []
basic_time = []
eff_time = []
basic_mem = []
eff_mem = []

with open("results.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        sizes.append(int(row["Size(m+n)"]))
        basic_time.append(float(row["BasicTime(ms)"]) / 1000)   # ms → s
        eff_time.append(float(row["EffTime(ms)"]) / 1000)
        basic_mem.append(float(row["BasicMem(KB)"]))
        eff_mem.append(float(row["EffMem(KB)"]))

# ------------------------ CPU Plot ------------------------
plt.figure(figsize=(8,6))
plt.plot(sizes, basic_time, 'ro-', label="Basic Version")
plt.plot(sizes, eff_time, 'go-', label="Efficient Version")
plt.xlabel("Problem Size (m+n)")
plt.ylabel("CPU Time (s)")
plt.title("CPU Time vs Problem Size")
plt.grid(True)
plt.legend()
plt.savefig("CPUPlot.png", dpi=300)

# ------------------------ Memory Plot ------------------------
plt.figure(figsize=(8,6))
plt.plot(sizes, basic_mem, 'ro-', label="Basic Version")
plt.plot(sizes, eff_mem, 'go-', label="Efficient Version")
plt.xlabel("Problem Size (m+n)")
plt.ylabel("Memory Usage (KB)")
plt.title("Memory Usage vs Problem Size")
plt.grid(True)
plt.legend()
plt.savefig("MemoryPlot.png", dpi=300)

print("CPUPlot.png and MemoryPlot.png generated.")
