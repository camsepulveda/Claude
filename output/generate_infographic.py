#!/usr/bin/env python3
"""Generate a chalkboard/handwritten style infographic for CAR T Cell Financial Analysis."""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np
import random

# --- Configuration ---
FIG_WIDTH, FIG_HEIGHT = 24, 36
BG_COLOR = '#1a2a1a'  # Dark green chalkboard
CHALK_WHITE = '#e8e4d8'
CHALK_YELLOW = '#f5e6a3'
CHALK_BLUE = '#8ec8e8'
CHALK_PINK = '#f0a0a0'
CHALK_GREEN = '#a8d8a8'
CHALK_ORANGE = '#f5c078'

random.seed(42)


def chalk_effect_text(ax, x, y, text, fontsize=14, color=CHALK_WHITE, ha='left',
                      va='center', fontweight='normal', rotation=0, alpha=0.88):
    """Draw text with chalk-like appearance."""
    # Slight shadow for depth
    ax.text(x + 0.001, y - 0.001, text, fontsize=fontsize, color=color,
            ha=ha, va=va, fontweight=fontweight, fontfamily='serif',
            alpha=alpha * 0.3, rotation=rotation,
            transform=ax.transAxes)
    ax.text(x, y, text, fontsize=fontsize, color=color,
            ha=ha, va=va, fontweight=fontweight, fontfamily='serif',
            alpha=alpha, rotation=rotation,
            transform=ax.transAxes)


def draw_chalk_line(ax, x1, y1, x2, y2, color=CHALK_WHITE, lw=1.5, alpha=0.5):
    """Draw a slightly wobbly chalk line."""
    n_points = 20
    x = np.linspace(x1, x2, n_points)
    y = np.linspace(y1, y2, n_points)
    wobble = 0.001
    x += np.random.normal(0, wobble, n_points)
    y += np.random.normal(0, wobble, n_points)
    ax.plot(x, y, color=color, linewidth=lw, alpha=alpha, transform=ax.transAxes)


def draw_chalk_box(ax, x, y, w, h, color=CHALK_WHITE, lw=1.5, alpha=0.4):
    """Draw a chalk-style box."""
    draw_chalk_line(ax, x, y, x + w, y, color=color, lw=lw, alpha=alpha)
    draw_chalk_line(ax, x + w, y, x + w, y + h, color=color, lw=lw, alpha=alpha)
    draw_chalk_line(ax, x + w, y + h, x, y + h, color=color, lw=lw, alpha=alpha)
    draw_chalk_line(ax, x, y + h, x, y, color=color, lw=lw, alpha=alpha)


def draw_chalk_arrow(ax, x1, y1, x2, y2, color=CHALK_YELLOW, lw=2, alpha=0.7):
    """Draw a chalk-style arrow."""
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                xycoords='axes fraction', textcoords='axes fraction',
                arrowprops=dict(arrowstyle='->', color=color, lw=lw,
                               connectionstyle='arc3,rad=0.1'),
                alpha=alpha)


def draw_bar_chart(ax, x_start, y_start, width, height, values, labels, colors, title):
    """Draw a chalk-style bar chart."""
    chalk_effect_text(ax, x_start + width / 2, y_start + height + 0.015, title,
                      fontsize=16, color=CHALK_YELLOW, ha='center', fontweight='bold')

    n = len(values)
    max_val = max(values)
    bar_width = width / (n * 1.8)
    gap = width / (n * 3.5)

    for i, (val, label, col) in enumerate(zip(values, labels, colors)):
        bx = x_start + gap + i * (bar_width + gap)
        bar_h = (val / max_val) * height * 0.85

        # Draw bar with chalk texture
        rect = FancyBboxPatch((bx, y_start), bar_width, bar_h,
                              boxstyle="round,pad=0.002",
                              facecolor=col, edgecolor=col,
                              alpha=0.45, linewidth=1.5,
                              transform=ax.transAxes)
        ax.add_patch(rect)

        # Value on top
        chalk_effect_text(ax, bx + bar_width / 2, y_start + bar_h + 0.005,
                          f'${val}B' if val >= 1 else f'${int(val * 1000)}M',
                          fontsize=11, color=col, ha='center', fontweight='bold')

        # Label below
        chalk_effect_text(ax, bx + bar_width / 2, y_start - 0.012, label,
                          fontsize=9, color=CHALK_WHITE, ha='center', rotation=25)


def draw_chalk_dust(ax):
    """Add subtle chalk dust particles."""
    for _ in range(300):
        x = random.random()
        y = random.random()
        size = random.uniform(0.1, 1.5)
        alpha = random.uniform(0.02, 0.08)
        ax.plot(x, y, 'o', color=CHALK_WHITE, markersize=size, alpha=alpha,
                transform=ax.transAxes)


def draw_doodle_circle(ax, x, y, r, color=CHALK_YELLOW, lw=1.5, alpha=0.5):
    """Draw a hand-drawn looking circle."""
    theta = np.linspace(0, 2 * np.pi, 60)
    wobble = r * 0.08
    cx = x + r * np.cos(theta) + np.random.normal(0, wobble, len(theta))
    cy = y + r * np.sin(theta) + np.random.normal(0, wobble, len(theta))
    ax.plot(cx, cy, color=color, linewidth=lw, alpha=alpha, transform=ax.transAxes)


def draw_underline(ax, x, y, length, color=CHALK_YELLOW, lw=2, alpha=0.6):
    """Draw a wobbly underline."""
    draw_chalk_line(ax, x, y, x + length, y, color=color, lw=lw, alpha=alpha)


def main():
    fig, ax = plt.subplots(1, 1, figsize=(FIG_WIDTH, FIG_HEIGHT))
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    # Add chalk dust texture
    draw_chalk_dust(ax)

    # === TITLE ===
    chalk_effect_text(ax, 0.5, 0.975, 'CAR T-Cell Therapy', fontsize=42,
                      color=CHALK_YELLOW, ha='center', fontweight='bold', alpha=0.92)
    chalk_effect_text(ax, 0.5, 0.960, 'Financial Analysis 2025-2026', fontsize=32,
                      color=CHALK_WHITE, ha='center', fontweight='bold', alpha=0.85)
    draw_underline(ax, 0.15, 0.952, 0.70, color=CHALK_YELLOW, lw=2.5)

    # === SECTION 1: Market Overview (top left) ===
    y_sec1 = 0.935
    chalk_effect_text(ax, 0.05, y_sec1, '[=] Market Overview', fontsize=22,
                      color=CHALK_GREEN, ha='left', fontweight='bold')
    draw_underline(ax, 0.05, y_sec1 - 0.008, 0.35, color=CHALK_GREEN, lw=1.5)

    draw_chalk_box(ax, 0.05, 0.855, 0.40, 0.070, color=CHALK_GREEN, alpha=0.3)
    chalk_effect_text(ax, 0.08, 0.910, '2025:  $6.03 Billion', fontsize=18,
                      color=CHALK_WHITE, fontweight='bold')
    chalk_effect_text(ax, 0.08, 0.892, '2026:  $7.24 Billion', fontsize=18,
                      color=CHALK_WHITE, fontweight='bold')
    chalk_effect_text(ax, 0.08, 0.874, '2031:  $13.78 Billion', fontsize=18,
                      color=CHALK_YELLOW, fontweight='bold')
    chalk_effect_text(ax, 0.08, 0.860, 'CAGR: 13.7%', fontsize=16,
                      color=CHALK_ORANGE)

    draw_chalk_arrow(ax, 0.30, 0.862, 0.38, 0.920, color=CHALK_GREEN, lw=2.5)
    chalk_effect_text(ax, 0.385, 0.925, '>>  Growth', fontsize=13,
                      color=CHALK_GREEN, fontweight='bold')

    # === SECTION 2: Key Stats (top right) ===
    chalk_effect_text(ax, 0.55, y_sec1, '[*] Key Stats', fontsize=22,
                      color=CHALK_BLUE, ha='left', fontweight='bold')
    draw_underline(ax, 0.55, y_sec1 - 0.008, 0.25, color=CHALK_BLUE, lw=1.5)

    stats = [
        ('7', 'FDA-Approved Products'),
        ('70.4%', 'North America Market Share'),
        ('$32B+', 'Total Capital Invested'),
        ('$373K-$475K', 'Treatment Cost Per Patient'),
    ]
    for i, (val, label) in enumerate(stats):
        yy = 0.915 - i * 0.022
        draw_doodle_circle(ax, 0.57, yy, 0.008, color=CHALK_BLUE, alpha=0.4)
        chalk_effect_text(ax, 0.59, yy, val, fontsize=16, color=CHALK_YELLOW, fontweight='bold')
        chalk_effect_text(ax, 0.70, yy, label, fontsize=13, color=CHALK_WHITE)

    # === DIVIDER ===
    draw_chalk_line(ax, 0.05, 0.838, 0.95, 0.838, color=CHALK_WHITE, lw=1, alpha=0.3)

    # === SECTION 3: Product Revenue Bar Chart ===
    y_bar = 0.83
    chalk_effect_text(ax, 0.5, y_bar, '[$] Product Revenue Leaders (2024-2025)', fontsize=22,
                      color=CHALK_ORANGE, ha='center', fontweight='bold')
    draw_underline(ax, 0.15, y_bar - 0.008, 0.70, color=CHALK_ORANGE, lw=1.5)

    products = ['Yescarta', 'CARVYKTI', 'Kymriah', 'Tecartus', 'Breyanzi']
    revenues = [1.6, 0.963, 0.536, 0.370, 0.350]
    bar_colors = [CHALK_BLUE, CHALK_GREEN, CHALK_PINK, CHALK_ORANGE, CHALK_YELLOW]

    # Draw bars
    bar_area_x = 0.08
    bar_area_y = 0.700
    bar_area_w = 0.84
    bar_area_h = 0.110

    n = len(products)
    max_rev = max(revenues)
    bar_w = bar_area_w / (n * 1.6)
    gap = bar_area_w / (n * 4)

    for i, (prod, rev, col) in enumerate(zip(products, revenues, bar_colors)):
        bx = bar_area_x + gap + i * (bar_w + gap)
        bh = (rev / max_rev) * bar_area_h

        # Fill bar with chalk-like rectangles
        for j in range(int(bh * 800)):
            yy = bar_area_y + j / 800.0
            if yy > bar_area_y + bh:
                break
            ax.plot([bx + 0.005, bx + bar_w - 0.005], [yy, yy],
                    color=col, alpha=0.12, linewidth=2, transform=ax.transAxes)

        # Border
        draw_chalk_box(ax, bx, bar_area_y, bar_w, bh, color=col, lw=2, alpha=0.6)

        # Value
        chalk_effect_text(ax, bx + bar_w / 2, bar_area_y + bh + 0.008,
                          f'${rev}B' if rev >= 1 else f'${int(rev * 1000)}M',
                          fontsize=14, color=col, ha='center', fontweight='bold')

        # Label
        chalk_effect_text(ax, bx + bar_w / 2, bar_area_y - 0.015, prod,
                          fontsize=12, color=CHALK_WHITE, ha='center')

    # Company names under product names
    companies = ['Gilead/Kite', 'J&J/Legend', 'Novartis', 'Gilead/Kite', 'BMS']
    for i, (comp, col) in enumerate(zip(companies, bar_colors)):
        bx = bar_area_x + gap + i * (bar_w + gap)
        chalk_effect_text(ax, bx + bar_w / 2, bar_area_y - 0.030, comp,
                          fontsize=9, color=col, ha='center', alpha=0.7)

    # CARVYKTI callout
    chalk_effect_text(ax, 0.50, 0.670, '[*] CARVYKTI: 93% YoY Growth — On pace for #1 by 2026!',
                      fontsize=14, color=CHALK_GREEN, ha='center', fontweight='bold')

    # === DIVIDER ===
    draw_chalk_line(ax, 0.05, 0.655, 0.95, 0.655, color=CHALK_WHITE, lw=1, alpha=0.3)

    # === SECTION 4: M&A Deals (left side) ===
    y_ma = 0.645
    chalk_effect_text(ax, 0.05, y_ma, '[<>] Major M&A Deals', fontsize=22,
                      color=CHALK_PINK, ha='left', fontweight='bold')
    draw_underline(ax, 0.05, y_ma - 0.008, 0.38, color=CHALK_PINK, lw=1.5)

    deals = [
        ('Eli Lilly -> Orna', '$2.4B', CHALK_YELLOW),
        ('AbbVie -> Capstan', '$2.1B', CHALK_ORANGE),
        ('Roche -> Poseida', '$1.5B', CHALK_GREEN),
        ('BMS -> Orbital', '$1.5B', CHALK_BLUE),
        ('AstraZeneca -> EsoBiotec', '$1.0B', CHALK_PINK),
        ('Gilead -> Interius', '$350M', CHALK_WHITE),
        ('BMS -> 2seventy Bio', '$286M', CHALK_WHITE),
    ]

    for i, (deal, val, col) in enumerate(deals):
        yy = 0.622 - i * 0.020
        chalk_effect_text(ax, 0.07, yy, deal, fontsize=13, color=CHALK_WHITE)
        chalk_effect_text(ax, 0.35, yy, val, fontsize=14, color=col, fontweight='bold')

    # Total box
    draw_chalk_box(ax, 0.06, 0.465, 0.36, 0.025, color=CHALK_PINK, alpha=0.4)
    chalk_effect_text(ax, 0.24, 0.478, 'Total In Vivo Deals: >$7.3B',
                      fontsize=15, color=CHALK_PINK, ha='center', fontweight='bold')

    # === SECTION 5: Three Converging Forces (right side) ===
    chalk_effect_text(ax, 0.55, y_ma, '[!] Three Converging Forces (2026)', fontsize=20,
                      color=CHALK_YELLOW, ha='left', fontweight='bold')
    draw_underline(ax, 0.55, y_ma - 0.008, 0.40, color=CHALK_YELLOW, lw=1.5)

    forces = [
        ('1. Expanded Indications', 'Moving CAR-T into earlier\n   treatment lines', CHALK_GREEN),
        ('2. Next-Gen Platforms', 'Allogeneic (off-the-shelf) &\n   in vivo CAR-T', CHALK_BLUE),
        ('3. Autoimmune Expansion', 'Beyond oncology into\n   autoimmune diseases', CHALK_ORANGE),
    ]

    for i, (title, desc, col) in enumerate(forces):
        yy = 0.620 - i * 0.055
        draw_chalk_box(ax, 0.54, yy - 0.020, 0.42, 0.045, color=col, alpha=0.25)
        chalk_effect_text(ax, 0.56, yy + 0.010, title, fontsize=15, color=col, fontweight='bold')
        chalk_effect_text(ax, 0.56, yy - 0.008, desc, fontsize=11, color=CHALK_WHITE)

    # === SECTION 6: In Vivo CAR-T Emerging Market ===
    draw_chalk_line(ax, 0.55, 0.455, 0.95, 0.455, color=CHALK_WHITE, lw=1, alpha=0.3)
    chalk_effect_text(ax, 0.55, 0.445, '[~] In Vivo CAR-T Market', fontsize=18,
                      color=CHALK_GREEN, fontweight='bold')

    chalk_effect_text(ax, 0.57, 0.420, '2024: $368M', fontsize=14, color=CHALK_WHITE)
    draw_chalk_arrow(ax, 0.68, 0.420, 0.73, 0.420, color=CHALK_GREEN, lw=2)
    chalk_effect_text(ax, 0.74, 0.420, '2034: $44.2B', fontsize=14,
                      color=CHALK_GREEN, fontweight='bold')
    chalk_effect_text(ax, 0.57, 0.400, 'CAGR: 61.5% — The Fastest Growing Segment',
                      fontsize=13, color=CHALK_YELLOW)

    # === DIVIDER ===
    draw_chalk_line(ax, 0.05, 0.440, 0.95, 0.440, color=CHALK_WHITE, lw=1, alpha=0.3)

    # === SECTION 7: Cost Challenge ===
    y_cost = 0.430
    chalk_effect_text(ax, 0.05, y_cost, '[$] The Cost Challenge', fontsize=22,
                      color=CHALK_ORANGE, ha='left', fontweight='bold')
    draw_underline(ax, 0.05, y_cost - 0.008, 0.35, color=CHALK_ORANGE, lw=1.5)

    cost_items = [
        ('US Treatment Cost', '$373K - $475K', CHALK_PINK),
        ('Total w/ Hospital Care', '$500K - $1M+', CHALK_PINK),
        ('India (NexCAR19)', '$30K - $50K', CHALK_GREEN),
        ('Barcelona Hospital', '$97K', CHALK_GREEN),
        ('Target Allogeneic 2030', '$150K', CHALK_YELLOW),
    ]

    for i, (item, cost, col) in enumerate(cost_items):
        yy = 0.408 - i * 0.020
        chalk_effect_text(ax, 0.07, yy, item, fontsize=13, color=CHALK_WHITE)
        chalk_effect_text(ax, 0.32, yy, cost, fontsize=13, color=col, fontweight='bold')

    # Cost reduction arrow
    draw_chalk_arrow(ax, 0.38, 0.410, 0.38, 0.330, color=CHALK_GREEN, lw=3)
    chalk_effect_text(ax, 0.40, 0.370, 'Cost\nReduction\nTrend', fontsize=11,
                      color=CHALK_GREEN, fontweight='bold')

    # === SECTION 8: Companies to Watch (right) ===
    chalk_effect_text(ax, 0.55, y_cost, '[#] Key Players & Strategies', fontsize=20,
                      color=CHALK_BLUE, ha='left', fontweight='bold')
    draw_underline(ax, 0.55, y_cost - 0.008, 0.40, color=CHALK_BLUE, lw=1.5)

    players = [
        ('Gilead/Kite', '4x cell-processing output by 2026', CHALK_BLUE),
        ('J&J/Legend', 'Earlier-line myeloma expansion', CHALK_GREEN),
        ('Bristol Myers', 'Automated closed manufacturing', CHALK_PINK),
        ('Novartis', 'Next-gen solid tumor constructs', CHALK_ORANGE),
        ('Cartesian', 'mRNA CAR-T for autoimmune', CHALK_YELLOW),
    ]

    for i, (company, strategy, col) in enumerate(players):
        yy = 0.405 - i * 0.022
        draw_doodle_circle(ax, 0.57, yy, 0.006, color=col, alpha=0.5)
        chalk_effect_text(ax, 0.59, yy, company, fontsize=13, color=col, fontweight='bold')
        chalk_effect_text(ax, 0.72, yy, strategy, fontsize=11, color=CHALK_WHITE)

    # === DIVIDER ===
    draw_chalk_line(ax, 0.05, 0.295, 0.95, 0.295, color=CHALK_WHITE, lw=1, alpha=0.3)

    # === SECTION 9: Investment Trends ===
    y_inv = 0.285
    chalk_effect_text(ax, 0.5, y_inv, '[^] Investment & Financing Trends', fontsize=22,
                      color=CHALK_YELLOW, ha='center', fontweight='bold')
    draw_underline(ax, 0.15, y_inv - 0.008, 0.70, color=CHALK_YELLOW, lw=1.5)

    # Investment timeline
    inv_data = [
        ('Total Capital', '$32B+', 'invested over recent years', CHALK_YELLOW),
        ('2024-Q2 2025', '$2.3B', 'across 52 rounds (avg $47M)', CHALK_BLUE),
        ('Q3 2025 Series D+', '$832M', 'surged from $14M in one quarter', CHALK_GREEN),
        ('Diversification', '28 financings', 'spanning 10+ modalities', CHALK_ORANGE),
    ]

    for i, (period, amount, detail, col) in enumerate(inv_data):
        yy = 0.262 - i * 0.025
        xb = 0.08 + i * 0.22
        draw_chalk_box(ax, xb, yy - 0.012, 0.20, 0.030, color=col, alpha=0.25)
        chalk_effect_text(ax, xb + 0.10, yy + 0.008, period, fontsize=12,
                          color=col, ha='center', fontweight='bold')
        chalk_effect_text(ax, xb + 0.10, yy - 0.005, amount, fontsize=15,
                          color=CHALK_WHITE, ha='center', fontweight='bold')
        if i < 3:
            draw_chalk_arrow(ax, xb + 0.20, yy, xb + 0.22, yy, color=col, lw=1.5)

    chalk_effect_text(ax, 0.5, 0.195, 'Signal: Late-stage investors selectively re-entering de-risked assets',
                      fontsize=13, color=CHALK_YELLOW, ha='center')

    # === DIVIDER ===
    draw_chalk_line(ax, 0.05, 0.178, 0.95, 0.178, color=CHALK_WHITE, lw=1, alpha=0.3)

    # === SECTION 10: Regional Growth ===
    y_reg = 0.168
    chalk_effect_text(ax, 0.05, y_reg, '[@] Regional Growth', fontsize=20,
                      color=CHALK_GREEN, ha='left', fontweight='bold')
    draw_underline(ax, 0.05, y_reg - 0.008, 0.30, color=CHALK_GREEN, lw=1.5)

    regions = [
        ('North America', '70.4% share', CHALK_BLUE),
        ('Europe', '33.2% CAGR', CHALK_PINK),
        ('Asia-Pacific', '21% CAGR (fastest)', CHALK_GREEN),
    ]

    for i, (region, growth, col) in enumerate(regions):
        xb = 0.08 + i * 0.30
        yy = 0.140
        draw_chalk_box(ax, xb, yy - 0.010, 0.25, 0.030, color=col, alpha=0.25)
        chalk_effect_text(ax, xb + 0.125, yy + 0.010, region, fontsize=14,
                          color=col, ha='center', fontweight='bold')
        chalk_effect_text(ax, xb + 0.125, yy - 0.005, growth, fontsize=13,
                          color=CHALK_WHITE, ha='center')

    # === SECTION 11: Market Projections ===
    y_proj = 0.168
    chalk_effect_text(ax, 0.55, y_proj, '[>] Long-Term Projections', fontsize=20,
                      color=CHALK_ORANGE, ha='left', fontweight='bold')
    draw_underline(ax, 0.55, y_proj - 0.008, 0.35, color=CHALK_ORANGE, lw=1.5)

    projections = [
        ('2025', '$6.0B'),
        ('2026', '$7.2B'),
        ('2031', '$13.8B'),
        ('2034', '$19-189B'),
        ('2035', '$46-218B'),
    ]

    for i, (year, val) in enumerate(projections):
        xb = 0.57 + i * 0.08
        yy = 0.140
        h = 0.005 + i * 0.005
        # Growing bars
        for j in range(int(h * 500)):
            jy = yy - 0.005 + j / 500.0
            if jy > yy - 0.005 + h:
                break
            ax.plot([xb, xb + 0.05], [jy, jy], color=CHALK_ORANGE,
                    alpha=0.15, linewidth=2, transform=ax.transAxes)
        draw_chalk_box(ax, xb, yy - 0.005, 0.05, h, color=CHALK_ORANGE, alpha=0.5)
        chalk_effect_text(ax, xb + 0.025, yy - 0.005 + h + 0.005, val,
                          fontsize=10, color=CHALK_ORANGE, ha='center', fontweight='bold')
        chalk_effect_text(ax, xb + 0.025, yy - 0.015, year,
                          fontsize=10, color=CHALK_WHITE, ha='center')

    # === DIVIDER ===
    draw_chalk_line(ax, 0.05, 0.095, 0.95, 0.095, color=CHALK_WHITE, lw=1, alpha=0.3)

    # === BOTTOM: Key Takeaway ===
    draw_chalk_box(ax, 0.05, 0.025, 0.90, 0.060, color=CHALK_YELLOW, lw=2.5, alpha=0.5)
    chalk_effect_text(ax, 0.5, 0.070, '[**] KEY TAKEAWAY', fontsize=20,
                      color=CHALK_YELLOW, ha='center', fontweight='bold')
    chalk_effect_text(ax, 0.5, 0.048,
                      'CAR T-cell therapy is at an inflection point: $7B+ market with 13.7% CAGR,',
                      fontsize=14, color=CHALK_WHITE, ha='center')
    chalk_effect_text(ax, 0.5, 0.033,
                      'driven by CARVYKTI\'s explosive growth, >$7.3B in M&A, and the promise of',
                      fontsize=14, color=CHALK_WHITE, ha='center')
    chalk_effect_text(ax, 0.5, 0.018,
                      'in vivo CAR-T (61.5% CAGR) to solve cost & scalability challenges.',
                      fontsize=14, color=CHALK_GREEN, ha='center', fontweight='bold')

    # === Footer ===
    chalk_effect_text(ax, 0.5, 0.005, 'Research compiled March 2026 | Sources: MarketsandMarkets, Fortune BI, DelveInsight, BioPharma Dive, Morgan Stanley, Labiotech',
                      fontsize=9, color=CHALK_WHITE, ha='center', alpha=0.5)

    # Save
    plt.tight_layout(pad=0.5)
    plt.savefig('/home/user/Claude/output/car_t_cell_infographic.png',
                dpi=150, bbox_inches='tight', facecolor=BG_COLOR,
                edgecolor='none', pad_inches=0.3)
    plt.close()
    print("Infographic saved to /home/user/Claude/output/car_t_cell_infographic.png")


if __name__ == '__main__':
    main()
