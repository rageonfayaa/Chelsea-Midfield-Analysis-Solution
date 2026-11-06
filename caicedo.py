import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from decimal import Decimal, ROUND_HALF_UP

def round_half_up(val, decimals=2):
    """Accurate standard half-up rounding for display consistency."""
    d = Decimal(str(val))
    target = Decimal('10') ** -decimals
    return float(d.quantize(target, rounding=ROUND_HALF_UP))

script_dir = os.path.dirname(os.path.abspath(__file__))
possible_paths = [
    os.path.join(script_dir, '..', 'step2_defensive_fragility_by_pivot.csv'),
    os.path.join(script_dir, 'step2_defensive_fragility_by_pivot.csv'),
    'step2_defensive_fragility_by_pivot.csv',
    '/Users/rageonfayaa/Desktop/Data analytics /step2_defensive_fragility_by_pivot.csv'
]

csv_path = None
for path in possible_paths:
    if os.path.exists(path):
        csv_path = path
        break

if not csv_path:
    raise FileNotFoundError("Could not find step2_defensive_fragility_by_pivot.csv")

df = pd.read_csv(csv_path)

pivot_groups = [
    {
        'key': 'With Caicedo (Henderson + Caicedo)',
        'label': 'Henderson + Caicedo',
        'sublabel': '(2 games)',
        'color': '#10b981',
        'edge': '#6ee7b7'
    },
    {
        'key': 'Without Caicedo (Lavia + James/Gusto)',
        'label': 'Lavia + James/Gusto',
        'sublabel': '(4 games)',
        'color': '#f43f5e',
        'edge': '#fda4af'
    },
    {
        'key': 'Without Caicedo (Henderson + Barco)',
        'label': 'Henderson + Barco',
        'sublabel': '(1 game)',
        'color': '#f59e0b',
        'edge': '#fcd34d'
    }
]

pivot_data = {}
for p in pivot_groups:
    sub = df[df['Pivot_Category'] == p['key']]
    n_games = len(sub)
    pivot_data[p['key']] = {
        'n_games': n_games,
        'goals': round_half_up(sub['Goals_Conceded'].mean(), 2),
        'opp_xg': round_half_up(sub['Opp_xG_Sofascore'].mean(), 2),
        'box_touches': round_half_up(sub['Opp_Touches_In_Box'].mean(), 1),
        'danger_lost': round_half_up(sub['Chelsea_Danger_Poss_Lost'].mean(), 1),
    }

plt.style.use('default')

bg_color = '#0e1626'
card_color = '#152036'
text_main = '#f8fafc'
text_sub = '#94a3b8'
grid_color = '#25334d'

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 8.2), facecolor=bg_color)
ax1.set_facecolor(card_color)
ax2.set_facecolor(card_color)

width = 0.24
n_pivots = len(pivot_groups)

m1_labels = [
    "Goals Conceded\n(per game)",
    "Opponent xG\n(Shot Quality per game)"
]
x1 = np.arange(len(m1_labels))

for idx, p in enumerate(pivot_groups):
    stats = pivot_data[p['key']]
    vals = [stats['goals'], stats['opp_xg']]
    pos = x1 + (idx - 1) * width

    rects = ax1.bar(
        pos, vals, width,
        label=f"{p['label']} {p['sublabel']}",
        color=p['color'],
        edgecolor=p['edge'],
        linewidth=1.2,
        zorder=3,
        alpha=0.92
    )

    for i, val in enumerate(vals):
        ax1.annotate(
            f"{val:.2f}",
            xy=(pos[i], val),
            xytext=(0, 6),
            textcoords="offset points",
            ha='center', va='bottom',
            fontsize=10.5, fontweight='bold',
            color=text_main, zorder=5
        )

ax1.set_title("Direct Defensive Concessions", fontsize=13, fontweight='bold', color=text_main, pad=14, loc='left')
ax1.set_ylabel("Average per Game", fontsize=11, fontweight='bold', color=text_sub, labelpad=10)
ax1.set_xticks(x1)
ax1.set_xticklabels(m1_labels, fontsize=10.5, color=text_main)
ax1.set_ylim(0, 3.65)
ax1.tick_params(colors=text_sub, labelsize=10)
ax1.grid(axis='y', color=grid_color, linestyle='--', linewidth=0.8, alpha=0.7, zorder=0)
ax1.set_axisbelow(True)

for spine in ['top', 'right', 'left']:
    ax1.spines[spine].set_visible(False)
ax1.spines['bottom'].set_color(grid_color)
ax1.spines['bottom'].set_linewidth(1.1)

m2_labels = [
    "Opponent Box Touches\n(Penalty Area Penetration)",
    "Dangerous Possessions Lost\n(High-Risk Turnovers per game)"
]
x2 = np.arange(len(m2_labels))

for idx, p in enumerate(pivot_groups):
    stats = pivot_data[p['key']]
    vals = [stats['box_touches'], stats['danger_lost']]
    pos = x2 + (idx - 1) * width

    rects = ax2.bar(
        pos, vals, width,
        label=f"{p['label']} {p['sublabel']}",
        color=p['color'],
        edgecolor=p['edge'],
        linewidth=1.2,
        zorder=3,
        alpha=0.92
    )

    for i, val in enumerate(vals):
        ax2.annotate(
            f"{val:.1f}",
            xy=(pos[i], val),
            xytext=(0, 6),
            textcoords="offset points",
            ha='center', va='bottom',
            fontsize=10.5, fontweight='bold',
            color=text_main, zorder=5
        )

ax2.set_title("Defensive Territory & Risk Exposure", fontsize=13, fontweight='bold', color=text_main, pad=14, loc='left')
ax2.set_ylabel("Average per Game", fontsize=11, fontweight='bold', color=text_sub, labelpad=10)
ax2.set_xticks(x2)
ax2.set_xticklabels(m2_labels, fontsize=10.5, color=text_main)
ax2.set_ylim(0, 34)
ax2.tick_params(colors=text_sub, labelsize=10)
ax2.grid(axis='y', color=grid_color, linestyle='--', linewidth=0.8, alpha=0.7, zorder=0)
ax2.set_axisbelow(True)

for spine in ['top', 'right', 'left']:
    ax2.spines[spine].set_visible(False)
ax2.spines['bottom'].set_color(grid_color)
ax2.spines['bottom'].set_linewidth(1.1)

fig.suptitle("CHELSEA FC : DEFENSIVE FRAGILITY BY MIDFIELD PIVOT",
             fontsize=17, fontweight='bold', color=text_main, x=0.5, y=0.97, ha='center')

plt.figtext(0.5, 0.925,
            "Comparing 4 defensive averages across starting pivot pairings (2026/27 Season | 7 matches)",
            fontsize=11, color=text_sub, ha='center')

handles, labels = ax1.get_legend_handles_labels()
legend = fig.legend(
    handles, labels,
    loc='lower center',
    bbox_to_anchor=(0.5, 0.845),
    ncol=3,
    frameon=True,
    facecolor=bg_color,
    edgecolor=grid_color,
    fontsize=10,
    labelcolor=text_main,
    framealpha=0.92
)
legend.get_frame().set_linewidth(1.0)

fig.text(0.06, 0.02,
         "Data source: step2_defensive_fragility_by_pivot.csv | Henderson + Caicedo conceded only 0.50 goals & 0.90 xG per game",
         fontsize=8.5, color=text_sub, ha='left')

plt.tight_layout(rect=[0.05, 0.04, 0.95, 0.84])

output_path = os.path.join(script_dir, 'defensive_pivot_comparison.png')
plt.savefig(output_path, dpi=300, facecolor=bg_color, bbox_inches='tight')
print(f"Defensive comparison plot saved successfully to: {output_path}")

plt.show()
