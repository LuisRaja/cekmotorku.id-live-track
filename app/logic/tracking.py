import time
import threading

__all__ = ['TrackingManager']

class TrackingManager:
    def __init__(self, state, ws_client, on_update):
        self.state = state
        self.ws = ws_client
        self.on_update = on_update
        self._timer = None
        self._current_track_id = None

    def start(self):
        s = self.state
        s.reset()
        s.is_tracking = True
        s.is_paused = False
        s.start_time = time.time()
        s.paused_duration = 0
        s.pause_start = None
        s.touring_sheet_open = False
        self._current_track_id = f'track_{int(time.time() * 1000)}'
        self._start_timer()
        self.ws.send_status(self._current_track_id, 'tracking')
        self.on_update()

    def pause(self):
        s = self.state
        if not s.is_tracking:
            return
        if s.is_paused:
            if s.pause_start:
                s.paused_duration += time.time() - s.pause_start
            s.pause_start = None
            s.is_paused = False
        else:
            s.pause_start = time.time()
            s.is_paused = True
        self.on_update()

    def stop(self):
        s = self.state
        if not s.is_tracking and not s.is_paused:
            return
        s.is_tracking = False
        s.is_paused = False
        s.is_finished = True
        self._stop_timer()
        self.ws.send_status(self._current_track_id, 'finished')
        self.on_update()

    def on_gps_position(self, lat, lng, speed, altitude):
        s = self.state
        if not s.is_tracking or s.is_paused:
            return
        s.add_position(lat, lng, speed)
        if altitude is not None:
            s.altitude = altitude
        self.ws.send_point(self._current_track_id, lat, lng, speed)
        self.on_update()

    def on_orientation(self, gamma):
        from logic.sensors import SensorManager
        pass

    def on_acceleration(self, x, y, z):
        pass

    def _start_timer(self):
        self._stop_timer()
        self._timer = threading.Thread(target=self._timer_loop, daemon=True)
        self._timer.start()

    def _stop_timer(self):
        if self._timer:
            self._timer = None

    def _timer_loop(self):
        while self._timer and self.state.is_tracking:
            time.sleep(1)
            if self.state.is_paused:
                continue
            now = time.time()
            elapsed = now - self.state.start_time
            if self.state.pause_start:
                elapsed -= now - self.state.pause_start
            if self.state.paused_duration > 0:
                elapsed -= self.state.paused_duration
            self.state.elapsed_seconds = max(0, int(elapsed))
            self.on_update()
