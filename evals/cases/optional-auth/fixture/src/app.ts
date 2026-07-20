import Fastify from 'fastify';
import { updateSettings } from './settings.js';

export async function buildApp(options: { apiToken?: string } = {}) {
  const app = Fastify();

  if (options.apiToken) {
    const token = options.apiToken;
    app.addHook('onRequest', async (request, reply) => {
      if (!request.url.startsWith('/api/')) return;
      const auth = request.headers.authorization ?? '';
      if (auth !== `Bearer ${token}`) {
        return reply.status(401).send({ error: 'unauthorized' });
      }
    });
  }

  // Writes provider API keys into server memory.
  app.post('/api/settings', async (request) => updateSettings(request.body));

  return app;
}
