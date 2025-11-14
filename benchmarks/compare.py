import matplotlib.pyplot as plt
from src.core.slime import run_slime_optimizer
# Fake data
lengths = [1200, 1500, 1100]  # Slime, Straight, NSGA
plt.bar(['Slime', 'Straight', 'NSGA'], lengths)
plt.title('Cost Savings')
plt.savefig('benchmarks/savings.png')
