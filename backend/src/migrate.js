import { readFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import db from './db.js';

const __dirname = dirname(fileURLToPath(import.meta.url));

function migrate() {
  console.log('[Migrate] Starting...');
  const sql = readFileSync(join(__dirname, 'migrations', '001_init.sql'), 'utf-8');
  db.exec(sql);
  console.log('[Migrate] Success');
}

migrate();
