import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from decimal import Decimal, ROUND_HALF_UP

def round_half_up(val, decimals=1):
    """Accurate standard half-up rounding for display consistency."""
    d = Decimal(str(val))
    target = Decimal('10') ** -decimals
    return float(d.quantize(target, rounding=ROUND_HALF_UP))

script_dir = os.path.dirname(os.path.abspath(__file__))
possible_paths = [
    os.path.join(script_dir, '..', 'step1_team_matches_with_vs_without_henderson.csv'),
    os.path.join(script_dir, 'step1_team_matches_with_vs_without_henderson.csv'),
    'step1_team_matches_with_vs_without_henderson.csv',
    '/Users/rageonfayaa/Desktop/Data analytics /step1_team_matches_with_vs_without_henderson.csv'
]

csv_path = None
for path in possible_paths:
    if os.path.exists(path):
        csv_path = path
        break

if not csv_path:
    raise FileNotFoundError("Could not find step1_team_matches_with_vs_without_henderson.csv")

df = pd.read_csv(csv_path)

with_h = df[df['Henderson_Played'] == 'Yes']
without_h = df[df['Henderson_Played'] == 'No']

n_with = len(with_h)
n_without = len(without_h)

metrics = [
    {
        'name': 'Buildup Completion %',
        'subname': '(Retention: 1st/2nd Phase)',
        'col': 'Buildup_Completion_pct',
        'is_pct': True,
        'with_val': round_half_up(with_h['Buildup_Completion_pct'].mean(), 1),
        'without_val': round_half_up(without_h['Buildup_Completion_pct'].mean(), 1),
    },
    {
        'name': 'Possession %',
        'subname': '(Match Control)',
        'col': 'Possession_pct',
        'is_pct': True,
        'with_val': round_half_up(with_h['Possession_pct'].mean(), 1),
        'without_val': round_half_up(without_h['Possession_pct'].mean(), 1),
    },
    {
        'name': 'Final Third Entries',
        'subname': '(Progression / Game)',
        'col': 'Final_Third_Entries',
        'is_pct': False,
        'with_val': round_half_up(with_h['Final_Third_Entries'].mean(), 1),
        'without_val': round_half_up(without_h['Final_Third_Entries'].mean(), 1),
    },
    {
        'name': 'Deep Entries',
        'subname': '(Box Threat / Game)',
        'col': 'Deep_Entries',
        'is_pct': False,
        'with_val': round_half_up(with_h['Deep_Entries'].mean(), 1),
        'without_val': round_half_up(without_h['Deep_Entries'].mean(), 1),
    }
]

plt.style.use('default')

bg_color = '#0e1626'
card_color = '#152036'
text_main = '#f8fafc'
text_sub = '#94a3b8'
grid_color = '#334155'

color_with = '#0070f3'
color_without = '#f43f5e'

fig, ax = plt.subplots(figsize=(11, 7), facecolor=bg_color)
ax.set_facecolor(card_color)

x = np.arange(len(metrics))
width = 0.36

with_vals = [m['with_val'] for m in metrics]
without_vals = [m['without_val'] for m in metrics]

rects_with = ax.bar(x - width/2, with_vals, width, label=f'With Henderson ({n_with} games)',
                    color=color_with, edgecolor='#38bdf8', linewidth=1.2, zorder=3, alpha=0.92)
rects_without = ax.bar(x + width/2, without_vals, width, label=f'Without Henderson ({n_without} games)',
                       color=color_without, edgecolor='#fda4af', linewidth=1.2, zorder=3, alpha=0.92)

for i, m in enumerate(metrics):
    val_w = m['with_val']
    val_wo = m['without_val']
    diff = round_half_up(val_w - val_wo, 1)
    is_pct = m['is_pct']

    fmt_w = f"{val_w:.1f}%" if is_pct else f"{val_w:.1f}"
    fmt_wo = f"{val_wo:.1f}%" if is_pct else f"{val_wo:.1f}"

    ax.annotate(fmt_w,
                xy=(x[i] - width/2, val_w),
                xytext=(0, 7),
                textcoords="offset points",
                ha='center', va='bottom',
                fontsize=11.5, fontweight='bold', color=text_main)

    ax.annotate(fmt_wo,
                xy=(x[i] + width/2, val_wo),
                xytext=(0, 7),
                textcoords="offset points",
                ha='center', va='bottom',
                fontsize=11.5, fontweight='bold', color=text_main)

    max_val = max(val_w, val_wo)
    sign = "+" if diff > 0 else ""
    diff_fmt = f"{sign}{diff:.1f}%" if is_pct else f"{sign}{diff:.1f}"
    diff_color = '#4ade80' if diff > 0 else '#fb7185'

    ax.annotate(f"Diff: {diff_fmt}",
                xy=(x[i], max_val + 13),
                ha='center', va='center',
                fontsize=9.5, fontweight='bold',
                color=diff_color,
                bbox=dict(boxstyle="round,pad=0.28", facecolor=bg_color, edgecolor=diff_color, alpha=0.9, lw=0.8))

category_labels = [f"{m['name']}\n{m['subname']}" for m in metrics]
ax.set_xticks(x)
ax.set_xticklabels(category_labels, fontsize=10.5, color=text_main)

ax.set_ylabel("Metric Value", fontsize=11, fontweight='bold', color=text_sub, labelpad=12)
ax.set_ylim(0, 105)
ax.tick_params(axis='y', colors=text_sub, labelsize=10)
ax.tick_params(axis='x', colors=text_main, length=0, pad=8)

ax.grid(axis='y', color=grid_color, linestyle='--', linewidth=0.8, alpha=0.6, zorder=0)
ax.set_axisbelow(True)

for spine in ['top', 'right', 'left']:
    ax.spines[spine].set_visible(False)
ax.spines['bottom'].set_color(grid_color)
ax.spines['bottom'].set_linewidth(1.2)

fig.suptitle("CHELSEA FC : TEAM PERFORMANCE IMPACT",
             fontsize=17, fontweight='bold', color=text_main, x=0.125, y=0.97, ha='left')

plt.title("Team averages with Jordan Henderson (3 games) vs. without Henderson (4 games)",
          fontsize=11.5, color=text_sub, pad=18, loc='left')

legend = ax.legend(loc='upper right', frameon=True, facecolor=bg_color, edgecolor=grid_color,
                   fontsize=10.5, labelcolor=text_main, framealpha=0.9)
legend.get_frame().set_linewidth(1.0)

fig.text(0.125, 0.02,
         "Data source: step1_team_matches_with_vs_without_henderson.csv | Analysis across 2026/27 matches",
         fontsize=8.5, color=text_sub, ha='left')

plt.tight_layout(rect=[0, 0.03, 1, 0.94])

output_path = os.path.join(script_dir, 'henderson_comparison.png')
plt.savefig(output_path, dpi=300, facecolor=fig.get_facecolor(), bbox_inches='tight')
print(f"Plot saved successfully to: {output_path}")

plt.show()
