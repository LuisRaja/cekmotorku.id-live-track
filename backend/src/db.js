import Database from 'better-sqlite3';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import { existsSync, mkdirSync } from 'fs';

const __dirname = dirname(fileURLToPath(import.meta.url));
const dbDir = join(__dirname, '..', 'data');
if (!existsSync(dbDir)) mkdirSync(dbDir, { recursive: true });

const dbPath = join(dbDir, 'cekmotormu.db');
const db = new Database(dbPath);

// WAL mode untuk performa concurrent lebih baik
db.pragma('journal_mode = WAL');
db.pragma('foreign_keys = ON');

export default db;
