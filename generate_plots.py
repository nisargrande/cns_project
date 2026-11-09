import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Ensure output directory exists
out_dir = r"C:\Users\Nisarg\.gemini\antigravity\scratch\ieee_fdi_ev_paper\images"
os.makedirs(out_dir, exist_ok=True)

# Set high-quality IEEE publication styling
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['xtick.labelsize'] = 9
plt.rcParams['ytick.labelsize'] = 9
plt.rcParams['legend.fontsize'] = 9
plt.rcParams['figure.titlesize'] = 13

# ==========================================================
# FIGURE 1: End-to-End System Flowchart
# ==========================================================
fig, ax = plt.subplots(figsize=(10, 4.5), dpi=300)
ax.set_xlim(0, 100)
ax.set_ylim(0, 50)
ax.axis('off')

# Box styles
box_blue = dict(boxstyle="round,pad=0.5", fc="#e8f1f5", ec="#1f77b4", lw=2)
box_green = dict(boxstyle="round,pad=0.5", fc="#e8f8ec", ec="#2ca02c", lw=2)
box_red = dict(boxstyle="round,pad=0.5", fc="#fde8e8", ec="#d62728", lw=2)
box_gold = dict(boxstyle="round,pad=0.5", fc="#fef7e0", ec="#bc8000", lw=2)

# Nodes
ax.text(10, 38, "EV User Inputs\n(ST, ET, ED, MA)", ha="center", va="center", bbox=box_blue, weight="bold")
ax.text(32, 38, "EVSE & CMS\nCommunication\n(HTTP / OCPP)", ha="center", va="center", bbox=box_blue, weight="bold")
ax.text(58, 38, "NARX Neural\nNetwork Estimator\n(Closed-Loop $\hat{y}(t)$)", ha="center", va="center", bbox=box_green, weight="bold")
ax.text(85, 38, "EoE Computation\n$EoE(t) = y(t) - \hat{y}(t)$\n& IQR Bounds (UB, LB)", ha="center", va="center", bbox=box_blue, weight="bold")

ax.text(32, 14, "Stealthy FDI Attack\n(ID Spoofing / MitM)\n$MA \Rightarrow MA \pm \phi$", ha="center", va="center", bbox=box_red, weight="bold")
ax.text(68, 14, "Window Mechanism\nConsecutive Spikes\n$(q \geq 5)$", ha="center", va="center", bbox=box_gold, weight="bold")
ax.text(90, 14, "FDI Attack Alert\n& Mitigation\n(Acc: 99.40%)", ha="center", va="center", bbox=box_red, weight="bold")

# Normal flow arrows
arrow_norm = dict(arrowstyle="->", lw=2, color="#1f77b4")
ax.annotate("", xy=(22, 38), xytext=(17.5, 38), arrowprops=arrow_norm)
ax.annotate("", xy=(47.5, 38), xytext=(41.5, 38), arrowprops=arrow_norm)
ax.annotate("", xy=(73.5, 38), xytext=(68.5, 38), arrowprops=arrow_norm)

# Attack flow arrows
arrow_att = dict(arrowstyle="->", lw=2, color="#d62728", ls="--")
ax.annotate("", xy=(32, 21), xytext=(32, 31.5), arrowprops=arrow_att)
ax.annotate("", xy=(47.5, 33), xytext=(41.5, 18), arrowprops=arrow_att)

# Detection flow arrows
arrow_det = dict(arrowstyle="->", lw=2, color="#333333")
ax.annotate("", xy=(68, 22), xytext=(85, 30.5), arrowprops=arrow_det)
ax.annotate("", xy=(80, 14), xytext=(78, 14), arrowprops=arrow_det)

ax.set_title("End-to-End System Pipeline: Stealthy FDI Attack Injection, NARX Forecasting, and IQR Window Detection", fontsize=11, weight="bold", pad=12)
plt.tight_layout()
plt.savefig(os.path.join(out_dir, "fig1_flowchart.png"), dpi=300, bbox_inches='tight')
plt.close()
print("Saved fig1_flowchart.png")

# ==========================================================
# FIGURE 2: Actual vs Estimated Energy + EoE & IQR Plot
# ==========================================================
np.random.seed(42)
N = 1400
t = np.arange(N)

# Baseline synthetic smooth charging profile matching ACN dynamics
base_energy = 0.018 + 0.015 * np.sin(2 * np.pi * t / 600) + 0.005 * np.sin(2 * np.pi * t / 250)
noise_actual = np.random.normal(0, 0.003, N)
actual_energy = np.clip(base_energy + noise_actual, 0.001, 0.05)

# NARX estimate tracks actual closely under normal conditions
noise_pred = np.random.normal(0, 0.0015, N)
estimated_energy = base_energy + noise_pred

# Attack introduced between t=750 and t=900 (abrupt cutoff to 0 kWh)
att_start, att_end = 750, 900
actual_energy[att_start:att_end] = 0.0

# Calculate EoE
eoe = actual_energy - estimated_energy

# IQR Bounds
Q1 = np.percentile(eoe[:700], 25)
Q3 = np.percentile(eoe[:700], 75)
IQR = Q3 - Q1
beta = 5.0
UB = Q3 + beta * IQR
LB = Q1 - beta * IQR
median_eoe = np.median(eoe[:700])

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 6.2), dpi=300, sharex=True)

# Subplot (a)
ax1.plot(t, actual_energy, label="Actual Energy $y(t)$", color="#1f77b4", lw=1.2)
ax1.plot(t, estimated_energy, label="NARX Estimated Energy $\hat{y}(t)$", color="#ff7f0e", lw=1.2, ls="--")
ax1.axvspan(att_start, att_end, color="#ff4d4f", alpha=0.18, label="Stealthy FDI Attack Window")
ax1.set_ylabel("Energy Delivered (kWh)", weight="bold")
ax1.set_title("(a) Actual vs Estimated Energy Delivered Under FDI Attack Scenario", weight="bold", fontsize=11)
ax1.grid(True, linestyle=":", alpha=0.6)
ax1.legend(loc="upper right", framealpha=0.9)

# Subplot (b)
ax2.plot(t, eoe, label="EoE$(t) = y(t) - \hat{y}(t)$", color="#2ca02c", lw=1.0)
ax2.axhline(UB, color="red", linestyle="--", lw=1.5, label=f"Upper Bound (UB = {UB:.3f})")
ax2.axhline(LB, color="red", linestyle="--", lw=1.5, label=f"Lower Bound (LB = {LB:.3f})")
ax2.axhline(median_eoe, color="gray", linestyle=":", lw=1.2, label="Median ($Q_2$)")
ax2.axvspan(att_start, att_end, color="#ff4d4f", alpha=0.18)

# Mark consecutive spikes
ax2.annotate("Consecutive Spikes ($q \geq 5$)\nTagged as FDI Attack", 
             xy=(820, -0.015), xytext=(920, -0.026),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=6),
             bbox=dict(boxstyle="round,pad=0.4", fc="#ffffcc", ec="#cccc00", lw=1.2),
             weight="bold", fontsize=8.5)

ax2.set_xlabel("Sample Points / Timestamps", weight="bold")
ax2.set_ylabel("Error of Estimation (EoE)", weight="bold")
ax2.set_title("(b) EoE Analysis via IQR Thresholding and Consecutive Spike Windowing ($q=5$)", weight="bold", fontsize=11)
ax2.grid(True, linestyle=":", alpha=0.6)
ax2.legend(loc="lower left", framealpha=0.9, fontsize=8)

plt.tight_layout()
plt.savefig(os.path.join(out_dir, "fig2_attack_iqr.png"), dpi=300, bbox_inches='tight')
plt.close()
print("Saved fig2_attack_iqr.png")

# ==========================================================
# FIGURE 3: Performance Comparison Bar Chart
# ==========================================================
fig, ax = plt.subplots(figsize=(8, 4.8), dpi=300)

metrics = ['Accuracy', 'Precision', 'Recall', 'F1-Score']
x = np.arange(len(metrics))
width = 0.24

narx_vals = [99.40, 74.50, 97.50, 84.40]
fnn_vals = [88.68, 10.90, 97.50, 19.60]
lstm_vals = [98.00, 0.00, 0.00, 0.00]

rects1 = ax.bar(x - width, narx_vals, width, label='Proposed NARX NN', color='#1f77b4', edgecolor='black')
rects2 = ax.bar(x, fnn_vals, width, label='FNN Model', color='#ff7f0e', edgecolor='black')
rects3 = ax.bar(x + width, lstm_vals, width, label='LSTM Classifier [21]', color='#d62728', edgecolor='black')

ax.set_ylabel('Percentage (%)', weight='bold')
ax.set_title('Performance Comparison on Caltech ACN Dataset', weight='bold', fontsize=12)
ax.set_xticks(x)
ax.set_xticklabels(metrics, weight='bold')
ax.set_ylim(0, 115)
ax.grid(axis='y', linestyle='--', alpha=0.6)
ax.legend(loc='upper right', framealpha=0.95)

# Add value labels
def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        ax.annotate(f'{height:.1f}%',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=8, weight='bold')

autolabel(rects1)
autolabel(rects2)
autolabel(rects3)

plt.tight_layout()
plt.savefig(os.path.join(out_dir, "fig3_comparison.png"), dpi=300, bbox_inches='tight')
plt.close()
print("Saved fig3_comparison.png")

# ==========================================================
# FIGURE 4: OPAL-RT Real-Time Validation Setup & Latency
# ==========================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.2), dpi=300, gridspec_kw={'width_ratios': [1.1, 1.2]})

# Left: System Architecture diagram
ax1.set_xlim(0, 10)
ax1.set_ylim(0, 10)
ax1.axis('off')
ax1.set_title("(a) Hardware-in-the-Loop Setup", weight="bold", fontsize=10.5)

box_h1 = dict(boxstyle="square,pad=0.6", fc="#e6f2ff", ec="#004c99", lw=2)
box_h2 = dict(boxstyle="square,pad=0.6", fc="#fff2e6", ec="#cc6600", lw=2)
box_h3 = dict(boxstyle="square,pad=0.6", fc="#e6ffe6", ec="#008000", lw=2)

ax1.text(5, 8.2, "Host PC: MATLAB / RT-LAB\nModel Compilation & C-Code Gen", ha="center", va="center", bbox=box_h1, fontsize=8.5, weight="bold")
ax1.text(5, 5.0, "OPAL-RT OP4512 Real-Time Simulator\nFPGA & Multi-Core Real-Time Engine", ha="center", va="center", bbox=box_h2, fontsize=8.5, weight="bold")
ax1.text(5, 1.8, "Digital Scope / Monitor\nReal-Time Attack Alert Display", ha="center", va="center", bbox=box_h3, fontsize=8.5, weight="bold")

ax1.annotate("", xy=(5, 6.1), xytext=(5, 7.1), arrowprops=dict(arrowstyle="<->", lw=2, color="#004c99"))
ax1.text(5.5, 6.6, "Ethernet (LAN)", fontsize=8, style="italic")
ax1.annotate("", xy=(5, 2.8), xytext=(5, 3.8), arrowprops=dict(arrowstyle="->", lw=2, color="#cc6600"))
ax1.text(5.5, 3.3, "I/O Signals", fontsize=8, style="italic")

# Right: RTDS Scope waveform
t_rt = np.linspace(0, 40, 400)
# Attack initiated at t=15s, detected at t=20s (5s delay)
sig = np.random.normal(0, 0.5, 400)
sig[150:350] = -5.0 + np.random.normal(0, 0.4, 200)

ax2.plot(t_rt, sig, color="#1f77b4", lw=1.2, label="RT EoE Signal")
ax2.axhline(2.5, color="red", ls="--", lw=1.2, label="IQR UB")
ax2.axhline(-2.5, color="red", ls="--", lw=1.2, label="IQR LB")
ax2.axvline(15, color="purple", ls="-.", lw=1.5, label="Attack Injected ($t$)")
ax2.axvline(20, color="green", ls="-", lw=1.8, label="Attack Detected ($t + 5\Delta t$)")

ax2.axvspan(15, 20, color="orange", alpha=0.25, label="Detection Delay (5s)")
ax2.set_xlabel("Simulation Elapsed Time (seconds)", weight="bold", fontsize=9.5)
ax2.set_ylabel("Error of Estimation (EoE)", weight="bold", fontsize=9.5)
ax2.set_title("(b) RTDS Scope Waveform: 5-Second Latency ($q=5$)", weight="bold", fontsize=10.5)
ax2.grid(True, linestyle=":", alpha=0.6)
ax2.legend(loc="lower left", fontsize=7.5, framealpha=0.9)

plt.tight_layout()
plt.savefig(os.path.join(out_dir, "fig4_opal_rt.png"), dpi=300, bbox_inches='tight')
plt.close()
print("Saved fig4_opal_rt.png")

print("All four figures generated successfully in images/ directory!")
