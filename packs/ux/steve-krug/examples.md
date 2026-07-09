# Examples — Krug Pack

Invented cases. Bad → good, with the principle applied.

## Button labels (P10, ER15)

| Bad | Good | Why |
|-----|------|-----|
| `Submit` | `Create account` | Says what happens, not what the form technically does |
| `OK` (in delete dialog) | `Delete 3 photos` | Restates the consequence at the moment of commitment |
| `Continue` | `Continue to payment` | Names the destination — no leap of faith |
| `Ignite your journey` | `Start free trial` | User vocabulary beats brand poetry |
| `Manage preferences center` | `Notification settings` | The word the user would search for |

## Link text (ER16)

- Bad: `To read our shipping policy, click here.`
- Good: `Shipping policy` (linked noun, works out of context, scannable)

## Navigation labels (P5, anti-pattern "clever labels")

| Bad | Good |
|-----|------|
| Solutions | Products |
| My Universe | Account |
| Engage | Contact |
| Resources (mixed bag) | Docs · Blog · Support (split by actual content) |

## Homepage tagline (P9)

- Bad: `Welcome! We're passionate about empowering seamless experiences.`
- Good: `Track every subscription you pay for — and cancel the ones you forgot.`
- Test: could a competitor use the sentence unchanged? Bad one, yes → says nothing.

## Copy reduction (P10)

Before (34 words):
> In order to get started with creating your very first project, all you need to do is simply click on the "New Project" button which is located in the upper right corner.

After (0 words): make the New Project button visually dominant on the empty state. If text is still needed: **"Create your first project →"** (4 words, placed on the empty state itself).

## Form friction (ER20, ER23)

Bad: card number field rejecting spaces; separate "confirm email" field; mandatory phone for a newsletter.
Good: input strips spaces silently; email typed once (typo risk handled by verification email anyway); newsletter asks for email only.

## Error messages (ER17)

- Bad: `Error 422: Unprocessable entity.`
- Good: `That coupon expired on May 1. Remove it to continue, or use a current code.`
- Structure: what happened → why → what to do.

## Empty states (ER25)

- Bad: blank table, no rows, no text.
- Good: `No invoices yet. They'll appear here after your first billing cycle — or import past invoices.` (orientation + next action)

## Trunk test fix (P8)

Symptom: user lands on `/docs/webhooks/retries` from search. Page shows only prose.
Fix: page `<h1>Webhook retries</h1>`, breadcrumb `Docs > Webhooks > Retries`, sidebar with Webhooks section expanded and current page highlighted, logo linking home.

## "Do the least" fix sizing (P13)

Observed: test users can't find export.
- Redesign reflex: rebuild the toolbar system (3 weeks).
- Least-you-can-do: rename icon-only button to `Export CSV` with visible text (30 minutes). Re-test; escalate only if it still fails.
