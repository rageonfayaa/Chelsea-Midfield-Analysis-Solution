import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from math import pi

script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, '..', 'step3_all9_players_2526_per90_radar.csv')
df = pd.read_csv(csv_path).dropna(subset=['Player'])

axes_def = [
    ('Acc_Passes_p90',        'Acc. Passes/90'),
    ('Acc_Opp_Half_p90',      'Opp. Half Passes/90'),
    ('Key_Passes_p90',        'Key Passes/90'),
    ('_Ball_Retention_pct',   'Ball Retention %'),
    ('Tkl_Plus_Int_p90',      'Tackles+Int/90'),
    ('Balls_Recovered_p90',   'Balls Recovered/90'),
    ('Ground_Duels_Won_pct',  'Ground Duel %'),
    ('Sprints_p90',           'Sprints/90'),
]

df['_Ball_Retention_pct'] = 100.0 - df['Turnovers_Per_100_Touches']

target_players = [
    'Moisés Caicedo',
    'Jordan Henderson',
    'Angelo Stiller',
    'Chema Andrés',
    'Alex Scott',
]

df_sel = df[df['Player'].isin(target_players)].copy()

col_names = [a[0] for a in axes_def]
axis_labels = [a[1] for a in axes_def]

for col in col_names:
    col_min = df[col].min()
    col_max = df[col].max()
    rng = col_max - col_min if col_max != col_min else 1.0
    df_sel[f'{col}_norm'] = 0.05 + 0.95 * (df_sel[col] - col_min) / rng

norm_cols = [f'{c}_norm' for c in col_names]

bg_color = '#0b0f17'
card_bg = '#111827'
text_primary = '#f1f5f9'
text_muted = '#64748b'
border_subtle = '#1e293b'

PLAYER_STYLES = {
    'Moisés Caicedo':    {'color': '#3b82f6', 'ls': '-',  'lw': 2.4, 'fill_alpha': 0.12, 'label': 'Caicedo', 'zorder': 5},
    'Jordan Henderson':  {'color': '#e11d48', 'ls': '-',  'lw': 2.0, 'fill_alpha': 0.08, 'label': 'Henderson', 'zorder': 4},
    'Angelo Stiller':    {'color': '#10b981', 'ls': '--', 'lw': 2.2, 'fill_alpha': 0.10, 'label': 'Stiller', 'zorder': 6},
    'Chema Andrés':      {'color': '#f59e0b', 'ls': '--', 'lw': 2.0, 'fill_alpha': 0.08, 'label': 'Andrés', 'zorder': 3},
    'Alex Scott':        {'color': '#a78bfa', 'ls': '--', 'lw': 2.0, 'fill_alpha': 0.08, 'label': 'Scott', 'zorder': 3},
}

N = len(axis_labels)
angles = [n / float(N) * 2 * pi for n in range(N)]
angles += angles[:1]

fig, ax = plt.subplots(figsize=(9.5, 9.5), subplot_kw=dict(polar=True), facecolor=bg_color)
ax.set_facecolor(bg_color)

ax.set_theta_offset(pi / 2)
ax.set_theta_direction(-1)

ax.set_xticks(angles[:-1])
ax.set_xticklabels(axis_labels, fontsize=10, fontweight='bold', color=text_primary)

ax.set_rlabel_position(30)
ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
ax.set_yticklabels(['20', '40', '60', '80', '100'], fontsize=7.5, color='#334155')
ax.set_ylim(0, 1.08)

ax.xaxis.grid(True, color='#1e293b', linewidth=0.5, alpha=0.7)
ax.yaxis.grid(True, color='#1e293b', linewidth=0.4, alpha=0.5)
ax.spines['polar'].set_color('#1e293b')
ax.spines['polar'].set_linewidth(0.5)

ax.tick_params(axis='x', pad=18)

for player in target_players:
    row = df_sel[df_sel['Player'] == player]
    if row.empty:
        continue

    style = PLAYER_STYLES[player]
    values = row[norm_cols].values.flatten().tolist()
    values += values[:1]

    ax.plot(angles, values, linewidth=style['lw'], linestyle=style['ls'],
            color=style['color'], label=style['label'], zorder=style['zorder'])

    ax.fill(angles, values, color=style['color'], alpha=style['fill_alpha'],
            zorder=style['zorder'] - 1)

    ax.scatter(angles[:-1], values[:-1], s=22, color=style['color'],
               edgecolors='white', linewidths=0.4, zorder=style['zorder'] + 1)

annotation_players = ['Moisés Caicedo', 'Angelo Stiller']
annotation_offsets = {
    'Moisés Caicedo': 0.08,
    'Angelo Stiller': -0.06,
}

for player in annotation_players:
    row = df_sel[df_sel['Player'] == player]
    if row.empty:
        continue
    style = PLAYER_STYLES[player]
    norms = row[norm_cols].values.flatten().tolist()
    raws = row[col_names].values.flatten().tolist()
    offset = annotation_offsets.get(player, 0.06)

    for i, (angle, norm_val, raw_val) in enumerate(zip(angles[:-1], norms, raws)):
        display = f'{raw_val:.1f}' if raw_val != int(raw_val) else f'{int(raw_val)}'
        r_pos = norm_val + offset
        r_pos = max(0.12, min(r_pos, 1.12))

        ax.text(angle, r_pos, display, ha='center', va='center',
                fontsize=7, color=style['color'], fontweight='bold', alpha=0.85,
                zorder=10)

legend = ax.legend(
    loc='lower center',
    bbox_to_anchor=(0.5, -0.12),
    ncol=5, frameon=False,
    fontsize=10, labelcolor=text_primary,
    handletextpad=0.6, columnspacing=1.5
)

for handle in legend.legend_handles:
    handle.set_linewidth(2.5)

fig.text(0.5, 0.97, 'PER-90 RADAR  ·  MIDFIELD PIVOT COMPARISON',
         fontsize=15, fontweight='bold', color=text_primary, ha='center', va='top')
fig.text(0.5, 0.935, 'Chelsea Core (solid) vs. Transfer Targets (dashed)  ·  2025-26 season data',
         fontsize=10, color=text_muted, ha='center', va='top')

fig.text(0.18, 0.90, '● Chelsea Core', fontsize=9, color='#3b82f6',
         fontweight='bold', ha='left', va='top')
fig.text(0.18, 0.875, '● Aging / Outgoing', fontsize=9, color='#e11d48',
         fontweight='bold', ha='left', va='top')
fig.text(0.72, 0.90, '◆ Transfer Targets', fontsize=9, color='#10b981',
         fontweight='bold', ha='left', va='top')

fig.text(0.5, 0.02, 'Data: WhoScored / FBref  ·  Chelsea FC Analytics  ·  Values normalized across all 9 candidates',
         fontsize=7.5, color='#334155', ha='center', va='bottom')

fig.subplots_adjust(top=0.88, bottom=0.10)

output_path = os.path.join(script_dir, 'midfield_pivot_radar.png')
plt.savefig(output_path, dpi=300, facecolor=bg_color, bbox_inches='tight')
print(f"Radar chart saved to: {output_path}")

try:
    plt.show()
except Exception:
    pass

