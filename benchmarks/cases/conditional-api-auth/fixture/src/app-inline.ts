export function register(app, options) {
  if (options.apiToken) { app.addHook('onRequest', checkToken); }
  app.post('/api/settings', updateSettings);
}
