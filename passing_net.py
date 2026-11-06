import os
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mplsoccer import VerticalPitch

script_dir = os.path.dirname(os.path.abspath(__file__))
possible_dirs = [
    os.path.join(script_dir, '..'),
    script_dir,
    '.',
    '/Users/rageonfayaa/Desktop/Data analytics '
]

nodes_file = None
edges_file = None

for d in possible_dirs:
    n_path = os.path.join(d, 'step1_passing_network_nodes.csv')
    e_path = os.path.join(d, 'step1_passing_network_edges.csv')
    if os.path.exists(n_path) and os.path.exists(e_path):
        nodes_file = n_path
        edges_file = e_path
        break

if not nodes_file or not edges_file:
    raise FileNotFoundError("Could not find step1_passing_network_nodes.csv or step1_passing_network_edges.csv")

df_nodes = pd.read_csv(nodes_file)
df_edges = pd.read_csv(edges_file)

def get_short_name(name):
    parts = str(name).strip().split()
    if len(parts) >= 2:
        return parts[-1]
    return name

df_nodes['short_name'] = df_nodes['Player'].apply(get_short_name)

df_nodes['y_plot'] = 100 - df_nodes['y']

match_with = "Brentford 3-0 Chelsea"
match_without = "Chelsea 2-2 Hull City"

nodes_with = df_nodes[df_nodes['Match'] == match_with].copy()
edges_with = df_edges[df_edges['Match'] == match_with].copy()

nodes_without = df_nodes[df_nodes['Match'] == match_without].copy()
edges_without = df_edges[df_edges['Match'] == match_without].copy()

def draw_shrunk_pass_line(pitch, ax, x_start, y_start, x_end, y_end, pass_count,
                          color='#38bdf8', min_count=6, max_count=18):
    """
    Draws a pass line trimmed at both player circle boundaries.
    Line thickness and opacity scale with pass count.
    """
    dx = x_end - x_start
    dy = y_end - y_start
    dist = math.hypot(dx, dy)
    shrink = 3.8

    if dist > 2 * shrink:
        angle = math.atan2(dy, dx)
        x1 = x_start + shrink * math.cos(angle)
        y1 = y_start + shrink * math.sin(angle)
        x2 = x_end - shrink * math.cos(angle)
        y2 = y_end - shrink * math.sin(angle)
    else:
        x1, y1 = x_start, y_start
        x2, y2 = x_end, y_end

    lw = np.interp(pass_count, [min_count, max_count], [1.8, 5.8])
    alpha = np.interp(pass_count, [min_count, max_count], [0.55, 0.92])

    pitch.lines(x1, y1, x2, y2, lw=lw, color=color, alpha=alpha, zorder=2, ax=ax)

    if pass_count >= 11:
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2
        ax.annotate(str(pass_count), xy=(mid_y, mid_x),
                    fontsize=8, fontweight='bold', color='#ffffff',
                    ha='center', va='center', zorder=3,
                    bbox=dict(boxstyle="round,pad=0.22", facecolor='#0e1626',
                              edgecolor=color, alpha=0.9, lw=0.8))

plt.style.use('default')

bg_color = '#0e1626'
pitch_color = '#152036'
line_color = '#2d3d5a'
text_main = '#f8fafc'
text_sub = '#94a3b8'

pitch = VerticalPitch(
    pitch_type='custom',
    pitch_length=100,
    pitch_width=100,
    pitch_color=pitch_color,
    line_color=line_color,
    linewidth=1.2,
    goal_type='box',
    line_zorder=1
)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 11), facecolor=bg_color)
pitch.draw(ax=ax1)
pitch.draw(ax=ax2)

node_lookup_with = nodes_with.set_index('Player')

for _, row in edges_with.iterrows():
    p_from = row['From_Player']
    p_to = row['To_Player']
    cnt = row['Pass_Count_Est']

    if p_from in node_lookup_with.index and p_to in node_lookup_with.index:
        x_start = node_lookup_with.loc[p_from, 'x']
        y_start = node_lookup_with.loc[p_from, 'y_plot']
        x_end = node_lookup_with.loc[p_to, 'x']
        y_end = node_lookup_with.loc[p_to, 'y_plot']

        is_hendo_link = (p_from == 'Jordan Henderson' or p_to == 'Jordan Henderson')
        link_col = '#38bdf8' if is_hendo_link else '#0284c7'
        draw_shrunk_pass_line(pitch, ax1, x_start, y_start, x_end, y_end, cnt, color=link_col)

for _, row in nodes_with.iterrows():
    p_name = row['Player']
    p_num = row['Number']
    short_n = row['short_name']
    touches = row['Touches']
    x_pos = row['x']
    y_pos = row['y_plot']

    node_size = np.interp(touches, [15, 80], [280, 850])
    is_hendo = (p_name == 'Jordan Henderson')

    node_color = '#00f2fe' if is_hendo else '#1e40af'
    edge_color = '#ffffff' if is_hendo else '#60a5fa'
    lw = 2.4 if is_hendo else 1.5

    if is_hendo:
        pitch.scatter(x_pos, y_pos, s=node_size + 200, facecolors='none',
                      edgecolors='#00f2fe', linewidth=2.2, linestyle='--', ax=ax1, zorder=3)

    pitch.scatter(x_pos, y_pos, s=node_size, color=node_color,
                  edgecolors=edge_color, linewidth=lw, alpha=0.95, ax=ax1, zorder=4)

    num_col = '#0e1626' if is_hendo else '#ffffff'
    pitch.annotate(str(p_num), xy=(x_pos, y_pos), ax=ax1,
                   ha='center', va='center', fontsize=9.5, fontweight='bold',
                   color=num_col, zorder=5)

    name_offset = 3.6 if x_pos < 20 else -3.8
    label_txt = f"{short_n} ({touches})" if is_hendo else short_n
    label_col = '#38bdf8' if is_hendo else text_main

    pitch.annotate(label_txt, xy=(x_pos + name_offset, y_pos), ax=ax1,
                   ha='center', va='center', fontsize=8.5,
                   fontweight='bold' if is_hendo else 'normal',
                   color=label_col, zorder=5)

node_lookup_without = nodes_without.set_index('Player')

for _, row in edges_without.iterrows():
    p_from = row['From_Player']
    p_to = row['To_Player']
    cnt = row['Pass_Count_Est']

    if p_from in node_lookup_without.index and p_to in node_lookup_without.index:
        x_start = node_lookup_without.loc[p_from, 'x']
        y_start = node_lookup_without.loc[p_from, 'y_plot']
        x_end = node_lookup_without.loc[p_to, 'x']
        y_end = node_lookup_without.loc[p_to, 'y_plot']

        is_flank_link = ('Gusto' in p_from or 'Gusto' in p_to or 'Neto' in p_to)
        link_col = '#f43f5e' if is_flank_link else '#fb7185'
        draw_shrunk_pass_line(pitch, ax2, x_start, y_start, x_end, y_end, cnt, color=link_col)

for _, row in nodes_without.iterrows():
    p_name = row['Player']
    p_num = row['Number']
    short_n = row['short_name']
    touches = row['Touches']
    x_pos = row['x']
    y_pos = row['y_plot']

    node_size = np.interp(touches, [15, 80], [280, 850])
    is_pivot = (p_name in ['Roméo Lavia', 'Reece James'])

    node_color = '#e11d48' if is_pivot else '#9f1239'
    edge_color = '#fda4af' if is_pivot else '#f43f5e'
    lw = 2.0 if is_pivot else 1.5

    pitch.scatter(x_pos, y_pos, s=node_size, color=node_color,
                  edgecolors=edge_color, linewidth=lw, alpha=0.95, ax=ax2, zorder=4)

    pitch.annotate(str(p_num), xy=(x_pos, y_pos), ax=ax2,
                   ha='center', va='center', fontsize=9.5, fontweight='bold',
                   color='#ffffff', zorder=5)

    name_offset = 3.6 if x_pos < 20 else -3.8
    pitch.annotate(short_n, xy=(x_pos + name_offset, y_pos), ax=ax2,
                   ha='center', va='center', fontsize=8.5,
                   fontweight='bold' if is_pivot else 'normal',
                   color='#fda4af' if is_pivot else text_main, zorder=5)

fig.suptitle("CHELSEA FC : PASSING NETWORK COMPARISON",
             fontsize=19, fontweight='bold', color=text_main, x=0.5, y=0.98, ha='center')

ax1.set_title("Brentford 3–0 Chelsea  (Away | 2026-09-19)\n"
              "WITH HENDERSON  •  Formation: 3-4-2-1\n"
              "Central Pivot Distribution (Henderson: 65 Touches, 4 Key Hub Connections)",
              fontsize=11.5, fontweight='bold', color='#38bdf8', pad=15, linespacing=1.4)

ax2.set_title("Chelsea 2–2 Hull City  (Home | 2026-09-12)\n"
              "WITHOUT HENDERSON  •  Formation: 4-2-3-1\n"
              "Right-Flank Overload (Lavia + James Pivot | Fofana–Gusto–Neto Axis)",
              fontsize=11.5, fontweight='bold', color='#fb7185', pad=15, linespacing=1.4)

fig.text(0.5, 0.02,
         "Data source: step1_passing_network_nodes.csv & step1_passing_network_edges.csv\n"
         "Circle size = Player touches | Line thickness = Pass volume between players | Badge on line = Pass count (≥11)",
         fontsize=9, color=text_sub, ha='center', linespacing=1.3)

plt.tight_layout(rect=[0.02, 0.04, 0.98, 0.95])

output_path = os.path.join(script_dir, 'passing_network_comparison.png')
plt.savefig(output_path, dpi=300, facecolor=bg_color, bbox_inches='tight')
print(f"Passing network saved successfully to: {output_path}")

plt.show()
