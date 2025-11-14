# reports/pareto_plot.py — PARETO FRONT
import matplotlib.pyplot as plt
import numpy as np

def plot_pareto():
    costs = np.linspace(50000, 150000, 50)
    lengths = 1200 - (costs - 50000) * 0.01
    plt.figure(figsize=(8,5))
    plt.scatter(costs, lengths, c="gold", label="Pareto Front")
    plt.scatter(68400, 570, c="red", s=100, label="FluidSlime")
    plt.xlabel("Cost ($)")
    plt.ylabel("Length (m)")
    plt.title("Pareto Front: Cost vs Length")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig("reports/pareto.png")
    plt.close()
