CREATE TABLE IF NOT EXISTS tracks (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL DEFAULT 'Untitled',
    motor TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'idle'
        CHECK (status IN ('idle','tracking','paused','finished')),
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    finished_at TEXT,
    total_distance REAL NOT NULL DEFAULT 0,
    max_speed REAL NOT NULL DEFAULT 0,
    avg_speed REAL NOT NULL DEFAULT 0,
    duration_seconds REAL NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS track_points (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    track_id TEXT NOT NULL REFERENCES tracks(id) ON DELETE CASCADE,
    lat REAL NOT NULL,
    lng REAL NOT NULL,
    speed REAL NOT NULL DEFAULT 0,
    accuracy REAL NOT NULL DEFAULT 0,
    heading REAL NOT NULL DEFAULT 0,
    recorded_at TEXT NOT NULL DEFAULT (datetime('now')),
    point_index INTEGER NOT NULL DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_track_points_track_id
    ON track_points(track_id);

CREATE INDEX IF NOT EXISTS idx_track_points_index
    ON track_points(track_id, point_index);

CREATE INDEX IF NOT EXISTS idx_tracks_status
    ON tracks(status);
