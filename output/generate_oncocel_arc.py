#!/usr/bin/env python3
"""Generate OncoCel LLC branded ARC Volume Heads-Up document."""

from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml
import os

# OncoCel colors - clean professional palette
# Using navy + teal + green (derived from OncoCel strategic plan style)
OC_NAVY = RGBColor(0x1B, 0x2A, 0x4A)
OC_TEAL = RGBColor(0x00, 0x7B, 0x7F)
OC_GREEN = RGBColor(0x2E, 0x86, 0x4B)
OC_BLUE = RGBColor(0x2C, 0x5F, 0x8A)
OC_LIGHT = RGBColor(0xE8, 0xF0, 0xF2)
OC_DARK = RGBColor(0x2C, 0x2C, 0x2C)
OC_GRAY = RGBColor(0x77, 0x77, 0x77)
OC_WHITE = RGBColor(0xFF, 0xFF, 0xFF)
OC_RED = RGBColor(0xBB, 0x33, 0x33)
OC_POS = RGBColor(0x1E, 0x88, 0x49)

def shade(cell, hex_color):
    cell._tc.get_or_add_tcPr().append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>'))

def border(cell, c="CCCCCC"):
    cell._tc.get_or_add_tcPr().append(parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="2" w:space="0" w:color="{c}"/>'
        f'<w:bottom w:val="single" w:sz="2" w:space="0" w:color="{c}"/>'
        f'<w:left w:val="single" w:sz="2" w:space="0" w:color="{c}"/>'
        f'<w:right w:val="single" w:sz="2" w:space="0" w:color="{c}"/>'
        f'</w:tcBorders>'))

def margins(cell, v=40, h=80):
    cell._tc.get_or_add_tcPr().append(parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{v}" w:type="dxa"/><w:bottom w:w="{v}" w:type="dxa"/>'
        f'<w:left w:w="{h}" w:type="dxa"/><w:right w:w="{h}" w:type="dxa"/>'
        f'</w:tcMar>'))

def table(doc, headers, rows, hdr_hex="1B2A4A"):
    t = doc.add_table(rows=1+len(rows), cols=len(headers))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = True
    for i, h in enumerate(headers):
        c = t.rows[0].cells[i]
        c.text = ""
        p = c.paragraphs[0]
        p.space_before = Pt(1); p.space_after = Pt(1)
        r = p.add_run(h)
        r.bold = True; r.font.size = Pt(8); r.font.color.rgb = OC_WHITE; r.font.name = "Calibri"
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        shade(c, hdr_hex); border(c, hdr_hex); margins(c)
    for ri, rd in enumerate(rows):
        is_sum = any(k in str(rd[0]).lower() for k in ["total","capture","treated","access","growth","on-island","arc "])
        for ci, v in enumerate(rd):
            c = t.rows[ri+1].cells[ci]
            c.text = ""
            p = c.paragraphs[0]
            p.space_before = Pt(1); p.space_after = Pt(1)
            txt = str(v)
            r = p.add_run(txt)
            r.font.size = Pt(8); r.font.name = "Calibri"
            if ci == 0:
                r.bold = True
                r.font.color.rgb = OC_TEAL if is_sum else OC_DARK
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                if "+" in txt and any(d.isdigit() for d in txt):
                    r.font.color.rgb = OC_POS; r.bold = True
                elif txt.startswith("-") and any(d.isdigit() for d in txt):
                    r.font.color.rgb = OC_RED
                elif is_sum:
                    r.bold = True; r.font.color.rgb = OC_TEAL
                else:
                    r.font.color.rgb = OC_DARK
            bg = "F5F7F8" if ri % 2 == 1 else "FFFFFF"
            if is_sum: bg = "E8F4F0"
            shade(c, bg); border(c); margins(c)
    return t

def sect(doc, num, title):
    p = doc.add_paragraph()
    p.space_before = Pt(16); p.space_after = Pt(2)
    r = p.add_run(f"{num}  "); r.font.size = Pt(9); r.font.color.rgb = OC_TEAL; r.font.name = "Calibri"; r.bold = True
    r = p.add_run(title.upper()); r.font.size = Pt(13); r.font.color.rgb = OC_NAVY; r.font.name = "Calibri"; r.bold = True
    p2 = doc.add_paragraph(); p2.space_after = Pt(4)
    p2._p.get_or_add_pPr().append(parse_xml(f'<w:pBdr {nsdecls("w")}><w:bottom w:val="single" w:sz="6" w:space="1" w:color="007B7F"/></w:pBdr>'))

def sub(doc, title):
    p = doc.add_paragraph(); p.space_before = Pt(8); p.space_after = Pt(2)
    r = p.add_run(title); r.font.size = Pt(10); r.font.color.rgb = OC_TEAL; r.font.name = "Calibri"; r.bold = True

def body(doc, text, bold=False, color=None, size=9, after=3):
    p = doc.add_paragraph(); p.space_after = Pt(after)
    r = p.add_run(text); r.font.size = Pt(size); r.font.name = "Calibri"; r.bold = bold; r.font.color.rgb = color or OC_DARK
    return p

def bullet(doc, text, prefix=None):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.left_indent = Inches(0.3); p.space_after = Pt(2)
    if prefix:
        r = p.add_run(prefix); r.bold = True; r.font.size = Pt(8.5); r.font.name = "Calibri"; r.font.color.rgb = OC_TEAL
        r = p.add_run(f" — {text}"); r.font.size = Pt(8.5); r.font.name = "Calibri"; r.font.color.rgb = OC_DARK
    else:
        r = p.add_run(text); r.font.size = Pt(8.5); r.font.name = "Calibri"; r.font.color.rgb = OC_DARK

def callout(doc, text, color=None):
    p = doc.add_paragraph(); p.space_before = Pt(4); p.space_after = Pt(4)
    p.paragraph_format.left_indent = Inches(0.15)
    p._p.get_or_add_pPr().append(parse_xml(f'<w:pBdr {nsdecls("w")}><w:left w:val="single" w:sz="16" w:space="8" w:color="007B7F"/></w:pBdr>'))
    r = p.add_run(text); r.font.size = Pt(8.5); r.font.name = "Calibri"; r.bold = True; r.font.color.rgb = color or OC_NAVY

# ============================================================
doc = Document()
s = doc.styles['Normal']; s.font.name = 'Calibri'; s.font.size = Pt(9); s.font.color.rgb = OC_DARK
for sec in doc.sections:
    sec.top_margin = Cm(1.8); sec.bottom_margin = Cm(1.5); sec.left_margin = Cm(2.2); sec.right_margin = Cm(2.2)

# ============================================================
# HEADER
# ============================================================
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.LEFT; p.space_after = Pt(0)
r = p.add_run("ONCOCEL"); r.font.size = Pt(26); r.font.color.rgb = OC_NAVY; r.font.name = "Calibri"; r.bold = True
r = p.add_run("  LLC"); r.font.size = Pt(14); r.font.color.rgb = OC_GRAY; r.font.name = "Calibri"

p = doc.add_paragraph(); p.space_after = Pt(8)
p._p.get_or_add_pPr().append(parse_xml(f'<w:pBdr {nsdecls("w")}><w:bottom w:val="single" w:sz="10" w:space="1" w:color="007B7F"/></w:pBdr>'))

p = doc.add_paragraph(); p.space_after = Pt(2)
r = p.add_run("Volume Growth Notification"); r.font.size = Pt(18); r.font.color.rgb = OC_TEAL; r.font.name = "Calibri"; r.bold = True

p = doc.add_paragraph(); p.space_after = Pt(2)
r = p.add_run("Prepared for American Red Cross (ARC)"); r.font.size = Pt(11); r.font.color.rgb = OC_DARK; r.font.name = "Calibri"

p = doc.add_paragraph(); p.space_after = Pt(1)
r = p.add_run("Apheresis & Cell Processing Services — Anticipated Volume Increase"); r.font.size = Pt(9); r.font.color.rgb = OC_GRAY; r.font.name = "Calibri"; r.italic = True

p = doc.add_paragraph(); p.space_after = Pt(6)
r = p.add_run("June 2026  |  Confidential"); r.font.size = Pt(8.5); r.font.color.rgb = OC_GRAY; r.font.name = "Calibri"

# ============================================================
# 01 CONTEXT
# ============================================================
sect(doc, "01", "Context")

body(doc, "TCT Oncology is launching a BMTCI Program (Hematopoietic Stem Cell Transplantation & Cellular Immunotherapy) at the Centro Comprensivo de Cancer de la Universidad de Puerto Rico (CCCUPR), with clinical operations beginning August 2026. OncoCel LLC provides strategic, operational, and research infrastructure support to the program.")

body(doc, "TCT Oncology also operates the established allogeneic HSCT program and CIBMTR reporting infrastructure at Auxilio Mutuo Hospital (HAM). Together, TCT Oncology and OncoCel create Puerto Rico's first comprehensive cellular therapy network — with CCCUPR handling autologous HCT and CAR-T, and HAM continuing as the allo-HSCT center.")

body(doc, "ARC is the only FACT-accredited apheresis and cell processing provider on the island. As TCT Oncology scales across both sites with OncoCel support, ARC's collection and processing volume will increase significantly. This document provides ARC with advance notice of projected volumes to support capacity planning and contract scope review.", after=6)

callout(doc, "Purpose: Give ARC a heads-up on anticipated volume growth across TCT Oncology at CCCUPR and HAM — supported by OncoCel — so both organizations can plan capacity, amend contract scope, and ensure service continuity.")

# ============================================================
# 02 PROGRAM PHASES
# ============================================================
sect(doc, "02", "OncoCel Program Phases")

table(doc,
    ["Phase", "Timeline", "Scope", "Volume Target"],
    [
        ["Phase 1", "Year 1 (Aug 2026-2027)", "Autologous HCT", "10-15 auto-HCTs"],
        ["Phase 2", "Year 2-3 (2028-2029)", "+ CAR-T + Donor Search", "20-30+ transplants/yr"],
        ["Phase 3", "Year 3+ (2029+)", "+ Allogeneic HCT + Gene Therapy", "Full-spectrum program"],
    ], hdr_hex="007B7F")

body(doc, "")
body(doc, "TCT Oncology also operates the allogeneic HSCT program at Auxilio Mutuo Hospital (HAM). Patients identified at CCCUPR who need allo-HSCT will be referred to HAM through TCT Oncology, generating additional donor collection volume for ARC across both sites.", size=8.5)

# ============================================================
# 03 PROJECTED ARC VOLUMES
# ============================================================
sect(doc, "03", "Projected ARC Collection Volumes")

body(doc, "All volumes below represent new programmatic activity. This is not a redistribution of existing ARC workload.", bold=True, size=9, color=OC_TEAL, after=6)

table(doc,
    ["ARC Service", "Year 1", "Year 2", "Year 3", "Year 5"],
    [
        ["Autologous HSC collections (CCCUPR)", "12-18", "22-32", "30-42", "40-55"],
        ["CAR-T leukapheresis (CCCUPR)", "4-8", "10-14", "16-22", "30-45"],
        ["Allo donor collections (HAM via TCT Oncology)", "4-6", "8-12", "10-15", "15-22"],
        ["Total apheresis procedures", "20-32", "40-58", "56-80", "85-122"],
    ], hdr_hex="007B7F")

body(doc, "")
body(doc, "Supporting processing volume:", bold=True, size=9, color=OC_TEAL, after=2)

table(doc,
    ["Processing Service", "Year 1", "Year 2", "Year 3", "Year 5"],
    [
        ["Cryopreservation events", "16-24", "30-44", "40-57", "55-77"],
        ["Product release testing", "20-32", "40-58", "56-80", "85-122"],
        ["Chain-of-custody/identity", "20-32", "40-58", "56-80", "85-122"],
    ], hdr_hex="1B2A4A")

# ============================================================
# 04 CONTRACT SCOPE REVIEW
# ============================================================
sect(doc, "04", "Contract Scope — Items to Review")

body(doc, "OncoCel requests ARC confirm coverage for the following services as the program scales:", after=4)

table(doc,
    ["Service", "Status", "Action"],
    [
        ["Autologous HSC collection & processing", "Confirm", "Verify explicit coverage in current agreement"],
        ["HSC cryopreservation & long-term storage", "Confirm", "Verify capacity and pricing at projected volume"],
        ["CAR-T leukapheresis & shipment logistics", "Likely gap", "Amend contract — new service category required"],
        ["Allogeneic donor collections", "Plan ahead", "Amendment needed by Year 2 (2028)"],
        ["Capacity guarantees & turnaround SLA", "Critical", "Must guarantee slots for emergent collections"],
        ["Volume-based pricing", "Discuss", "As volume scales from 20 to 85+ procedures/year"],
    ], hdr_hex="007B7F")

# ============================================================
# 05 WHY THIS MATTERS
# ============================================================
sect(doc, "05", "Why Volume Is Growing")

body(doc, "Puerto Rico currently has no on-island CAR-T program and limited transplant capacity. Most eligible patients travel to the US mainland or go untreated:", after=4)

table(doc,
    ["Metric", "Current State", "With OncoCel (Year 5)"],
    [
        ["Auto SCT performed on-island/year", "20-35", "62-83"],
        ["Allo-HSCT performed on-island/year", "8-15", "25-38"],
        ["CAR-T performed on-island/year", "0", "30-45"],
        ["Total on-island cellular therapy cases", "28-50", "117-166"],
        ["Patients traveling to mainland/year", "60-100", "18-31"],
        ["ARC apheresis procedures/year (OncoCel)", "0", "85-122"],
    ], hdr_hex="1B2A4A")

body(doc, "")
callout(doc, "ARC is positioned as the sole on-island partner for this growth. No other FACT-accredited provider in Puerto Rico can support the apheresis and cell processing requirements of TCT Oncology's cellular therapy network.")

# ============================================================
# 06 TIMELINE
# ============================================================
sect(doc, "06", "Timeline & Next Steps")

table(doc,
    ["When", "What", "ARC Impact"],
    [
        ["August 2026", "TCT Oncology launches BMTCI at CCCUPR", "First collection requests anticipated Q4 2026"],
        ["Q4 2026", "First autologous HSC collections (CCCUPR)", "12-18 collections in Year 1"],
        ["Q1 2027", "First CAR-T leukapheresis (CCCUPR)", "New service type — contract amendment needed"],
        ["2028", "Allo-HSCT donor collections ramp (HAM via TCT)", "Donor collection volume increasing"],
        ["2028-2029", "Program reaches 40-58 procedures/year", "Volume-based pricing discussion"],
        ["2031", "Full program at 85-122 procedures/year", "Steady-state capacity planning"],
    ], hdr_hex="007B7F")

body(doc, "")
body(doc, "OncoCel, on behalf of TCT Oncology, proposes a meeting with ARC leadership to:", bold=True, size=9, color=OC_TEAL, after=2)
bullet(doc, "Review current contract scope against projected service needs")
bullet(doc, "Confirm capacity availability for Year 1 collections (Q4 2026 start)")
bullet(doc, "Discuss CAR-T leukapheresis as a new service category and amend agreement")
bullet(doc, "Establish turnaround and capacity SLA for emergent collection slots")
bullet(doc, "Plan volume-based pricing as the program scales")

# ============================================================
# FOOTER
# ============================================================
p = doc.add_paragraph(); p.space_before = Pt(24)
p._p.get_or_add_pPr().append(parse_xml(f'<w:pBdr {nsdecls("w")}><w:top w:val="single" w:sz="6" w:space="6" w:color="007B7F"/></w:pBdr>'))

p = doc.add_paragraph(); p.space_after = Pt(0)
r = p.add_run("ONCOCEL"); r.font.size = Pt(12); r.font.color.rgb = OC_NAVY; r.font.name = "Calibri"; r.bold = True
r = p.add_run("  LLC"); r.font.size = Pt(8); r.font.color.rgb = OC_GRAY; r.font.name = "Calibri"

p = doc.add_paragraph(); p.space_after = Pt(1)
r = p.add_run("Carlos Mendez, COO — cmendez@tctoncology.com"); r.font.size = Pt(8); r.font.color.rgb = OC_GRAY; r.font.name = "Calibri"

p = doc.add_paragraph(); p.space_after = Pt(1)
r = p.add_run("Supporting TCT Oncology at CCCUPR and Auxilio Mutuo Hospital"); r.font.size = Pt(7.5); r.font.color.rgb = OC_GRAY; r.font.name = "Calibri"; r.italic = True

p = doc.add_paragraph()
r = p.add_run("June 2026  |  Confidential"); r.font.size = Pt(7.5); r.font.color.rgb = OC_GRAY; r.font.name = "Calibri"

# Save
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "OncoCel_ARC_Volume_Notification.docx")
doc.save(out)
print(f"Saved: {out}")
