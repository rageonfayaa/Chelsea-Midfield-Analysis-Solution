import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
from matplotlib.colors import LinearSegmentedColormap

script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.join(script_dir, '..')

radar_path = os.path.join(base_dir, 'step3_all9_players_2526_per90_radar.csv')
pairings_path = os.path.join(base_dir, 'step3_pnc_double_pivot_pairings_matrix.csv')

df_radar = pd.read_csv(radar_path)
df_radar = df_radar.dropna(subset=['Player'])

df_pairings = pd.read_csv(pairings_path)
df_pairings = df_pairings.dropna(subset=['Pivot_Pairing'])

bg_color = '#0b0f17'
card_bg = '#111827'
text_primary = '#f1f5f9'
text_muted = '#64748b'
border_subtle = '#1e293b'

GROUP_COLORS = {
    'Chelsea Core': '#3b82f6',
    'Chelsea Core (Aging)': '#e11d48',
    'Target': '#10b981',
}

BAR_GRAD_TOP = '#6366f1'
BAR_GRAD_BOT = '#1e293b'

fig, (ax_scatter, ax_bars) = plt.subplots(
    1, 2, figsize=(18, 8.5), facecolor=bg_color,
    gridspec_kw={'width_ratios': [1.05, 1], 'wspace': 0.32}
)

ax = ax_scatter
ax.set_facecolor(bg_color)

for _, row in df_radar.iterrows():
    player = row['Player']
    group = row['Group']
    cx = row['Construct_Index']
    dy = row['Destruct_Index']
    dur = row['Durability_Index']

    color = GROUP_COLORS.get(group, '#64748b')

    size = (dur / 100) * 550 + 60

    ax.scatter(cx, dy, s=size * 1.6, color=color, alpha=0.08, zorder=1, edgecolors='none')
    ax.scatter(cx, dy, s=size, color=color, alpha=0.75, edgecolors='white',
               linewidths=0.6, zorder=3)

    offsets = {
        'Moisés Caicedo': (5, 8),
        'Angelo Stiller': (5, -12),
        'Roméo Lavia': (5, 8),
        'Valentín Barco': (-8, -14),
        'Manu Koné': (5, 8),
        'Alex Scott': (5, -12),
        'Chema Andrés': (5, 8),
        'Jack Hinshelwood': (8, 12),
        'Jordan Henderson': (-8, -14),
    }
    dx, dyo = offsets.get(player, (5, -10))

    short = player.split()[-1] if ' ' in player else player
    if player == 'Moisés Caicedo':
        short = 'Caicedo'
    elif player == 'Roméo Lavia':
        short = 'Lavia'
    elif player == 'Valentín Barco':
        short = 'Barco'
    elif player == 'Jordan Henderson':
        short = 'Henderson'
    elif player == 'Jack Hinshelwood':
        short = 'Hinshelwood'

    ax.annotate(
        short,
        (cx, dy), xytext=(dx, dyo), textcoords='offset points',
        fontsize=9.5, fontweight='bold', color=text_primary,
        ha='left', va='center', zorder=5,
        arrowprops=dict(arrowstyle='-', color='#334155', lw=0.5)
    )

cx_med = df_radar['Construct_Index'].median()
dy_med = df_radar['Destruct_Index'].median()
ax.axvline(cx_med, color='#1e293b', ls='--', lw=0.8, zorder=0)
ax.axhline(dy_med, color='#1e293b', ls='--', lw=0.8, zorder=0)

pad = 1.5
ax.text(df_radar['Construct_Index'].max() - pad, df_radar['Destruct_Index'].max() - pad,
        'ELITE ALL-ROUND', fontsize=7.5, color='#334155', ha='right', va='top',
        style='italic', zorder=0)
ax.text(df_radar['Construct_Index'].min() + pad, df_radar['Destruct_Index'].max() - pad,
        'PURE DESTROYER', fontsize=7.5, color='#334155', ha='left', va='top',
        style='italic', zorder=0)
ax.text(df_radar['Construct_Index'].max() - pad, df_radar['Destruct_Index'].min() + pad,
        'PURE CONSTRUCTOR', fontsize=7.5, color='#334155', ha='right', va='bottom',
        style='italic', zorder=0)
ax.text(df_radar['Construct_Index'].min() + pad, df_radar['Destruct_Index'].min() + pad,
        'LIMITED PROFILE', fontsize=7.5, color='#334155', ha='left', va='bottom',
        style='italic', zorder=0)

ax.set_xlabel('Construct Index  →', fontsize=11, color=text_muted, labelpad=10)
ax.set_ylabel('Destruct Index  →', fontsize=11, color=text_muted, labelpad=10)
ax.tick_params(colors=text_muted, labelsize=9)
for spine in ax.spines.values():
    spine.set_color(border_subtle)
    spine.set_linewidth(0.5)
ax.grid(True, color='#1a2233', linewidth=0.3, alpha=0.6)

ax.set_title('A   Construct vs. Destruct Profile', fontsize=13, fontweight='bold',
             color=text_primary, loc='left', pad=14)

legend_handles = [
    Line2D([0], [0], marker='o', color='none', markerfacecolor=c,
           markeredgecolor='white', markeredgewidth=0.5, markersize=9, label=g)
    for g, c in GROUP_COLORS.items()
]
legend_handles.append(
    Line2D([0], [0], marker='o', color='none', markerfacecolor='#475569',
           markeredgecolor='white', markeredgewidth=0.5, markersize=5,
           label='Bubble size = Durability')
)
leg = ax.legend(handles=legend_handles, loc='upper left', frameon=False,
                fontsize=8.5, labelcolor=text_muted, handletextpad=0.6,
                bbox_to_anchor=(0.0, 0.98))

ax2 = ax_bars
ax2.set_facecolor(bg_color)

top10 = df_pairings.nlargest(10, 'Total_Tactical_Fit_Score').iloc[::-1]

y_positions = np.arange(len(top10))
scores = top10['Total_Tactical_Fit_Score'].values
labels = top10['Pivot_Pairing'].values
categories = top10['Pairing_Category'].values

max_score = scores.max()
min_score = scores.min()

cmap = LinearSegmentedColormap.from_list(
    'pivot_fit', ['#1e293b', '#4338ca', '#6366f1', '#818cf8', '#a5b4fc'], N=256
)

for i, (y, score, label, cat) in enumerate(zip(y_positions, scores, labels, categories)):
    norm_val = (score - min_score) / (max_score - min_score) if max_score != min_score else 0.5
    bar_color = cmap(norm_val * 0.75 + 0.25)

    ax2.barh(y, score, height=0.62, color=bar_color, edgecolor='none', zorder=2,
             alpha=0.9, left=0)

    if i >= len(top10) - 3:
        ax2.barh(y, score, height=0.72, color=bar_color, edgecolor='none',
                 zorder=1, alpha=0.12)

    ax2.text(score - 0.8, y, f'{score:.1f}', ha='right', va='center',
             fontsize=10.5, fontweight='bold', color='white', zorder=4)

short_labels = []
for lbl in labels:
    parts = lbl.split(' + ')
    short_parts = []
    for p in parts:
        tokens = p.strip().split()
        short_parts.append(tokens[-1] if len(tokens) > 1 else tokens[0])
    short_labels.append(' + '.join(short_parts))

ax2.set_yticks(y_positions)
ax2.set_yticklabels(short_labels, fontsize=10, fontweight='bold', color=text_primary)

for i in range(len(top10) - 3, len(top10)):
    ax2.get_yticklabels()[i].set_color('#fbbf24')

ax2.set_xlabel('Total Tactical Fit Score  →', fontsize=11, color=text_muted, labelpad=10)
ax2.tick_params(axis='x', colors=text_muted, labelsize=9)
ax2.tick_params(axis='y', length=0, pad=8)

ax2.set_xlim(0, max_score + 5)

for spine in ax2.spines.values():
    spine.set_color(border_subtle)
    spine.set_linewidth(0.5)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.grid(axis='x', color='#1a2233', linewidth=0.3, alpha=0.6)

ax2.set_title('B   Top 10 Double-Pivot Pairings', fontsize=13, fontweight='bold',
              color=text_primary, loc='left', pad=14)

for i in range(len(top10) - 3, len(top10)):
    cat_text = categories[i]
    short_cat = cat_text.replace('Chelsea Core + Target', 'Core + Target') \
                        .replace('Target + Target (New Pivot Pair)', 'New Pair')
    ax2.text(4, y_positions[i] + 0.32, short_cat,
             fontsize=7, color='#64748b', ha='left', va='bottom',
             style='italic', zorder=4)

fig.text(0.06, 0.97, 'PnC DOUBLE-PIVOT SYNERGY MATRIX',
         fontsize=16, fontweight='bold', color=text_primary, ha='left', va='top')
fig.text(0.06, 0.935, 'Construct vs. Destruct scatter & Top 10 tactical pairings  ·  2025-26 Per-90 data',
         fontsize=10, color=text_muted, ha='left', va='top')

fig.text(0.94, 0.02, 'Data: WhoScored / FBref  ·  Chelsea FC Analytics',
         fontsize=7.5, color='#334155', ha='right', va='bottom')

fig.subplots_adjust(top=0.88, bottom=0.10, left=0.06, right=0.97)

output_path = os.path.join(script_dir, 'pnc_double_pivot_synergy.png')
plt.savefig(output_path, dpi=300, facecolor=bg_color, bbox_inches='tight')
print(f"Plot saved to: {output_path}")

try:
    plt.show()
except Exception:
    pass
