# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "matplot",
# ]
# ///
import matplotlib.pyplot as plt

# Create a simple diagram for Hyper-V partitions
fig, ax = plt.subplots(figsize=(8,6))

# Draw hardware box
ax.add_patch(plt.Rectangle((0,0), 8, 1, edgecolor="black", facecolor="#d9ead3"))
ax.text(4, 0.5, "Hardware (CPU, Memory, Devices)", ha="center", va="center", fontsize=10, weight="bold")

# Draw Hyper-V box
ax.add_patch(plt.Rectangle((0,1), 8, 0.7, edgecolor="black", facecolor="#b6d7a8"))
ax.text(4, 1.35, "Hyper-V Hypervisor\n(Type-1, owns the hardware)", ha="center", va="center", fontsize=10)

# Draw Parent Partition (Windows 11)
ax.add_patch(plt.Rectangle((0,1.7), 8, 1.5, edgecolor="black", facecolor="#cfe2f3"))
ax.text(4, 2.45, "Parent Partition (Windows 11)\n- Runs drivers for real hardware\n- Manages child partitions\n- Privileged access", 
        ha="center", va="center", fontsize=9)

# Draw Child Partitions
ax.add_patch(plt.Rectangle((0,3.2), 3.9, 1.2, edgecolor="black", facecolor="#f9cb9c"))
ax.text(1.95, 3.8, "Child Partition\n(Ubuntu VM)", ha="center", va="center", fontsize=9)

ax.add_patch(plt.Rectangle((4.1,3.2), 3.9, 1.2, edgecolor="black", facecolor="#fce5cd"))
ax.text(6.05, 3.8, "Child Partition\n(Other VM)", ha="center", va="center", fontsize=9)

# Formatting
ax.set_xlim(0,8)
ax.set_ylim(0,4.6)
ax.axis("off")

plt.title("Hyper-V Architecture: Parent and Child Partitions", fontsize=12, weight="bold")
plt.show()

