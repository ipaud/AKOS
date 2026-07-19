# Examples — GOV.UK Content Design Pack

Invented cases throughout. Fictional organisations: **Bellcastle Council**, the **Coastal Licensing Authority**, **Northgate Health Trust**.

## Front-loading the page (GC5, GCE10)

**Before**

> Bellcastle Council is committed to supporting residents in managing their parking arrangements. As part of our ongoing modernisation programme, we have introduced a range of improvements to the way permits are administered. This page provides information relating to the renewal of residents' parking permits.

**After**

> Renew your resident parking permit online. It takes about 5 minutes and costs £42 for 12 months.

The first version says nothing a reader needs. Deleting it loses no information — the test in GCE10.

## Titles (GC13, GCE13)

| Before | After | Why |
|--------|-------|-----|
| Parking permit information | Renew a resident parking permit | Names the task, verb-led, front-loaded |
| About the Coastal Licensing Authority's shellfish framework | Apply for a shellfish harvesting licence | The reader wants the licence, not the framework |
| Further guidance on eligibility criteria | Check if you can get a shellfish licence | Uses the words a person would type |
| Northgate Health Trust — Outpatient Appointment Attendance Information | Change or cancel your outpatient appointment | Two real tasks, named |

## The hidden actor (GC8, GCE8)

| Before (passive) | After (actor named) |
|------------------|---------------------|
| Applications will be assessed in due course. | We assess applications within 10 working days. |
| Supporting documents must be provided. | You must send 2 documents: proof of address and your vehicle registration. |
| Payment will be taken once approval has been granted. | We take payment after we approve your application. |
| Non-compliance may result in the licence being revoked. | We can cancel your licence if you fish outside your allocated zone. |

The first column is not merely stiff. In each row the reader cannot tell whether they have a job to do.

## Prose that should be steps (GC7, GCE15)

**Before**

> To renew, you will first need to locate your existing permit number, which can be found on your current permit. Following this, you should sign in to your account, after which the renewal option can be selected. Payment is then required to complete the process.

**After**

> To renew your permit:
>
> 1. Find your permit number — it is printed on the top right of your current permit.
> 2. Sign in to your Bellcastle account.
> 3. Select **Renew permit**.
> 4. Pay £42 by card.
>
> You will get a confirmation email within 1 hour.

## Prose that should be a table (GCE16)

**Before**

> Standard permits cost £42 per year and allow parking in zones A and B. Visitor permits cost £15 for 10 days and are valid in zone A only. Business permits are £180 per year, cover all zones, and require proof of trading address.

**After**

| Permit | Cost | Zones | Extra requirement |
|--------|------|-------|-------------------|
| Standard | £42 a year | A and B | None |
| Visitor | £15 for 10 days | A only | None |
| Business | £180 a year | All | Proof of trading address |

The reader was going to build this table anyway.

## Nested conditionals that should branch (GCE22)

**Before**

> You may be eligible if you reside within the zone, unless your property was constructed after 2016, in which case eligibility applies only where no off-street parking was provided, except for conversions, which are treated as pre-2016 properties.

**After**

> **Check if you can get a permit**
>
> You can get a permit if you live in zone A or B **and** your home has no driveway or garage.
>
> If your home was built after 2016, you can only get a permit if the developer did not provide off-street parking.
>
> Converted buildings count as built before 2016, whatever the conversion date.

Same facts, three short statements, no clause nesting. Better still on a high-traffic page: a 3-question eligibility checker.

## Jargon laundering vs real content design (GC4)

**Original:** *Applicants must submit evidentiary documentation substantiating their residential status prior to the commencement of the assessment process.*

**Laundered (still failing):** *Applicants need to provide supporting documentation confirming their residential status before the assessment process begins.* — synonyms swapped, reading age barely moved, reader still does not know what to send.

**Content designed:** *Send us 1 document that shows your address, such as a council tax bill or tenancy agreement. We cannot start your application until we get it.*

The fix was not vocabulary. It was answering the question the reader actually had: *which document, and what happens if I do not send it?*

## Metaphor removal (GCE25)

- Before: *We are on a journey to unlock a seamless licensing ecosystem for our coastal partners.*
- After: *From 6 April 2026 you can apply for all 3 licence types in one form.*

## Formal filler (GCE26)

| Before | After |
|--------|-------|
| in order to renew | to renew |
| prior to 1 May | before 1 May |
| please note that the office is closed on Mondays | the office is closed on Mondays |
| in the event that your permit expires | if your permit expires |
| we will endeavour to respond | we reply within 5 working days |

The last row is the important one: the filler was hiding the absence of a commitment.

## Link text (GCE31)

- Before: *For more information about the appeals process, click here.*
- After: *Appeal a refused permit application* — front-loaded, works out of context, survives a screen reader's link list.

## Retiring content (GC15, GCE40)

Bellcastle has 4 pages about the old paper permit scheme, ended in 2024. Traffic is negligible, no owner, one page still shows the withdrawn £30 fee.

- Wrong: leave them; they "might be useful for reference".
- Also wrong: delete them, producing 404s from search results and old emails.
- Right: redirect all 4 to *Renew a resident parking permit*, record the reason and date in the page log. If the historic fee genuinely matters to a live dispute, it belongs in one archived page clearly marked as no longer in use.

## Post-launch iteration (GC16)

One month after launch, search logs show people arriving on the renewal page typing *"parking permit moved house"* and bouncing. The page never mentions moving.

- Smallest fix that meets the need: add a section **"If you have moved"** with the 2-step process, and a task page if volume justifies it.
- Not the fix: rewriting the page, or adding an FAQ entry somewhere else.
