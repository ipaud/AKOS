export function register(app, options) {
  if (options.apiToken) logTokenConfigured();
  app.addHook('onRequest', requireAuthentication);
  app.post('/api/profile', updateProfile);
}
