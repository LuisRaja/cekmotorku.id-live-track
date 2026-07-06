import express from 'express';
import { createServer } from 'http';
import { Server } from 'socket.io';
import cors from 'cors';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import { config } from './config.js';
import tracksRouter from './routes/tracks.js';
import { setupSocket } from './socket/handler.js';

const __dirname = dirname(fileURLToPath(import.meta.url));

const app = express();
const httpServer = createServer(app);
const io = new Server(httpServer, {
  cors: { origin: config.corsOrigin, methods: ['GET', 'POST'] },
  pingInterval: 10000,
  pingTimeout: 5000,
});

app.use(cors({ origin: config.corsOrigin }));
app.use(express.json());

// Serve frontend static files (fixes file:// origin issues)
app.use(express.static(join(__dirname, '..', '..')));

app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', uptime: process.uptime() });
});

app.use('/api/tracks', tracksRouter);

setupSocket(io);

httpServer.listen(config.port, () => {
  console.log(`[Server] cekMotormu.id backend running on port ${config.port}`);
  console.log(`[Server] REST API: http://localhost:${config.port}/api`);
  console.log(`[Server] WebSocket: ws://localhost:${config.port}`);
});
