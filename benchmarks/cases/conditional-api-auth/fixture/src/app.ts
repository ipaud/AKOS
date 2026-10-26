export async function buildApp(options: { apiToken?: string } = {}) {
  const app = createServer();

  if (options.apiToken) {
    app.addHook('onRequest', async (request, reply) => {
      if (request.url.startsWith('/api/') && !validToken(request, options.apiToken)) {
        return reply.status(401).send({ error: 'unauthorized' });
      }
    });
  }

  app.post('/api/settings', updateSettings);
  return app;
}
