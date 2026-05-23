#!/usr/bin/env python3
"""Generate a handwritten/chalkboard-style infographic for CAR T-Cell Therapy Financials."""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np
import os

# Set up the dark chalkboard style
plt.rcParams.update({
    'figure.facecolor': '#2b2b2b',
    'axes.facecolor': '#2b2b2b',
    'text.color': '#e8e8e0',
    'axes.labelcolor': '#e8e8e0',
    'xtick.color': '#e8e8e0',
    'ytick.color': '#e8e8e0',
})

fig = plt.figure(figsize=(24, 36), facecolor='#1a1a2e')

# Add chalkboard texture effect
ax_bg = fig.add_axes([0, 0, 1, 1])
ax_bg.set_xlim(0, 1)
ax_bg.set_ylim(0, 1)
ax_bg.set_facecolor('#1a1a2e')

# Subtle chalk dust texture
np.random.seed(42)
for _ in range(3000):
    x, y = np.random.random(), np.random.random()
    alpha = np.random.uniform(0.01, 0.04)
    size = np.random.uniform(0.5, 2.0)
    ax_bg.plot(x, y, '.', color='white', alpha=alpha, markersize=size)

ax_bg.axis('off')

# Chalk colors
CHALK_WHITE = '#e8e8e0'
CHALK_YELLOW = '#f0e68c'
CHALK_BLUE = '#87ceeb'
CHALK_GREEN = '#90ee90'
CHALK_PINK = '#ffb6c1'
CHALK_ORANGE = '#ffa07a'
CHALK_CORAL = '#f08080'

# Helper function to add chalk-like text with slight imperfection
def chalk_text(ax, x, y, text, fontsize=14, color=CHALK_WHITE, ha='center', va='center',
               weight='normal', style='normal', alpha=0.95, rotation=0):
    ax.text(x, y, text, fontsize=fontsize, color=color, ha=ha, va=va,
            fontweight=weight, fontstyle=style, alpha=alpha, rotation=rotation,
            fontfamily='serif')

# Draw chalk-style underline
def chalk_underline(ax, x_start, x_end, y, color=CHALK_YELLOW, lw=2):
    xs = np.linspace(x_start, x_end, 50)
    ys = y + np.random.normal(0, 0.001, 50)
    ax.plot(xs, ys, color=color, linewidth=lw, alpha=0.7)

# Draw chalk box
def chalk_box(ax, x, y, w, h, color=CHALK_WHITE, lw=1.5):
    offsets = np.random.normal(0, 0.002, 8)
    ax.plot([x+offsets[0], x+w+offsets[1]], [y+offsets[2], y+offsets[3]], color=color, lw=lw, alpha=0.5)
    ax.plot([x+w+offsets[1], x+w+offsets[4]], [y+offsets[3], y+h+offsets[5]], color=color, lw=lw, alpha=0.5)
    ax.plot([x+w+offsets[4], x+offsets[6]], [y+h+offsets[5], y+h+offsets[7]], color=color, lw=lw, alpha=0.5)
    ax.plot([x+offsets[6], x+offsets[0]], [y+h+offsets[7], y+offsets[2]], color=color, lw=lw, alpha=0.5)

# Draw chalk arrow
def chalk_arrow(ax, x1, y1, x2, y2, color=CHALK_WHITE):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color, lw=2, alpha=0.7))

# ============================================================
# TITLE SECTION
# ============================================================
chalk_text(ax_bg, 0.5, 0.97, 'CAR T-CELL THERAPY', fontsize=42, color=CHALK_YELLOW, weight='bold')
chalk_text(ax_bg, 0.5, 0.955, 'FINANCIAL ANALYSIS', fontsize=36, color=CHALK_YELLOW, weight='bold')
chalk_underline(ax_bg, 0.15, 0.85, 0.945, color=CHALK_YELLOW, lw=3)
chalk_text(ax_bg, 0.5, 0.935, 'US & Puerto Rico  |  2025-2026', fontsize=20, color=CHALK_BLUE)

# ============================================================
# SECTION 1: MARKET SIZE (top-left)
# ============================================================
y_sec1 = 0.895
chalk_text(ax_bg, 0.25, y_sec1, 'MARKET SIZE', fontsize=26, color=CHALK_GREEN, weight='bold')
chalk_underline(ax_bg, 0.08, 0.42, y_sec1 - 0.012, color=CHALK_GREEN, lw=2)

chalk_box(ax_bg, 0.04, y_sec1 - 0.085, 0.42, 0.07, color=CHALK_GREEN)
chalk_text(ax_bg, 0.25, y_sec1 - 0.03, 'US Market 2025', fontsize=16, color=CHALK_WHITE, weight='bold')
chalk_text(ax_bg, 0.25, y_sec1 - 0.05, '$6.3 BILLION', fontsize=28, color=CHALK_YELLOW, weight='bold')
chalk_text(ax_bg, 0.25, y_sec1 - 0.07, '70.4% of Global Market', fontsize=13, color=CHALK_BLUE)

# Growth projections
y_proj = y_sec1 - 0.11
chalk_text(ax_bg, 0.25, y_proj, 'Growth Projections', fontsize=16, color=CHALK_WHITE, weight='bold', style='italic')

bars_data = [
    ('2025', 6.3, CHALK_BLUE),
    ('2030', 15.0, CHALK_GREEN),
    ('2033', 9.85, CHALK_ORANGE),
    ('2035', 42.61, CHALK_YELLOW),
]

bar_width = 0.08
bar_start_x = 0.06
for i, (label, val, color) in enumerate(bars_data):
    bx = bar_start_x + i * 0.105
    bar_h = val / 42.61 * 0.06
    chalk_box(ax_bg, bx, y_proj - 0.08, bar_width, bar_h, color=color)
    # Fill the bar
    for fill_y in np.linspace(y_proj - 0.08, y_proj - 0.08 + bar_h, 15):
        ax_bg.plot([bx + 0.005, bx + bar_width - 0.005], [fill_y, fill_y],
                   color=color, alpha=0.3, lw=1)
    chalk_text(ax_bg, bx + bar_width/2, y_proj - 0.09, label, fontsize=11, color=color)
    chalk_text(ax_bg, bx + bar_width/2, y_proj - 0.075 + bar_h, f'${val}B', fontsize=11, color=color, weight='bold')

chalk_text(ax_bg, 0.25, y_proj - 0.105, '30.4% CAGR through 2035', fontsize=13, color=CHALK_CORAL, style='italic')

# ============================================================
# SECTION 2: KEY PLAYERS (top-right)
# ============================================================
chalk_text(ax_bg, 0.75, y_sec1, 'KEY PLAYERS & REVENUE', fontsize=26, color=CHALK_PINK, weight='bold')
chalk_underline(ax_bg, 0.54, 0.96, y_sec1 - 0.012, color=CHALK_PINK, lw=2)

players = [
    ('LEGEND / J&J', 'Carvykti', '$1.9B', '64% YoY', CHALK_YELLOW),
    ('GILEAD / KITE', 'Yescarta', '$1.5B+', '35% share', CHALK_GREEN),
    ('BRISTOL-MYERS', 'Breyanzi+Abecma', '$1B+', '5 indications', CHALK_BLUE),
    ('NOVARTIS', 'Kymriah', '$388M', 'First CAR-T', CHALK_ORANGE),
    ('AUTOLUS', 'Aucatzyl', 'New', '2025 approval', CHALK_CORAL),
]

for i, (company, product, rev, note, color) in enumerate(players):
    py = y_sec1 - 0.04 - i * 0.04
    chalk_box(ax_bg, 0.54, py - 0.015, 0.42, 0.035, color=color)
    chalk_text(ax_bg, 0.63, py + 0.003, company, fontsize=13, color=color, weight='bold', ha='left')
    chalk_text(ax_bg, 0.76, py + 0.003, product, fontsize=11, color=CHALK_WHITE, ha='left', style='italic')
    chalk_text(ax_bg, 0.88, py + 0.003, rev, fontsize=14, color=CHALK_YELLOW, weight='bold', ha='center')
    chalk_text(ax_bg, 0.94, py + 0.003, note, fontsize=9, color=CHALK_WHITE, ha='center', alpha=0.7)

# ============================================================
# SECTION 3: TREATMENT COSTS (middle-left)
# ============================================================
y_sec3 = 0.63
chalk_text(ax_bg, 0.25, y_sec3, 'TREATMENT COSTS', fontsize=26, color=CHALK_ORANGE, weight='bold')
chalk_underline(ax_bg, 0.08, 0.42, y_sec3 - 0.012, color=CHALK_ORANGE, lw=2)

costs = [
    ('Drug Cost', '$373K - $475K', CHALK_YELLOW),
    ('Total Care', '$500K - $1M+', CHALK_CORAL),
    ('Hospital Bill', '$2M - $2.5M', CHALK_PINK),
    ('Patient OOP', '$5.5K median', CHALK_GREEN),
]

for i, (label, amount, color) in enumerate(costs):
    cy = y_sec3 - 0.035 - i * 0.035
    chalk_text(ax_bg, 0.12, cy, label, fontsize=14, color=CHALK_WHITE, ha='left')
    chalk_text(ax_bg, 0.38, cy, amount, fontsize=16, color=color, ha='right', weight='bold')

chalk_text(ax_bg, 0.25, y_sec3 - 0.185, '50% of patients report', fontsize=13, color=CHALK_CORAL, style='italic')
chalk_text(ax_bg, 0.25, y_sec3 - 0.205, 'financial toxicity', fontsize=13, color=CHALK_CORAL, style='italic')

# ============================================================
# SECTION 4: MEDICARE REIMBURSEMENT (middle-right)
# ============================================================
chalk_text(ax_bg, 0.75, y_sec3, 'MEDICARE REIMBURSEMENT', fontsize=26, color=CHALK_BLUE, weight='bold')
chalk_underline(ax_bg, 0.54, 0.96, y_sec3 - 0.012, color=CHALK_BLUE, lw=2)

chalk_box(ax_bg, 0.56, y_sec3 - 0.09, 0.17, 0.07, color=CHALK_BLUE)
chalk_text(ax_bg, 0.645, y_sec3 - 0.04, 'FY2025', fontsize=14, color=CHALK_WHITE, weight='bold')
chalk_text(ax_bg, 0.645, y_sec3 - 0.065, '$269K', fontsize=22, color=CHALK_YELLOW, weight='bold')

chalk_arrow(ax_bg, 0.74, y_sec3 - 0.055, 0.77, y_sec3 - 0.055, color=CHALK_GREEN)

chalk_box(ax_bg, 0.78, y_sec3 - 0.09, 0.17, 0.07, color=CHALK_GREEN)
chalk_text(ax_bg, 0.865, y_sec3 - 0.04, 'FY2026', fontsize=14, color=CHALK_WHITE, weight='bold')
chalk_text(ax_bg, 0.865, y_sec3 - 0.065, '$314K', fontsize=22, color=CHALK_GREEN, weight='bold')

chalk_text(ax_bg, 0.75, y_sec3 - 0.115, 'NTAP Cap: 65% (up from 50%)', fontsize=13, color=CHALK_ORANGE)
chalk_text(ax_bg, 0.75, y_sec3 - 0.14, 'Only 2/10 eligible patients', fontsize=14, color=CHALK_CORAL, weight='bold')
chalk_text(ax_bg, 0.75, y_sec3 - 0.16, 'actually receive CAR-T', fontsize=14, color=CHALK_CORAL, weight='bold')
chalk_text(ax_bg, 0.75, y_sec3 - 0.185, 'Reimbursement gap: $100K-$300K per case', fontsize=12, color=CHALK_YELLOW, style='italic')

# ============================================================
# SECTION 5: M&A DEALS (lower-left)
# ============================================================
y_sec5 = 0.385
chalk_text(ax_bg, 0.25, y_sec5, 'MAJOR M&A DEALS', fontsize=26, color=CHALK_YELLOW, weight='bold')
chalk_underline(ax_bg, 0.08, 0.42, y_sec5 - 0.012, color=CHALK_YELLOW, lw=2)

deals = [
    ('Eli Lilly -> Orna', '$2.4B', CHALK_YELLOW),
    ('AbbVie -> Capstan', '$2.1B', CHALK_GREEN),
    ('Roche -> Poseida', '$1.5B', CHALK_BLUE),
    ('BMS -> 2seventy Bio', '$286M', CHALK_PINK),
    ('Gilead -> Kite (2017)', '$11.9B', CHALK_ORANGE),
    ('BMS -> Celgene (2019)', '$74B', CHALK_CORAL),
]

for i, (deal, val, color) in enumerate(deals):
    dy = y_sec5 - 0.035 - i * 0.033
    chalk_text(ax_bg, 0.08, dy, deal, fontsize=13, color=CHALK_WHITE, ha='left')
    chalk_text(ax_bg, 0.42, dy, val, fontsize=15, color=color, ha='right', weight='bold')

chalk_text(ax_bg, 0.25, y_sec5 - 0.245, '$32B+ total investment', fontsize=14, color=CHALK_YELLOW, weight='bold', style='italic')
chalk_text(ax_bg, 0.25, y_sec5 - 0.265, '10,000+ patents filed', fontsize=12, color=CHALK_GREEN, style='italic')

# ============================================================
# SECTION 6: FDA-APPROVED PRODUCTS (lower-right)
# ============================================================
chalk_text(ax_bg, 0.75, y_sec5, '7 FDA-APPROVED CAR-T PRODUCTS', fontsize=22, color=CHALK_GREEN, weight='bold')
chalk_underline(ax_bg, 0.54, 0.96, y_sec5 - 0.012, color=CHALK_GREEN, lw=2)

products = [
    ('Kymriah', 'Novartis', 'CD19', '2017', CHALK_ORANGE),
    ('Yescarta', 'Gilead', 'CD19', '2017', CHALK_GREEN),
    ('Tecartus', 'Gilead', 'CD19', '2020', CHALK_BLUE),
    ('Breyanzi', 'BMS', 'CD19', '2021', CHALK_PINK),
    ('Abecma', 'BMS', 'BCMA', '2021', CHALK_CORAL),
    ('Carvykti', 'Legend/J&J', 'BCMA', '2022', CHALK_YELLOW),
    ('Aucatzyl', 'Autolus', 'CD19', '2025', CHALK_WHITE),
]

for i, (name, co, target, year, color) in enumerate(products):
    py = y_sec5 - 0.035 - i * 0.03
    chalk_text(ax_bg, 0.57, py, name, fontsize=13, color=color, ha='left', weight='bold')
    chalk_text(ax_bg, 0.72, py, co, fontsize=11, color=CHALK_WHITE, ha='left')
    chalk_text(ax_bg, 0.84, py, target, fontsize=11, color=CHALK_BLUE, ha='center')
    chalk_text(ax_bg, 0.93, py, year, fontsize=11, color=CHALK_WHITE, ha='center')

chalk_text(ax_bg, 0.75, y_sec5 - 0.255, 'REMS removed June 2025', fontsize=13, color=CHALK_GREEN, style='italic')
chalk_text(ax_bg, 0.75, y_sec5 - 0.275, '1,000+ active clinical trials', fontsize=13, color=CHALK_YELLOW, style='italic')

# ============================================================
# SECTION 7: EMERGING TRENDS (bottom)
# ============================================================
y_sec7 = 0.095
chalk_text(ax_bg, 0.5, y_sec7, 'EMERGING TRENDS & FUTURE OUTLOOK', fontsize=26, color=CHALK_CORAL, weight='bold')
chalk_underline(ax_bg, 0.15, 0.85, y_sec7 - 0.012, color=CHALK_CORAL, lw=2)

trends = [
    ('IN VIVO CAR-T', '$368M -> $44.2B by 2034 (61.5% CAGR)', CHALK_YELLOW),
    ('ALLOGENEIC OFF-THE-SHELF', '2026 = defining clinical test year', CHALK_GREEN),
    ('AUTOIMMUNE DISEASES', '94% off immunosuppression in trials', CHALK_BLUE),
    ('SOLID TUMORS', 'Next frontier: glioblastoma, ovarian, lung', CHALK_PINK),
    ('COST REDUCTION', 'Manufacturing automation + outpatient shift', CHALK_ORANGE),
]

for i, (trend, detail, color) in enumerate(trends):
    tx = 0.12 + (i % 3) * 0.28
    ty = y_sec7 - 0.03 - (i // 3) * 0.04
    chalk_text(ax_bg, tx, ty, trend, fontsize=12, color=color, ha='left', weight='bold')
    chalk_text(ax_bg, tx, ty - 0.015, detail, fontsize=10, color=CHALK_WHITE, ha='left', alpha=0.8)

# ============================================================
# FOOTER
# ============================================================
chalk_text(ax_bg, 0.5, 0.01, 'Sources: Fortune Business Insights | MarketsandMarkets | BioSpace | AJMC | CMS | Legend Biotech IR | Precedence Research',
           fontsize=10, color=CHALK_WHITE, alpha=0.5)
chalk_text(ax_bg, 0.5, 0.003, 'Compiled May 2026 | CAR T-Cell Therapy Financial Analysis - US & Puerto Rico',
           fontsize=10, color=CHALK_WHITE, alpha=0.5)

# Add decorative chalk elements
for _ in range(8):
    sx = np.random.uniform(0.02, 0.98)
    sy = np.random.uniform(0.02, 0.98)
    ax_bg.plot(sx, sy, '*', color=CHALK_WHITE, alpha=0.08, markersize=15)

# Horizontal divider lines
for y_div in [0.925, 0.68, 0.43, 0.12]:
    xs = np.linspace(0.03, 0.97, 100)
    ys = y_div + np.random.normal(0, 0.001, 100)
    ax_bg.plot(xs, ys, color=CHALK_WHITE, alpha=0.15, lw=1)

# Save
output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'car_t_chalkboard_infographic.png')
fig.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='#1a1a2e', pad_inches=0.3)
plt.close()
print(f"Infographic saved to: {output_path}")
