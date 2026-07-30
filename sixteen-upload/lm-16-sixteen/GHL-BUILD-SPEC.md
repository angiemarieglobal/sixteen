# SIXTEEN · GHL BUILD SPEC
## Lead magnet 16 | keyword 16 | Angie Marie Global
### Built 30 July 2026

Everything a VA needs to wire this up without asking a question. Nothing in here invents
a price, a date or a route. Routing comes from amg-ecosystem and nowhere else.

---

## 1. THE FUNNEL, END TO END

```
Social content, one keyword, four posts minimum per fortnight
   -> comment 16
   -> ManyChat DM: the link
   -> /sixteen                     opt-in, email captured in GHL
   -> GHL redirects to /sixteen/thank-you/
        download button, the three start-here steps, the audit CTA,
        and the two upsells: Recognise, then the membership
   -> delivery email               the PDF attached and linked
   -> PDF page 20 and thank-you    both route to the FREE Baseline Audit
   -> day three email              offers Recognise
   -> Recognise buyers             flow to the Baseline Membership nurture
```

**GHL does exactly one job in this funnel.** Capture the lead and send the email. Every page
is static and served by GitHub Pages from `docs/sixteen/`, so the only thing that can break
mid-launch is the form itself. Test that and you have tested the funnel.

**The pages are generated, not hand written.** Editing the HTML in `docs/` directly will be
overwritten on the next build. Words and URLs live in `build/funnel_content.py`.

Two asks, two moments, neither one crowded. The PDF asks for nothing but the audit. The
paid ask waits three days and arrives on its own.

**Why email delivery and not an instant download.** The redirect gives them the file and
teaches them nothing about opening your emails. The delivery email confirms the address,
lands in the inbox, and trains the open. Every asset after this one depends on that habit.

---

## 2. THE KEYWORD

| Keyword | Routes to | Window |
|---|---|---|
| **16** | the Sixteen landing page, `/sixteen` | Evergreen, always live |

Numeric, matching **22**, which is the pattern now established for AMG offers and assets.
Short, unmistakable in a comment thread, and impossible to mistype.

**Add this row to the capture table in amg-ecosystem.** Until that re-lock happens, this
file is the only place keyword 16 is recorded, and that is a single point of failure.

**The keyword series rule applies.** One keyword runs across a minimum of four posts per
fortnight to the same asset. Do not invent a fresh ask per piece. Recognition of the
keyword is itself the asset.

---

## 3. TAG ARCHITECTURE

Three tags on every lead, always. Without all three you cannot tell which asset built the
list and which one just made noise.

| Tag | Values | Job |
|---|---|---|
| `lm-sixteen` | fixed | Which magnet. Never reused by another asset. |
| `doorway-baseline` | fixed | Which doorway this lead entered through. |
| `src-{source}` | `src-ig-reel`, `src-ig-carousel`, `src-fb`, `src-email`, `src-substack`, `src-bio`, `src-direct` | Which piece of content sent them. |

The landing page stamps `src-` automatically from `?src=` or `?utm_source=` in the URL, so
every link you publish carries its own attribution.

**Link format for each platform:**

```
Instagram reel DM      angiemarieglobal.com/sixteen?src=ig-reel
Instagram carousel DM  angiemarieglobal.com/sixteen?src=ig-carousel
Facebook               angiemarieglobal.com/sixteen?src=fb
Email or Substack      angiemarieglobal.com/sixteen?src=email
Link in bio            angiemarieglobal.com/sixteen?src=bio
```

Behaviour tags applied later by the workflow:

| Tag | Applied when |
|---|---|
| `lm16-delivered` | The delivery email sends. |
| `lm16-opened` | They open the delivery email. |
| `audit-started` | They land on `/baseline-audit` from this funnel. |
| `audit-complete` | They finish the audit. |
| `recognise-offered` | The day three email sends. |
| `recognise-buyer` | They purchase Recognise. |

---

## 4. THE GHL BUILD, IN ORDER

**Step one. Custom field.** Create a text field `lm_source` on the contact record. The form
writes the `source` value into it, so the tag and the field agree.

**Step two. The form.** Name it `LM 16 · Sixteen`. Two visible fields, first name and
email, both required. Three hidden fields: `tags`, `source`, `lm_source`. On submit, apply
`lm-sixteen` and `doorway-baseline`, plus `src-{source}` built from the hidden field.

**Step three. Embed it.** Open `lm-16-sixteen/build/build_funnel.py`, find the block marked
`GHL FORM EMBED`, and replace the whole `.fallback` div with the GHL iframe. Keep the iframe
inside `.formcard` so the styling holds, then rerun `python3 build_funnel.py`. Do not edit
`docs/sixteen/index.html` directly; it is generated and your change will be overwritten.

If you would rather keep the native form, set `GHL_WEBHOOK` in `funnel_content.py` to a GHL
inbound webhook URL and delete the fallback notice line from the builder.

**Set the form's redirect to `https://www.angiemarieglobal.com/sixteen/thank-you/`.** That
page carries the download button, so someone who never opens the email still gets the guide.
The email is still the point, because the email is what the rest of the funnel runs on, but
the thank-you page means a bounced or delayed send never costs you the lead.

**Step four. Workflow `LM16 · Sixteen · Deliver`.**

| When | Action |
|---|---|
| Immediately | Send delivery email. Attach `AMG-Sixteen.pdf` and include the direct link as a backup. Apply `lm16-delivered`. |
| Day 3, 7am AEST | Send the Recognise email. Apply `recognise-offered`. |
| Day 7 | If `audit-complete` is absent, send the nudge email. |
| Day 10 | Drop into the standing Baseline nurture. Exit this workflow. |

Wait steps run on AEST. Set the sub-account timezone to Australia/Brisbane before you
build, or the day three email lands at 5pm for half the list.

**Step five. Host the PDF.** Upload `dist/AMG-Sixteen.pdf` to GHL media. Copy the
public URL into the delivery email as the backup link. Attachments get stripped by some
corporate mail servers, and this list has plenty of those.

**Step six. Trigger link.** Wrap the audit link in a GHL trigger link so `audit-started`
fires on click. Without it you are guessing at the handover rate, which is the single most
useful number this funnel produces.

**Step seven. Confirm the Baseline Membership URL.** `BASELINE_URL` in
`build/funnel_content.py` is a placeholder. The slug is not recorded in amg-ecosystem, and
the old `/baseline` URL is retired and must never be used. Confirm the real one, change the
line, rerun the build. Until then the step two upsell on all three pages points at a guess.

---

## 5. THE THREE EMAILS

Written to the voice law. First line of the body is always `Hey {{contact.first_name}},`.
One CTA each. No prices in email one. No urgency theatre anywhere.

---

### EMAIL 1 · Delivery. Sends immediately.

**Subject:** Sixteen, as promised
**Preview:** Read the moment first. The name is at the bottom on purpose.

```
Hey {{contact.first_name}},

Here it is.

Sixteen pages. Each one opens on something small and specific, and the name of the
pattern sits at the bottom of the page rather than the top.

That is deliberate. A name handed to you at the top is a label. A name you arrive at
yourself is a recognition. Only one of those changes anything.

Read the moment first. If it is not yours, turn the page. There is no prize for
collecting these.

[ OPEN SIXTEEN ]

One thing before you go in. None of the sixteen are flaws. Every one of them is
protection that outlived the season it was built for.

We honour what kept you safe. Now we build what lets you breathe.

Always, Angie
```

---

### EMAIL 2 · Recognise. Sends day three, 7am AEST.

**Subject:** The names are the first half
**Preview:** The loop underneath them is the other half.

```
Hey {{contact.first_name}},

You have had Sixteen for a few days. Most people tick four or five.

Here is what the ticks cannot tell you. Sixteen patterns is not sixteen problems. It is
one loop, wearing however many costumes it needed to keep you safe, and the loop runs on
one belief in one specific place.

That is what Recognise is for.

Three short audio transmissions and The Loop Map, a printable worksheet that maps one
turn of your own loop. You start at the result, because the result is the only station
you can already see, and you work backwards from there to the belief nobody ever
questioned.

Instant access, yours to keep.

[ GET RECOGNISE ]

You already did the honest part. This is the part where it stops being a list and starts
being a map.

Always, Angie

P.S. Remember, abundance is your baseline.
```

*Recognise pricing and access terms come from amg-ecosystem. Do not print a price in the
subject line or the preview text.*

---

### EMAIL 3 · Audit nudge. Day seven, only if `audit-complete` is absent.

**Subject:** The one you did not tick
**Preview:** It is usually the one running the year.

```
Hey {{contact.first_name}},

There is a pattern in Sixteen you read twice and did not tick.

That is worth paying attention to. The ones we recognise instantly are rarely the ones
costing us the most. The expensive one is the one that reads as normal, because it has
been running so long it stopped looking like a pattern and started looking like your
personality.

The free Baseline Audit takes a few minutes and it reads underneath all sixteen. Not the
pattern. The setting.

[ TAKE THE FREE BASELINE AUDIT ]

Settings change. That is the whole point.

Always, Angie
```

---

## 6. WHAT TO WATCH IN THE FIRST THIRTY DAYS

Six numbers. Not sixteen.

| Number | Why it matters |
|---|---|
| Comments on 16 per post | Whether the keyword is landing or the hook is wrong. |
| DM to landing page click rate | Whether the ManyChat message is doing its job. |
| Landing page to form submit | Below 30 percent means the page is asking too much or promising too little. |
| Delivery email open rate | The habit you are actually building. Watch this one hardest. |
| PDF to audit handover | The single number that tells you whether the last page works. |
| Day three to Recognise conversion | Whether the freebie pays for its own traffic. |

Report these into the weekly CEO pulse in amg-launch-metrics. Hook performance goes to
amg-10x10 so the winning openers compound into the next asset instead of resetting.

---

## 7. GO OR NO-GO BEFORE YOU PUBLISH A SINGLE POST

Every line ticked, or the launch waits.

- [ ] Keyword 16 tested with a real comment from a real account, not a preview.
- [ ] ManyChat message fires and the link opens on mobile.
- [ ] Form submits and the contact appears in GHL with all three tags.
- [ ] Delivery email arrives within one minute, with the attachment and a working backup link.
- [ ] PDF opens on iPhone, Android, Mac Preview, Adobe and inside GHL, with no colour shift.
- [ ] Audit trigger link fires `audit-started`.
- [ ] Day three email scheduled on AEST and previewed on a phone.
- [ ] `src=` stamping tested on two different links.
- [ ] Keyword 16 row added to the capture table in amg-ecosystem.

The last one is not admin. It is the difference between a documented asset and a thing
only one person remembers how to run.
