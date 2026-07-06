import db from '../db.js';

function calcDist(lat1, lon1, lat2, lon2) {
  const R = 6371000;
  const dLat = (lat2 - lat1) * Math.PI / 180;
  const dLon = (lon2 - lon1) * Math.PI / 180;
  const a = Math.sin(dLat / 2) ** 2 +
    Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) * Math.sin(dLon / 2) ** 2;
  return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
}

export function setupSocket(io) {
  io.on('connection', (socket) => {
    console.log('[WS] Connected:', socket.id);

    socket.on('track:join', (trackId) => {
      socket.join(`track:${trackId}`);
      socket.trackId = trackId;
      console.log(`[WS] ${socket.id} joined track:${trackId}`);
    });

    socket.on('track:leave', (trackId) => {
      socket.leave(`track:${trackId}`);
    });

    socket.on('track:status', (data) => {
      const { trackId, status } = data;
      if (!trackId || !status) return;
      try {
        const stmt = db.prepare("UPDATE tracks SET status = ?, finished_at = CASE WHEN ? = 'finished' THEN datetime('now') ELSE finished_at END WHERE id = ?");

        if (status === 'finished') {
          // Hitung statistik
          const points = db.prepare(
            'SELECT lat, lng, speed, recorded_at FROM track_points WHERE track_id = ? ORDER BY point_index ASC'
          ).all(trackId);

          let totalDist = 0;
          let maxSpd = 0;
          let sumSpd = 0;
          const speeds = [];

          if (points.length > 0) {
            for (let i = 1; i < points.length; i++) {
              totalDist += calcDist(points[i - 1].lat, points[i - 1].lng, points[i].lat, points[i].lng);
            }
            points.forEach(p => { if (p.speed > 0) speeds.push(p.speed); });
            if (speeds.length > 0) {
              maxSpd = Math.max(...speeds);
              sumSpd = speeds.reduce((a, b) => a + b, 0) / speeds.length;
            }
            const start = new Date(points[0].recorded_at).getTime();
            const end = new Date(points[points.length - 1].recorded_at).getTime();
            const dur = (end - start) / 1000;

            db.prepare(`
              UPDATE tracks SET status = 'finished', finished_at = datetime('now'),
                total_distance = ?, max_speed = ?, avg_speed = ?, duration_seconds = ?
              WHERE id = ?
            `).run(totalDist, maxSpd, sumSpd, dur, trackId);
          } else {
            stmt.run('finished', 'finished', trackId);
          }
        } else {
          db.prepare("UPDATE tracks SET status = ? WHERE id = ?").run(status, trackId);
        }

        const track = db.prepare('SELECT * FROM tracks WHERE id = ?').get(trackId);
        io.to(`track:${trackId}`).emit('track:updated', track);
      } catch (err) {
        socket.emit('track:error', { message: err.message });
      }
    });

    socket.on('track:point', (data) => {
      const { trackId, lat, lng, speed, accuracy, heading } = data;
      if (!trackId || lat == null || lng == null) return;
      try {
        const row = db.prepare(
          'SELECT COALESCE(MAX(point_index), -1) + 1 AS next_idx FROM track_points WHERE track_id = ?'
        ).get(trackId);
        const pointIndex = row.next_idx;

        db.prepare(`
          INSERT INTO track_points (track_id, lat, lng, speed, accuracy, heading, point_index)
          VALUES (?, ?, ?, ?, ?, ?, ?)
        `).run(trackId, lat, lng, speed || 0, accuracy || 0, heading || 0, pointIndex);

        db.prepare("UPDATE tracks SET status = 'tracking' WHERE id = ? AND status = 'idle'").run(trackId);

        io.to(`track:${trackId}`).emit('track:point', {
          lat, lng, speed: speed || 0, accuracy: accuracy || 0,
          heading: heading || 0, point_index: pointIndex,
          recorded_at: new Date().toISOString(),
        });
      } catch (err) {
        socket.emit('track:error', { message: err.message });
      }
    });

    socket.on('disconnect', () => {
      console.log('[WS] Disconnected:', socket.id);
    });
  });
}
