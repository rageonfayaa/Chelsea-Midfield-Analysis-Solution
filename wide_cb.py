import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

script_dir = os.path.dirname(os.path.abspath(__file__))
possible_paths = [
    os.path.join(script_dir, '..', 'step2_squad_defensive_workload_per90.csv'),
    os.path.join(script_dir, 'step2_squad_defensive_workload_per90.csv'),
    'step2_squad_defensive_workload_per90.csv',
    '/Users/rageonfayaa/Desktop/Data analytics /step2_squad_defensive_workload_per90.csv'
]

csv_path = None
for path in possible_paths:
    if os.path.exists(path):
        csv_path = path
        break

if not csv_path:
    raise FileNotFoundError("Could not find step2_squad_defensive_workload_per90.csv")

df = pd.read_csv(csv_path)

def harmonize_zone(zone_str):
    z = str(zone_str).lower()
    if 'wide cb' in z:
        return 'Wide CB (Channel Defender)'
    elif 'central cb' in z:
        return 'Central CB (Sweeper)'
    elif 'pivot' in z or 'central midfield' in z:
        return 'Central Midfield (Pivot)'
    elif 'wing-back' in z:
        return 'Wing-Back'
    elif 'attacking mid' in z or 'striker' in z or 'winger' in z:
        return 'Attacker / Forward'
    return 'Other'

df['Macro_Zone'] = df['Tactical_Zone'].apply(harmonize_zone)

zone_colors = {
    'Wide CB (Channel Defender)': '#38bdf8',
    'Central CB (Sweeper)': '#a855f7',
    'Central Midfield (Pivot)': '#10b981',
    'Wing-Back': '#f59e0b',
    'Attacker / Forward': '#f43f5e'
}

zone_edges = {
    'Wide CB (Channel Defender)': '#e0f2fe',
    'Central CB (Sweeper)': '#f3e8ff',
    'Central Midfield (Pivot)': '#d1fae5',
    'Wing-Back': '#fef3c7',
    'Attacker / Forward': '#ffe4e6'
}

plt.style.use('default')

bg_color = '#0b0f17'
grid_color = '#1e293b'
text_main = '#f8fafc'
text_sub = '#94a3b8'
text_faint = '#475569'

fig, ax = plt.subplots(figsize=(13.5, 8.5), facecolor=bg_color)
ax.set_facecolor(bg_color)

med_x = df['TKLA_per90'].median()
med_y = df['TKL_pct'].median()

ax.axvline(med_x, color='#334155', linestyle='--', linewidth=0.9, alpha=0.7, zorder=1)
ax.axhline(med_y, color='#334155', linestyle='--', linewidth=0.9, alpha=0.7, zorder=1)

quadrant_font = dict(fontsize=8.5, color=text_faint, fontweight='bold', zorder=1)
ax.text(3.9, 98.5, "HIGH VOLUME · HIGH SUCCESS", ha='right', va='top', **quadrant_font)
ax.text(0.35, 98.5, "LOW VOLUME · HIGH SUCCESS", ha='left', va='top', **quadrant_font)
ax.text(3.9, 44.5, "HIGH VOLUME · LOWER SUCCESS", ha='right', va='bottom', **quadrant_font)
ax.text(0.35, 44.5, "LOW VOLUME · LOWER SUCCESS", ha='left', va='bottom', **quadrant_font)

for zone, group in df.groupby('Macro_Zone'):
    c = zone_colors[zone]
    edge = zone_edges[zone]
    
    is_wide_cb = 'Wide CB' in zone
    size = 200 if is_wide_cb else 140
    
    ax.scatter(
        group['TKLA_per90'], group['TKL_pct'],
        s=size, color=c, edgecolors=edge, linewidth=1.5,
        alpha=0.95, zorder=4, label=zone
    )

label_configs = {
    'Josh Acheampong': {'ha': 'right', 'va': 'center', 'dx': -0.08, 'dy': 0},
    'Pedro Neto': {'ha': 'left', 'va': 'center', 'dx': 0.08, 'dy': 0},
    'Jorrel Hato': {'ha': 'left', 'va': 'bottom', 'dx': 0.07, 'dy': 1.2},
    'Roméo Lavia': {'ha': 'left', 'va': 'center', 'dx': 0.08, 'dy': 0.8},
    'Wesley Fofana': {'ha': 'right', 'va': 'center', 'dx': -0.08, 'dy': -0.6},
    'Malo Gusto': {'ha': 'left', 'va': 'center', 'dx': 0.08, 'dy': -0.5},
    'Morgan Rogers': {'ha': 'left', 'va': 'bottom', 'dx': 0.07, 'dy': 1.2},
    'Cole Palmer': {'ha': 'right', 'va': 'top', 'dx': -0.07, 'dy': -1.2},
    'Maxence Lacroix': {'ha': 'left', 'va': 'center', 'dx': 0.08, 'dy': 0},
    'Pep Chavarría': {'ha': 'left', 'va': 'top', 'dx': 0.08, 'dy': -1.2},
    'Reece James': {'ha': 'left', 'va': 'center', 'dx': 0.08, 'dy': 0},
    'Levi Colwill': {'ha': 'left', 'va': 'center', 'dx': 0.08, 'dy': 0},
    'Jordan Henderson': {'ha': 'right', 'va': 'center', 'dx': -0.08, 'dy': 0},
    'João Pedro': {'ha': 'left', 'va': 'center', 'dx': 0.08, 'dy': 0},
}

for _, row in df.iterrows():
    name = row['Player']
    x_val = row['TKLA_per90']
    y_val = row['TKL_pct']
    zone = row['Macro_Zone']
    
    cfg = label_configs.get(name, {'ha': 'left', 'va': 'center', 'dx': 0.07, 'dy': 0})
    
    is_hero = 'Wide CB' in zone
    font_weight = 'bold' if is_hero else 'normal'
    name_color = '#ffffff' if is_hero else text_main
    
    short_name = name.split()[-1]
    if name == 'Josh Acheampong':
        short_name = 'Acheampong'
    elif name == 'Pep Chavarría':
        short_name = 'Chavarría'
    elif name == 'João Pedro':
        short_name = 'João Pedro'
        
    label_text = f"{short_name} ({y_val:.0f}%)" if is_hero else f"{short_name}"
    
    ax.annotate(
        label_text,
        xy=(x_val, y_val),
        xytext=(x_val + cfg['dx'], y_val + cfg['dy']),
        ha=cfg['ha'], va=cfg['va'],
        fontsize=9.5, fontweight=font_weight,
        color=name_color,
        zorder=5
    )

ax.set_xlim(0.2, 4.0)
ax.set_ylim(42, 105)

ax.set_xlabel("Tackles Attempted per 90 (Volume)", fontsize=11, fontweight='bold', color=text_sub, labelpad=12)
ax.set_ylabel("Tackle Win % (Efficiency)", fontsize=11, fontweight='bold', color=text_sub, labelpad=12)

ax.tick_params(axis='both', colors=text_sub, labelsize=9.5, length=0, pad=8)

ax.grid(color=grid_color, linestyle='-', linewidth=0.6, alpha=0.7, zorder=0)
ax.set_axisbelow(True)

for s in ['top', 'right']:
    ax.spines[s].set_visible(False)
ax.spines['left'].set_color(grid_color)
ax.spines['bottom'].set_color(grid_color)

fig.text(0.08, 0.94, "CHELSEA FC  ·  DEFENSIVE WORKLOAD & TACKLE EFFICIENCY",
         fontsize=14.5, fontweight='bold', color=text_main, ha='left')
fig.text(0.08, 0.908, "Tackles Attempted per 90 vs. Tackle Win % across Tactical Zones (Wide CBs Highlighted)",
         fontsize=10, color=text_sub, ha='left')

legend = ax.legend(
    loc='upper right', bbox_to_anchor=(0.99, 1.13),
    ncol=3, frameon=False, fontsize=9.2,
    labelcolor=text_main, handletextpad=0.5, columnspacing=1.5
)

fig.text(0.08, 0.02,
         "Data source: step2_squad_defensive_workload_per90.csv | Dashed lines indicate squad medians (1.74 TKLA/90, 75.6% Win Rate)",
         fontsize=8.5, color=text_sub, ha='left')

fig.subplots_adjust(top=0.86, bottom=0.10, left=0.08, right=0.96)

output_path = os.path.join(script_dir, 'wide_cb_defensive_workload.png')
plt.savefig(output_path, dpi=300, facecolor=bg_color, bbox_inches='tight')
print(f"Minimalist plot saved successfully to: {output_path}")

if os.environ.get('DISPLAY') or os.environ.get('MPLBACKEND') != 'Agg':
    try:
        plt.show()
    except Exception:
        pass
