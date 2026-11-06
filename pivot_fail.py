import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

script_dir = os.path.dirname(os.path.abspath(__file__))
possible_paths = [
    os.path.join(script_dir, '..', 'step2_pivot_availability_and_logs.csv'),
    os.path.join(script_dir, 'step2_pivot_availability_and_logs.csv'),
    'step2_pivot_availability_and_logs.csv',
    '/Users/rageonfayaa/Desktop/Data analytics /step2_pivot_availability_and_logs.csv'
]

csv_path = None
for path in possible_paths:
    if os.path.exists(path):
        csv_path = path
        break

if not csv_path:
    raise FileNotFoundError("Could not find step2_pivot_availability_and_logs.csv")

df = pd.read_csv(csv_path)
df['Minutes'] = df['Minutes'].fillna(0).astype(int)

matches = [
    {'match': 'Fulham 2-3 Chelsea', 'mw': 'MW 1', 'opp': 'Fulham', 'venue': 'A'},
    {'match': 'Chelsea 4-3 Brighton', 'mw': 'MW 2', 'opp': 'Brighton', 'venue': 'H'},
    {'match': 'Arsenal 2-1 Chelsea', 'mw': 'MW 3', 'opp': 'Arsenal', 'venue': 'A'},
    {'match': 'Chelsea 2-2 Hull City', 'mw': 'MW 4', 'opp': 'Hull City', 'venue': 'H'},
    {'match': 'Brentford 3-0 Chelsea', 'mw': 'MW 5', 'opp': 'Brentford', 'venue': 'A'},
    {'match': 'Chelsea 5-1 Bournemouth', 'mw': 'MW 6', 'opp': 'Bournemouth', 'venue': 'H'},
    {'match': 'Everton 0-2 Chelsea', 'mw': 'MW 7', 'opp': 'Everton', 'venue': 'A'},
]

target_players = [
    'Moisés Caicedo',
    'Roméo Lavia',
    'Jordan Henderson',
    'Valentín Barco'
]

plt.style.use('default')

bg_color = '#0b0f17'
card_bg = '#111827'
text_primary = '#f1f5f9'
text_muted = '#64748b'
border_subtle = '#1e293b'

COLOR_START_FULL = '#1d4ed8'
BORDER_START_FULL = '#3b82f6'

COLOR_START_SUB = '#0284c7'
BORDER_START_SUB = '#38bdf8'

COLOR_SUB_IN = '#b45309'
BORDER_SUB_IN = '#f59e0b'

COLOR_INJURED = '#500724'
BORDER_INJURED = '#e11d48'

COLOR_UNUSED = '#131b2e'
BORDER_UNUSED = '#1e293b'

fig, ax = plt.subplots(figsize=(13.5, 6.2), facecolor=bg_color)
ax.set_facecolor(bg_color)

n_players = len(target_players)
n_matches = len(matches)

ax.set_xlim(-0.5, n_matches - 0.5)
ax.set_ylim(n_players - 0.5, -0.5)

for p_idx, player in enumerate(target_players):
    for m_idx, m_info in enumerate(matches):
        m_name = m_info['match']
        row = df[(df['Match'] == m_name) & (df['Player'] == player)]
        
        if len(row) > 0:
            started = row['Started'].values[0] == 'Yes'
            mins = row['Minutes'].values[0]
            rating = row['Rating'].values[0]
            note = str(row['Note'].values[0]).lower()
        else:
            started = False
            mins = 0
            rating = np.nan
            note = ''
            
        is_injured = ('injured' in note or 'unfit' in note or 'forced off' in note) and ('replaced injured' not in note)
        
        if started:
            if mins >= 85:
                bg, border = COLOR_START_FULL, BORDER_START_FULL
                main_txt = f"{mins}'"
                sub_txt = "90 min"
            else:
                bg, border = COLOR_START_SUB, BORDER_START_SUB
                main_txt = f"{mins}'"
                sub_txt = f"Off {mins}'"
        elif mins > 0:
            bg, border = COLOR_SUB_IN, BORDER_SUB_IN
            main_txt = f"{mins}'"
            sub_txt = f"Sub on"
        elif is_injured:
            bg, border = COLOR_INJURED, BORDER_INJURED
            main_txt = "INJ"
            sub_txt = "Injured"
        else:
            bg, border = COLOR_UNUSED, BORDER_UNUSED
            main_txt = "—"
            sub_txt = "Unused"
            
        tile = mpatches.FancyBboxPatch(
            (m_idx - 0.44, p_idx - 0.40), 0.88, 0.80,
            boxstyle="round,pad=0.02,rounding_size=0.06",
            facecolor=bg, edgecolor=border, linewidth=1.0, zorder=2
        )
        ax.add_patch(tile)
        
        text_color = '#ffffff' if (started or mins > 0 or is_injured) else text_muted
        ax.text(
            m_idx, p_idx - 0.07, main_txt,
            ha='center', va='center', color=text_color,
            fontsize=13, fontweight='bold', zorder=3
        )
        
        if pd.notna(rating) and rating > 0:
            sub_display = f"★ {rating:.1f}"
            sub_color = '#cbd5e1'
        elif is_injured:
            sub_display = sub_txt
            sub_color = '#fda4af'
        else:
            sub_display = sub_txt
            sub_color = '#94a3b8' if (started or mins > 0) else '#475569'
            
        ax.text(
            m_idx, p_idx + 0.18, sub_display,
            ha='center', va='center', color=sub_color,
            fontsize=8.5, zorder=3
        )

x_labels = [f"{m['mw']}\n{m['opp']} ({m['venue']})" for m in matches]
ax.set_xticks(range(n_matches))
ax.set_xticklabels(x_labels, fontsize=10.5, color=text_primary, linespacing=1.35)
ax.xaxis.tick_top()

player_totals = [df[df['Player'] == p]['Minutes'].sum() for p in target_players]
y_labels = [f"{p}\n{tot}' total" for p, tot in zip(target_players, player_totals)]
ax.set_yticks(range(n_players))
ax.set_yticklabels(y_labels, fontsize=11, fontweight='bold', color=text_primary, linespacing=1.3)

ax.tick_params(axis='both', length=0, pad=12)

for spine in ax.spines.values():
    spine.set_visible(False)

fig.text(0.08, 0.94, "CHELSEA FC  ·  MIDFIELD PIVOT AVAILABILITY",
         fontsize=14, fontweight='bold', color=text_primary, ha='left')
fig.text(0.08, 0.90, "Minutes played and match ratings across Matchweeks 1–7",
         fontsize=10, color=text_muted, ha='left')

legend_elements = [
    mpatches.Patch(facecolor=COLOR_START_FULL, edgecolor=BORDER_START_FULL, label='Started (Full 90)'),
    mpatches.Patch(facecolor=COLOR_START_SUB, edgecolor=BORDER_START_SUB, label='Started (Subbed off)'),
    mpatches.Patch(facecolor=COLOR_SUB_IN, edgecolor=BORDER_SUB_IN, label='Subbed on'),
    mpatches.Patch(facecolor=COLOR_INJURED, edgecolor=BORDER_INJURED, label='Injured / Unfit'),
    mpatches.Patch(facecolor=COLOR_UNUSED, edgecolor=BORDER_UNUSED, label='Unused'),
]

legend = ax.legend(
    handles=legend_elements, loc='lower center', bbox_to_anchor=(0.5, -0.16),
    ncol=5, frameon=False, fontsize=9.2, labelcolor=text_muted, handletextpad=0.5, columnspacing=1.8
)

fig.subplots_adjust(top=0.78, bottom=0.14, left=0.16, right=0.96)

output_path = os.path.join(script_dir, 'pivot_availability_heatmap.png')
plt.savefig(output_path, dpi=300, facecolor=bg_color, bbox_inches='tight')
print(f"Minimalist plot saved successfully to: {output_path}")

if os.environ.get('DISPLAY') or os.environ.get('MPLBACKEND') != 'Agg':
    try:
        plt.show()
    except Exception:
        pass
