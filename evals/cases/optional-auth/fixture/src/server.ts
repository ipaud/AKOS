import { loadConfig } from './env.js';
import { buildApp } from './app.js';

const config = loadConfig();
const app = await buildApp({ apiToken: config.API_TOKEN });
await app.listen({ port: config.PORT, host: '0.0.0.0' });
