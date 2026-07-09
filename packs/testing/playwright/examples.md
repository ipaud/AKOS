# Examples — Playwright Pack

## Auto-waiting locator vs sleep

Bad: `await page.click('.submit-btn'); await page.waitForTimeout(1000); expect(...)`.
Good: `await page.getByRole('button', { name: 'Submit' }).click(); await expect(page.getByText('Order confirmed')).toBeVisible();`

## Resilient selector

Bad: `page.locator('div.css-x7f3a > span:nth-child(2)')`
Good: `page.getByRole('link', { name: 'View invoice' })`

## Isolated test with API-seeded data

```ts
test('user can cancel their subscription', async ({ page, request }) => {
  const user = await request.post('/api/test/seed-user', { data: { plan: 'pro' } });
  await page.goto(`/login?as=${user.id}`);
  await page.getByRole('button', { name: 'Cancel subscription' }).click();
  await expect(page.getByText('Subscription canceled')).toBeVisible();
});
```

## Trace on failure config

```ts
// playwright.config.ts
use: { trace: 'retain-on-failure', video: 'retain-on-failure' }
```
