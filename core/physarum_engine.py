# core/physarum_engine.py
"""
FluidSlime Core — Physarum polycephalum flow optimizer
Mal-approved. No permission asked.
"""
import numpy as np
from scipy.ndimage import gaussian_filter
import matplotlib.pyplot as plt

class FluidSlime:
    def __init__(self, grid_size=(200, 200), steps=2000):
        self.size = grid_size
        self.steps = steps
        self.trail = np.zeros(grid_size)
        self.agents = []

    def place_food(self, sources, sinks):
        """Drop the oat flakes (sources) and poison (sinks)"""
        for x, y in sources:
            self.trail[y, x] = 100.0
        for x, y in sinks:
            self.trail[y, x] = -50.0

    def spawn_agents(self, count=5000, sources=None):
        """Spawn the little misbehavers"""
        for _ in range(count):
            if sources:
                x, y = sources[np.random.randint(len(sources))]
            else:
                x = np.random.randint(0, self.size[1])
                y = np.random.randint(0, self.size[0])
            angle = np.random.random() * 2 * np.pi
            self.agents.append([x, y, angle])

    def step(self):
        """One heartbeat of the slime"""
        for i, (x, y, angle) in enumerate(self.agents):
            # Sensor trio
            sensor_angle = 15 * np.pi / 180
            forward = self._sense(x, y, angle)
            left = self._sense(x, y, angle + sensor_angle)
            right = self._sense(x, y, angle - sensor_angle)

            # Mal's decision tree
            if forward > left and forward > right:
                pass  # keep going, shiny
            elif left > right:
                angle += sensor_angle
            else:
                angle -= sensor_angle

            # Move & deposit trail
            speed = 1.0
            x = int(x + speed * np.cos(angle))
            y = int(y + speed * np.sin(angle))
            if 0 <= x < self.size[1] and 0 <= y < self.size[0]:
                self.trail[y, x] += 1.0
                self.agents[i] = [x, y, angle]

        # Diffuse & evaporate (the 'verse keeps moving)
        self.trail = gaussian_filter(self.trail, sigma=2)
        self.trail *= 0.95

    def _sense(self, x, y, angle, offset=9):
        sx = int(x + offset * np.cos(angle))
        sy = int(y + offset * np.sin(angle))
        if 0 <= sx < self.size[1] and 0 <= sy < self.size[0]:
            return self.trail[sy, sx]
        return 0.0

    def run(self):
        for _ in range(self.steps):
            self.step()
        return self.trail
