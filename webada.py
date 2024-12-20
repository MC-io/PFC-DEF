import numpy as np
import matplotlib.pyplot as plt

# Example: Simulated hypervolume values over generations
generations = np.arange(1, 301)  # 100 generations
hypervolume_values = np.random.uniform(0.7, 1.0, len(generations))  # Simulated values

# Plot the hypervolume convergence
plt.figure(figsize=(10, 6))
plt.plot(generations, hypervolume_values, label="Hypervolume", color="blue", marker="o")
plt.title("Convergence Plot: Hypervolume Indicator")
plt.xlabel("Generation")
plt.ylabel("Hypervolume")
plt.grid(True)
plt.legend()
plt.show()