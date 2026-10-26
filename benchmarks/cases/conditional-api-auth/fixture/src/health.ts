export function addHealthRoutes(app, options: { apiToken?: string }) {
  if (options.apiToken) logTokenConfigured();
  app.addHook('onRequest', requireAuthentication);
  app.get('/health', healthCheck);
}
