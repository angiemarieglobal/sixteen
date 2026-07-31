#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Adds the interactive layer to the scan page of AMG-Sixteen.pdf.

WHAT THIS DOES
  Attaches an Acrobat calculate action that runs every time any checkbox changes.
  It counts the ticks, writes the count into the counter field, and lights up the
  marker and the underline of every cluster whose numbers are all ticked.

  A calculate action is used rather than a mouse-up action on purpose. Mouse-up
  fires while the checkbox value is still settling; calculate fires after every
  value change in the whole form, in a defined order, so the count is never one
  behind.

HOW FAR IT REACHES, HONESTLY
  Ticking and typing are plain AcroForm and work everywhere: Acrobat, Apple
  Preview, Chrome, Edge, Firefox, iOS Files, most Android readers.
  The automatic cluster highlighting is form JavaScript, which only Adobe Acrobat
  Reader runs. Every other viewer shows the page, ticks the boxes, keeps the
  typing, and simply does not light the clusters. Nothing breaks and nothing looks
  wrong; the reader just counts for themselves. That is why page 19 also carries a
  link to the live web scan, where the highlighting works in every browser.

Usage: python3 add_scan_script.py   (build_sixteen.py calls it automatically)
"""

import os
import pikepdf
from pikepdf import Name, String, Dictionary, Array

import content as C

HERE = os.path.dirname(os.path.abspath(__file__))
PDF = os.path.join(HERE, "..", "dist", "AMG-Sixteen.pdf")

# Recognise palette as Acrobat colour arrays. Solid values, no alpha.
LIT_MARK = "['RGB', 0.776, 0.475, 0.184]"   # Amber Ember  #C6792F
LIT_BAR = "['RGB', 0.816, 0.620, 0.412]"    # Golden Sand  #D09E69
DIM = "['RGB', 0.902, 0.855, 0.761]"        # Ivory Glow   #E6DAC2

# cluster index -> the tick numbers that make it whole
CLUSTER_MEMBERS = [
    ["01", "05", "13"],   # THE FUEL
    ["02", "06", "14"],   # THE YES
    ["03", "07"],         # THE GRIP
    ["04", "08", "15"],   # THE SILENCE
    ["09", "10", "16"],   # THE CHASE
    ["11", "12"],         # THE EXIT
]


def build_js():
    members = ",".join("[" + ",".join(f'"{n}"' for n in m) + "]"
                       for m in CLUSTER_MEMBERS)
    return f"""
// SIXTEEN - the scan
// Angie Marie Global. Runs on every value change in the form.
var SIXTEEN_CLUSTERS = [{members}];

function sixteenTicked(n) {{
    var f = this.getField("tick" + n);
    return (f != null && f.value != "Off");
}}

function sixteenScan() {{
    var total = 0;
    for (var i = 1; i <= 16; i++) {{
        var k = (i < 10 ? "0" : "") + i;
        if (sixteenTicked.call(this, k)) {{ total++; }}
    }}

    var cf = this.getField("count");
    if (cf != null) {{ cf.value = total; }}

    for (var ci = 0; ci < SIXTEEN_CLUSTERS.length; ci++) {{
        var grp = SIXTEEN_CLUSTERS[ci];
        var hits = 0;
        for (var gi = 0; gi < grp.length; gi++) {{
            if (sixteenTicked.call(this, grp[gi])) {{ hits++; }}
        }}
        var whole = (hits == grp.length);
        var mk = this.getField("mark" + ci);
        var br = this.getField("bar" + ci);
        if (mk != null) {{
            mk.fillColor = whole ? {LIT_MARK} : {DIM};
            mk.strokeColor = whole ? {LIT_MARK} : {DIM};
        }}
        if (br != null) {{
            br.fillColor = whole ? {LIT_BAR} : {DIM};
            br.strokeColor = whole ? {LIT_BAR} : {DIM};
        }}
    }}
}}

sixteenScan.call(this);
""".strip()


def main():
    js = build_js()
    with pikepdf.open(PDF, allow_overwriting_input=True) as pdf:
        root = pdf.Root
        acro = root.get("/AcroForm")
        if acro is None:
            raise SystemExit("No AcroForm found. Run build_sixteen.py first.")

        # ZapfDingbats declared in the form's default resources. reportlab draws the
        # tick as a vector path so it renders without the font, but the field's
        # default appearance string names /ZaDb, and any viewer that regenerates a
        # checkbox appearance needs to resolve it. Without this, some readers log a
        # font error and draw an empty box on a ticked field.
        dr = acro.get("/DR")
        if dr is not None and "/Font" in dr and "/ZaDb" not in dr["/Font"]:
            dr["/Font"]["/ZaDb"] = pdf.make_indirect(Dictionary(
                Type=Name.Font, Subtype=Name.Type1,
                BaseFont=Name.ZapfDingbats, Name=Name.ZaDb,
            ))

        # NeedAppearances is deliberately NOT set. reportlab has already written a
        # crisp appearance for every field, and forcing a global regeneration makes
        # lighter viewers redraw them with whatever fonts they can resolve. Acrobat
        # regenerates on its own whenever a value changes, which is all we need.
        if "/NeedAppearances" in acro:
            del acro["/NeedAppearances"]

        # Find the counter field. It carries the calculate action, so the whole
        # recalculation runs once per value change.
        fields = acro.get("/Fields", Array())
        count_ref = None
        for f in fields:
            t = f.get("/T")
            if t is not None and str(t) == "count":
                count_ref = f
                break
        if count_ref is None:
            raise SystemExit("Counter field not found. Check the field name.")

        action = pdf.make_indirect(Dictionary(
            Type=Name.Action, S=Name.JavaScript, JS=String(js),
        ))
        count_ref["/AA"] = Dictionary(C=action)
        acro["/CO"] = Array([count_ref])          # calculation order

        # Run it once on open so a reopened, half-filled copy shows the right state.
        open_js = pdf.make_indirect(Dictionary(
            Type=Name.Action, S=Name.JavaScript, JS=String(js),
        ))
        names = root.get("/Names")
        if names is None:
            names = pdf.make_indirect(Dictionary())
            root["/Names"] = names
        names["/JavaScript"] = pdf.make_indirect(Dictionary(
            Names=Array([String("SixteenScan"), open_js])
        ))

        pdf.save()

    print("scan script attached")
    print("  16 checkboxes, 3 text lines, 1 counter, 6 cluster markers, 6 bars")
    print("  fill and type: every reader. auto highlight: Adobe Acrobat.")


if __name__ == "__main__":
    main()
