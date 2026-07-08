import socketio

class WSClient:
    def __init__(self, url='http://localhost:4000'):
        self.url = url
        self.sio = socketio.Client()
        self.connected = False

    def connect(self):
        if self.connected:
            return
        try:
            self.sio.connect(self.url, transports=['websocket'], wait_timeout=5)
            self.connected = True
        except Exception:
            self.connected = False

    def send_point(self, track_id, lat, lng, speed):
        if not self.connected:
            return
        try:
            self.sio.emit('track:point', {
                'trackId': track_id,
                'latitude': lat,
                'longitude': lng,
                'speed': speed,
            })
        except Exception:
            pass

    def send_status(self, track_id, status):
        if not self.connected:
            return
        try:
            self.sio.emit('track:status', {
                'trackId': track_id,
                'status': status,
            })
        except Exception:
            pass

    def disconnect(self):
        if self.connected:
            try:
                self.sio.disconnect()
            except Exception:
                pass
            self.connected = False
