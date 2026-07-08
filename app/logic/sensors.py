import math

__all__ = ['SensorManager']

class SensorManager:
    def __init__(self, state):
        self.state = state
        self._lean_filter = 0.0
        self._g_filter = 0.0
        self._active = False

    def start(self):
        self._active = True

    def stop(self):
        self._active = False

    def on_orientation(self, gamma):
        if not self._active:
            return
        if gamma is None:
            return
        raw = abs(gamma)
        alpha = 0.3
        self._lean_filter += alpha * (raw - self._lean_filter)
        self.state.lean_angle = round(self._lean_filter)

    def on_acceleration(self, x, y, z):
        if not self._active:
            return
        raw = math.sqrt(x * x + y * y + z * z)
        g = raw / 9.80665
        alpha = 0.3
        self._g_filter = alpha * g + (1 - alpha) * self._g_filter
        self.state.g_force = round(self._g_filter, 2)
