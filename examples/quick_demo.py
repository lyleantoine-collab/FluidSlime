# examples/quick_demo.py
from core.physarum_engine import FluidSlime
import matplotlib.pyplot as plt

slime = FluidSlime(grid_size=(300, 300), steps=1500)
slime.place_food(sources=[(50, 150), (250, 150)], sinks=[(150, 150)])
slime.spawn_agents(count=8000, sources=[(50, 150), (250, 150)])
trail = slime.run()

plt.figure(figsize=(10,10))
plt.imshow(trail, cmap='viridis')
plt.title("FluidSlime just misbehaved all over your legacy design")
plt.axis('off')
plt.show()
