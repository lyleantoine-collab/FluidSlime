# core/vascular_engine.py (dropping now)
class VascularSlime(FluidSlime):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.curvature_weight = 0.3   # NEW: hates sharp turns like nature does
    
    def step(self):
        for i, (x, y, angle) in enumerate(self.agents):
            # ... same sensors ...
            # NEW: penalize sudden direction changes
            turn_penalty = abs(self.agents[i][2] - angle) * self.curvature_weight
            forward -= turn_penalty
            # rest same as before
