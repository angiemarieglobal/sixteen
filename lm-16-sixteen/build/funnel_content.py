# -*- coding: utf-8 -*-
"""
SIXTEEN funnel - copy and routing source of truth.
Angie Marie Global | lead magnet 16 | keyword 16

Every word and every URL on the three funnel pages lives here. build_funnel.py
renders index, thank-you and scan from this file, so the pages cannot drift apart.

Voice law: amg-voice-master. No em dashes, no exclamation marks, no ellipses,
no emoji, AU/UK spelling, non-gendered, never lead with the label.
Routing law: amg-ecosystem. No page in this funnel prints a price.
"""

BRAND = "Angie Marie Global"
AUTHOR = "Angie Marie"
CLOSING = "Abundance is your baseline"
TRILOGY = "Recognise. Rewire. Return."

# --------------------------------------------------------------------------- #
# ROUTING
# Change a URL here and all three pages update.
#
# CONFIRMED against amg-ecosystem (re-locked 27 July 2026):
#   /baseline-audit   the free front door, live, site wide
#   /recognise        the $22 rung, live, redirects from /the-recognition-page
#
#   /baseline         Baseline. Confirmed by Angie on 30 July 2026, and the offer is
#                     referred to as Baseline, one word, in line with the naming
#                     system.
#
# FOR THE NEXT RE-LOCK: the amg-ecosystem retired list still names
# angiemarieglobal.com/baseline as retired, because that URL used to carry the old
# Baseline Audit funnel. Angie has confirmed it now points at Baseline. That entry
# needs updating so nobody bans a live URL again.
# --------------------------------------------------------------------------- #

# Two hosting worlds, and they are not the same.
#   SITE   the GHL site. Serves /baseline-audit, /recognise, /baseline. Confirmed live.
#   PAGES  GitHub Pages. Serves this funnel, same as permission-audit and
#          capacity-audit. Confirmed by Angie on 30 July 2026.
SITE = "https://www.angiemarieglobal.com"
PAGES = "https://angiemarieglobal.github.io/sixteen"
AUDIT_URL = f"{SITE}/baseline-audit"
RECOGNISE_URL = f"{SITE}/recognise"
BASELINE_URL = f"{SITE}/baseline"
PDF_FILE = "AMG-Sixteen.pdf"                        # served from /sixteen/
SCAN_PATH = "scan/"
THANKS_PATH = "thank-you/"

# GHL. The form posts here, then GHL redirects to the thank-you page.
GHL_WEBHOOK = "REPLACE_WITH_GHL_WEBHOOK_URL"
THANKS_URL = f"{PAGES}/thank-you/"
GHL_TAGS = "lm-sixteen,doorway-baseline"
GHL_WORKFLOW = "LM16 · Sixteen · Deliver"
GHL_FORM_NAME = "LM 16 · Sixteen"

# --------------------------------------------------------------------------- #
# THE OPT-IN PAGE
# --------------------------------------------------------------------------- #

TITLE = "Sixteen"
STRAP = "Sixteen patterns nobody ever named for you"
BADGE = "Free &middot; 20 pages"
HERO_LINE = ("Read the moment first. The name is at the bottom of every page, "
             "and it is there on purpose.")
HERO_CTA = "Send me Sixteen"
HERO_TINY = "No cost. One email. Leave any time."

PROBLEM = [
    ("lede", "Nobody scrolls through their own life thinking I have poor boundaries."),
    ("p", "They think: I leaned on the horn at a stranger this morning. I cancelled on my "
          "family again. I redid the apprentice's work at 9pm."),
    ("p", "That is where this starts. The moment, not the diagnosis."),
    ("p", "Sixteen pages. Each one opens on something small and specific that most people "
          "have done and almost nobody has said out loud. Read the moment first. If it is "
          "not yours, turn the page. There is no prize for collecting these."),
]

# All sixteen, in full, on the page. Nothing held back. The guide holds the
# names, the loops, the questions and the scan.
GRID_EYEBROW = "All sixteen"
GRID_TITLE = "Here they are. Every one."
GRID_LEAD = ("Read them slowly. Some will not be yours and that is the point. The ones that "
             "are will feel less like reading and more like being caught.")

MOMENTS = [
    "Leaned on the horn at a stranger by 7:45am.",
    "Said yes to the extra swing before telling anyone at home.",
    "Nobody brings you a problem any more, only fires.",
    "The fight was never about the dishwasher.",
    "Checked email before your feet touched the floor.",
    "Three people offered to help and you said no to all of them.",
    "Redid the apprentice's work at 9pm. Told yourself it was faster.",
    "It's fine, said as a full sentence, three weeks running.",
    "Got the five year thing. Flat by Tuesday.",
    "It is finished. It has been in drafts for eleven days.",
    "10:47pm, two hours into the phone, alarm set for 4:45.",
    "Googled cabins on your lunch break again.",
    "Day two of the holiday and you were already itchy.",
    "I'm fine, said to everyone, meant for no one.",
    "3:14am, winning an argument with someone asleep.",
    "Smiled for the photo. Felt nothing.",
]

GRID_CLOSE = ("Sixteen moments. Sixteen names. The names are in the guide, at the bottom of "
              "each page, because a name handed to you at the top is a label and a name you "
              "arrive at yourself is a recognition.")

LOOP_EYEBROW = "Why naming it changes it"
LOOP_TITLE = "Discipline attacks the doing"
LOOP_BODY = [
    "Every one of the sixteen runs on the same loop. And the loop is why willpower keeps "
    "failing you, because willpower goes after the last link while the first one quietly "
    "manufactures more of the same.",
    "Trace it backwards from the moment and you land on a belief nobody ever questioned. "
    "That is the only place any of this actually changes.",
]
LOOP_PULL = ("None of these are flaws. Every single one is protection that outlived the "
             "season it was built for.")
LOOP_CHAIN = [
    ("01", "A <strong>belief</strong> nobody ever questioned"),
    ("02", "drives the <strong>thought</strong> you have on repeat"),
    ("03", "which drives what you <strong>feel</strong>"),
    ("04", "which drives what you <strong>do</strong>"),
    ("05", "which produces the <strong>result</strong>"),
    ("06", "and the result walks back around and hands the belief its evidence"),
]

INSIDE_EYEBROW = "See inside"
INSIDE_TITLE = "Twenty pages, and no filler"
INSIDE_LEAD = ("Every page carries one moment, what you have been calling it, what it "
               "actually is, the loop underneath it, and one question worth answering "
               "honestly.")
PREVIEWS = [
    ("preview-cover.jpg", "The cover", "The cover of Sixteen."),
    ("preview-code.jpg", "One of the sixteen",
     "A page of Sixteen showing the moment, the disguise, the truth and the loop."),
    ("preview-escape.jpg", "The honest one",
     "The page on wanting a life that does not need escaping."),
    ("preview-scan.jpg", "The scan", "The scan page, fillable, with the six clusters."),
]
COUNTS = [
    ("16", "One page per pattern. The moment, the disguise, the truth, the loop, and the "
           "name at the bottom."),
    ("6", "Clusters. Three ticks sitting together is not three problems. It is one loop, "
          "wearing three costumes."),
    ("1", "Question per page. One. Answerable in a sentence, and worth answering honestly."),
]

SCAN_TEASE_EYEBROW = "The scan"
SCAN_TEASE_TITLE = "Then watch the shape of it"
SCAN_TEASE_BODY = [
    "The scan page inside the guide is fillable, so you can tick the boxes and type on the "
    "lines without printing a thing. It also lives here on the site, where the clusters "
    "light up on their own as you go and the closing line rewrites itself to match what you "
    "ticked.",
    "You do not need the guide to run it. It is open right now.",
]
SCAN_TEASE_CTA = "Run the live scan"

CAPTURE_EYEBROW = "Send it to me"
CAPTURE_TITLE = "Sixteen, in your inbox in the next minute"
CAPTURE_BODY = [
    "Twenty pages, print ready, yours to keep. A4, and it works on a phone.",
    "One email with the guide. Nothing shared with anyone, and you can leave the list "
    "any time.",
]

# The capture fields, in this order. The phone is optional and says so on the
# label, because an unmarked optional field reads as a required one and costs
# submissions.
FIELDS = [
    dict(id="first_name", label="First name", type="text",
         autocomplete="given-name", required=True),
    dict(id="last_name", label="Surname", type="text",
         autocomplete="family-name", required=True),
    dict(id="email", label="Email", type="email",
         autocomplete="email", required=True),
    dict(id="phone", label="Phone (optional)", type="tel",
         autocomplete="tel", required=False),
]

WHO_EYEBROW = "Who wrote this"
WHO_BODY = [
    "I work with high functioning people who hold everything together and are held by "
    "nobody. I do it from a boat, because we did not escape our life. We redesigned it.",
    "The sixteen patterns in this guide are the ones I see over and over, on mine sites and "
    "in clinics and workshops and at kitchen tables. I have run most of them myself.",
]

# --------------------------------------------------------------------------- #
# THE TWO UPSELLS. Bottom of every page. No prices, per amg-ecosystem.
# --------------------------------------------------------------------------- #

NEXT_EYEBROW = "Where this goes next"
NEXT_TITLE = "Two doors, and they open in order"
NEXT_LEAD = ("Sixteen gives you the names. These two are what happens after you have them.")

UPSELLS = [
    dict(
        step="One",
        name="Recognise",
        line="A loop you can see has already lost its authority.",
        body="Three private audio transmissions, eyes closed, where you catch your own loop "
             "running live rather than hearing it explained. Then The Loop Map, three pages "
             "you fill in by hand, because the hand matters more than the paper. And the "
             "ninety-second practice that brings you back to centre in any room, any "
             "conversation, any Monday. About thirty-eight minutes of audio. Instant access, "
             "yours to keep.",
        cta="Go to Recognise",
        url_key="RECOGNISE_URL",
    ),
    dict(
        step="Two",
        name="Baseline",
        line="Read the blueprint instead of arguing with the print-out.",
        body="One Key Code a week, video and audio, short enough to receive while the kettle "
             "boils. Fifty-two of them across a year, and together they walk one full turn of "
             "the loop: see it, feel it, rewire it, hold the new floor. Plus the library that "
             "keeps growing, and a quiet room where everyone moves through the same Key Code "
             "in the same week. No tiers and no countdown. One steady room for as long as "
             "you stay.",
        cta="Go to Baseline",
        url_key="BASELINE_URL",
    ),
]

# --------------------------------------------------------------------------- #
# THE THANK YOU PAGE
# --------------------------------------------------------------------------- #

TY_BADGE = "It is on its way"
TY_TITLE = "Sixteen is yours"
TY_LEAD = ("The email is landing now. If it has not arrived in five minutes, check the "
           "promotions tab, and mark it as not spam so the rest reaches you.")
TY_DL = "Download Sixteen now"
TY_DL_NOTE = "20 pages, A4, print ready. The scan page is fillable."
TY_NEXT_TITLE = "Start here"
TY_NEXT = [
    "Open it and read the moments. Do not skip to the names.",
    "When one lands, keep reading down that page. The name is at the bottom.",
    "Then run the scan and look at the shape of it.",
]
TY_SCAN_CTA = "Run the live scan"
TY_AUDIT_EYEBROW = "And when you are ready"
TY_AUDIT_TITLE = "The names are the first half"
TY_AUDIT_BODY = ("The second half is the loop underneath them, and that is one specific "
                 "belief in one specific place generating all of it. The free Baseline Audit "
                 "takes a few minutes and reads what is running underneath every one of the "
                 "sixteen. Not the pattern. The setting.")
TY_AUDIT_CTA = "Take the free Baseline Audit"

# --------------------------------------------------------------------------- #
# THE SCAN PAGE
# --------------------------------------------------------------------------- #

SC_EYEBROW = "Sixteen"
SC_TITLE = "The scan"
SC_LEAD = "Tick the moments that were yours. The clusters move with you."
SC_H1 = "What was yours"
SC_H1_LEAD = "Not the ones you understand. The ones you have done."
SC_COUNT_SAID = ("Most people land on four or five. If you landed on nine, you are not worse "
                 "than anyone. You are more honest than most, and honesty is the entire "
                 "entry fee.")
SC_NAMES_LEAD = ("Now three names. Not the ones that made sense. The ones you felt somewhere "
                 "below your throat before your head caught up.")
SC_CLUSTER_TITLE = "The clusters"
SC_CLUSTER_LEAD = "A cluster lights up when every number in it is yours."
SC_VERDICT = ("Wherever three of your ticks sit together in one cluster, you are not looking "
              "at three problems. You are looking at one loop, wearing three costumes.")
SC_PRINT = "Print or save this scan"

CLUSTERS = [
    ("The Fuel", [1, 5, 13]),
    ("The Yes", [2, 6, 14]),
    ("The Grip", [3, 7]),
    ("The Silence", [4, 8, 15]),
    ("The Chase", [9, 10, 16]),
    ("The Exit", [11, 12]),
]
