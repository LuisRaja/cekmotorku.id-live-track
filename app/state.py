from .utils.helpers import haversine, format_time

class AppState:
    def __init__(self):
        self.reset()

    def reset(self):
        self.is_tracking = False
        self.is_paused = False
        self.is_finished = False
        self.mode = 'speed'

        self.coordinates = []
        self.speeds = []
        self.total_distance = 0.0
        self.top_speed = 0
        self.current_speed = 0

        self.start_time = 0
        self.paused_duration = 0
        self.pause_start = None
        self.elapsed_seconds = 0

        self.current_lat = None
        self.current_lng = None

        self.lean_angle = 0
        self.g_force = 0.0
        self.altitude = None

        self.touring_sheet_open = True

        self.form_data = {
            'route': '',
            'motor': '',
            'odometer': '',
            'notes': '',
            'photo_path': None,
        }

    def add_position(self, lat, lng, speed_kmh):
        if self.coordinates:
            last = self.coordinates[-1]
            dist = haversine(last[0], last[1], lat, lng)
            if dist > 0.003:
                self.total_distance += dist

        self.coordinates.append((lat, lng))
        self.speeds.append(speed_kmh)
        self.current_lat = lat
        self.current_lng = lng

        speed_int = int(speed_kmh)
        self.current_speed = speed_int
        if speed_int > self.top_speed:
            self.top_speed = speed_int

    def get_stats(self):
        return {
            'speed': self.current_speed,
            'top_speed': self.top_speed,
            'distance': round(self.total_distance, 2),
            'time': format_time(self.elapsed_seconds),
        }

    def get_avg_speed(self):
        valid = [s for s in self.speeds if s > 0]
        if not valid:
            return 0.0
        return round(sum(valid) / len(valid), 1)
