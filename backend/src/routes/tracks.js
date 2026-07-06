import { Router } from 'express';
import db from '../db.js';
import { v4 as uuidv4 } from 'uuid';

const router = Router();

function calcDist(lat1, lon1, lat2, lon2) {
  const R = 6371000;
  const dLat = (lat2 - lat1) * Math.PI / 180;
  const dLon = (lon2 - lon1) * Math.PI / 180;
  const a = Math.sin(dLat / 2) ** 2 +
    Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) * Math.sin(dLon / 2) ** 2;
  return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
}

// GET /api/tracks
router.get('/', (req, res) => {
  try {
    const limit = Math.min(parseInt(req.query.limit) || 50, 200);
    const offset = parseInt(req.query.offset) || 0;
    const rows = db.prepare(`
      SELECT t.*,
        (SELECT COUNT(*) FROM track_points WHERE track_id = t.id) AS point_count
      FROM tracks t ORDER BY t.created_at DESC LIMIT ? OFFSET ?
    `).all(limit, offset);
    res.json(rows);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// POST /api/tracks
router.post('/', (req, res) => {
  try {
    const { name, motor } = req.body || {};
    const id = uuidv4();
    db.prepare(`INSERT INTO tracks (id, name, motor, status) VALUES (?, ?, ?, 'idle')`).run(id, name || 'Untitled', motor || '');
    const track = db.prepare('SELECT * FROM tracks WHERE id = ?').get(id);
    res.status(201).json(track);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// GET /api/tracks/:id
router.get('/:id', (req, res) => {
  try {
    const track = db.prepare(`
      SELECT t.*,
        (SELECT COUNT(*) FROM track_points WHERE track_id = t.id) AS point_count
      FROM tracks t WHERE t.id = ?
    `).get(req.params.id);
    if (!track) return res.status(404).json({ error: 'Track not found' });
    res.json(track);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// PATCH /api/tracks/:id
router.patch('/:id', (req, res) => {
  try {
    const { name, motor, status } = req.body || {};
    const sets = [];
    const params = [];

    if (name !== undefined) { sets.push('name = ?'); params.push(name); }
    if (motor !== undefined) { sets.push('motor = ?'); params.push(motor); }
    if (status !== undefined) {
      sets.push('status = ?');
      params.push(status);
      if (status === 'finished') {
        sets.push("finished_at = datetime('now')");

        // Hitung stat dari semua titik
        const points = db.prepare(
          'SELECT lat, lng, speed, recorded_at FROM track_points WHERE track_id = ? ORDER BY point_index ASC'
        ).all(req.params.id);

        let totalDist = 0;
        let maxSpd = 0;
        let sumSpd = 0;

        if (points.length > 0) {
          for (let i = 1; i < points.length; i++) {
            totalDist += calcDist(points[i - 1].lat, points[i - 1].lng, points[i].lat, points[i].lng);
          }
          const speeds = points.map(p => p.speed).filter(s => s > 0);
          if (speeds.length > 0) {
            maxSpd = Math.max(...speeds);
            sumSpd = speeds.reduce((a, b) => a + b, 0) / speeds.length;
          }
          const start = new Date(points[0].recorded_at).getTime();
          const end = new Date(points[points.length - 1].recorded_at).getTime();
          const dur = (end - start) / 1000;

          sets.push('total_distance = ?'); params.push(totalDist);
          sets.push('max_speed = ?'); params.push(maxSpd);
          sets.push('avg_speed = ?'); params.push(sumSpd);
          sets.push('duration_seconds = ?'); params.push(dur);
        }
      }
    }

    if (sets.length === 0) return res.status(400).json({ error: 'No fields to update' });

    params.push(req.params.id);
    db.prepare(`UPDATE tracks SET ${sets.join(', ')} WHERE id = ?`).run(...params);

    const track = db.prepare('SELECT * FROM tracks WHERE id = ?').get(req.params.id);
    if (!track) return res.status(404).json({ error: 'Track not found' });
    res.json(track);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// DELETE /api/tracks/:id
router.delete('/:id', (req, res) => {
  try {
    const result = db.prepare('DELETE FROM tracks WHERE id = ?').run(req.params.id);
    if (result.changes === 0) return res.status(404).json({ error: 'Track not found' });
    res.json({ deleted: true });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// GET /api/tracks/:id/points
router.get('/:id/points', (req, res) => {
  try {
    const points = db.prepare(
      'SELECT id, lat, lng, speed, accuracy, heading, recorded_at, point_index FROM track_points WHERE track_id = ? ORDER BY point_index ASC'
    ).all(req.params.id);
    res.json(points);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// GET /api/tracks/:id/stats
router.get('/:id/stats', (req, res) => {
  try {
    const points = db.prepare(
      'SELECT lat, lng, speed, recorded_at FROM track_points WHERE track_id = ? ORDER BY point_index ASC'
    ).all(req.params.id);

    if (points.length === 0) {
      return res.json({ point_count: 0, total_distance: 0, max_speed: 0, avg_speed: 0, duration_seconds: 0 });
    }

    let totalDist = 0;
    let maxSpd = 0;
    let sumSpd = 0;
    const speeds = [];

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

    res.json({
      point_count: points.length,
      total_distance: totalDist,
      max_speed: maxSpd,
      avg_speed: sumSpd,
      start_time: points[0].recorded_at,
      end_time: points[points.length - 1].recorded_at,
      duration_seconds: (end - start) / 1000,
    });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

export default router;
