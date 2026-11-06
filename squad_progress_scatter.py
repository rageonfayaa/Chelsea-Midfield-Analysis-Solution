import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

script_dir = os.path.dirname(os.path.abspath(__file__))
possible_paths = [
    os.path.join(script_dir, '..', 'step1_chelsea_squad_progression_per90.csv'),
    os.path.join(script_dir, 'step1_chelsea_squad_progression_per90.csv'),
    'step1_chelsea_squad_progression_per90.csv',
    '/Users/rageonfayaa/Desktop/Data analytics /step1_chelsea_squad_progression_per90.csv'
]

csv_path = None
for path in possible_paths:
    if os.path.exists(path):
        csv_path = path
        break

if not csv_path:
    raise FileNotFoundError("Could not find step1_chelsea_squad_progression_per90.csv")

df = pd.read_csv(csv_path)

def get_category(pos_str):
    pos = str(pos_str).lower()
    if 'striker' in pos or 'winger' in pos or 'attacking mid' in pos:
        return 'Attacker / Winger'
    elif 'pivot' in pos or 'central midfield' in pos:
        return 'Midfielder / Pivot'
    elif 'wing-back' in pos or 'lwb' in pos or 'rwb' in pos:
        return 'Wing-Back'
    elif 'center-back' in pos or 'cb' in pos:
        return 'Center-Back'
    return 'Other'

df['Category'] = df['Position_Group'].apply(get_category)

category_colors = {
    'Midfielder / Pivot': '#38bdf8',
    'Center-Back': '#a78bfa',
    'Wing-Back': '#34d399',
    'Attacker / Winger': '#fb923c'
}

plt.style.use('default')

bg_color = '#0e1626'
card_color = '#152036'
text_main = '#f8fafc'
text_sub = '#94a3b8'
grid_color = '#22304a'

fig, ax = plt.subplots(figsize=(13, 8.5), facecolor=bg_color)
ax.set_facecolor(card_color)

min_size, max_size = 180, 850
sizes = np.interp(df['PASS_per90'], (df['PASS_per90'].min(), df['PASS_per90'].max()), (min_size, max_size))
df['bubble_size'] = sizes

mean_x = df['PPAS_per90'].mean()
mean_y = df['PCRY_per90'].mean()

ax.axvline(mean_x, color='#475569', linestyle='--', linewidth=1.1, alpha=0.75, zorder=1)
ax.axhline(mean_y, color='#475569', linestyle='--', linewidth=1.1, alpha=0.75, zorder=1)

ax.text(4.45, 2.45, "DUAL PROGRESSORS\n(High Pass & Carry)",
        fontsize=8.5, color='#64748b', ha='right', va='top', fontweight='bold', alpha=0.55)
ax.text(4.45, 1.25, "PASSING HUBS\n(High Pass / Low Carry)",
        fontsize=8.5, color='#64748b', ha='right', va='bottom', fontweight='bold', alpha=0.55)
ax.text(0.72, 1.65, "BALL CARRIERS\n(High Carry / Low Pass)",
        fontsize=8.5, color='#64748b', ha='left', va='top', fontweight='bold', alpha=0.55)
ax.text(0.72, 0.38, "DEEP CIRCULATION\n(Low Direct Progression)",
        fontsize=8.5, color='#64748b', ha='left', va='bottom', fontweight='bold', alpha=0.55)

for cat, color in category_colors.items():
    sub = df[df['Category'] == cat]
    ax.scatter(
        sub['PPAS_per90'],
        sub['PCRY_per90'],
        s=sub['bubble_size'],
        c=color,
        label=cat,
        alpha=0.88,
        edgecolors='#ffffff',
        linewidth=1.2,
        zorder=3
    )

hendo = df[df['Player'] == 'Jordan Henderson'].iloc[0]
ax.scatter(
    hendo['PPAS_per90'],
    hendo['PCRY_per90'],
    s=hendo['bubble_size'] + 150,
    facecolors='none',
    edgecolors='#00f2fe',
    linewidth=2.5,
    linestyle='-',
    zorder=4,
    label='Jordan Henderson (Focus)'
)

offsets = {
    'Jordan Henderson': (-38, 26),
    'Reece James': (18, 0),
    'Pep Chavarría': (16, 2),
    'Levi Colwill': (18, -8),
    'Wesley Fofana': (18, 0),
    'Maxence Lacroix': (-24, -20),
    'Malo Gusto': (16, 2),
    'Josh Acheampong': (16, -14),
    'Roméo Lavia': (-20, -18),
    'Pedro Neto': (16, 2),
    'Cole Palmer': (16, 2),
    'Morgan Rogers': (16, 2),
    'Jorrel Hato': (16, -6),
    'João Pedro': (16, 2),
}

for _, row in df.iterrows():
    name = row['Player']
    x_val = row['PPAS_per90']
    y_val = row['PCRY_per90']
    vol = row['PASS_per90']

    offset = offsets.get(name, (12, 4))
    is_hendo = (name == 'Jordan Henderson')

    label_text = f"{name}\n({vol:.1f} p/90)" if is_hendo else name
    label_color = '#38bdf8' if is_hendo else text_main
    font_weight = 'bold' if is_hendo else 'normal'

    ax.annotate(
        label_text,
        xy=(x_val, y_val),
        xytext=offset,
        textcoords='offset points',
        fontsize=9.5 if not is_hendo else 10.5,
        fontweight=font_weight,
        color=label_color,
        zorder=5,
        arrowprops=dict(
            arrowstyle='-',
            color='#64748b',
            lw=0.7,
            alpha=0.65
        ) if abs(offset[0]) > 14 or abs(offset[1]) > 14 else None
    )

ax.set_xlabel("Progressive Passes per 90 (PPAS_per90)", fontsize=11.5, fontweight='bold', color=text_main, labelpad=10)
ax.set_ylabel("Progressive Carries per 90 (PCRY_per90)", fontsize=11.5, fontweight='bold', color=text_main, labelpad=10)

ax.set_xlim(0.65, 4.65)
ax.set_ylim(0.32, 2.55)

ax.tick_params(colors=text_sub, labelsize=10)
ax.grid(True, color=grid_color, linestyle='--', linewidth=0.7, alpha=0.7, zorder=0)

for spine in ['top', 'right']:
    ax.spines[spine].set_visible(False)
for spine in ['left', 'bottom']:
    ax.spines[spine].set_color(grid_color)
    ax.spines[spine].set_linewidth(1.1)

fig.suptitle("CHELSEA FC : SQUAD BALL PROGRESSION & VOLUME PER 90",
             fontsize=17, fontweight='bold', color=text_main, x=0.08, y=0.97, ha='left')

plt.title("Progressive Passes vs. Progressive Carries per 90 (N=14) | Bubble size indicates Pass Volume (PASS_per90)",
          fontsize=11, color=text_sub, pad=16, loc='left')

leg1 = ax.legend(
    loc='upper left',
    frameon=True,
    facecolor=bg_color,
    edgecolor=grid_color,
    fontsize=9.5,
    labelcolor=text_main,
    title="Position Role",
    title_fontsize='10',
    framealpha=0.92
)
leg1.get_title().set_color(text_main)
leg1.get_title().set_fontweight('bold')
ax.add_artist(leg1)

size_samples = [20, 40, 65]
legend_handles = []
for val in size_samples:
    s = np.interp(val, (df['PASS_per90'].min(), df['PASS_per90'].max()), (min_size, max_size))
    legend_handles.append(
        plt.scatter([], [], s=s, color='none', edgecolors=text_sub, linewidth=1.2, label=f"{val} passes/90")
    )

leg2 = ax.legend(
    handles=legend_handles,
    loc='lower right',
    frameon=True,
    facecolor=bg_color,
    edgecolor=grid_color,
    fontsize=9,
    labelcolor=text_sub,
    title="Pass Volume Scale",
    title_fontsize='9.5',
    framealpha=0.92,
    scatterpoints=1
)
leg2.get_title().set_color(text_main)
leg2.get_title().set_fontweight('bold')

fig.text(0.08, 0.02,
         f"Data source: step1_chelsea_squad_progression_per90.csv | Dashed lines indicate squad means ({mean_x:.2f} PPAS/90, {mean_y:.2f} PCRY/90)",
         fontsize=8.5, color=text_sub, ha='left')

plt.tight_layout(rect=[0, 0.03, 1, 0.94])

output_path = os.path.join(script_dir, 'squad_progress_scatter.png')
plt.savefig(output_path, dpi=300, facecolor=fig.get_facecolor(), bbox_inches='tight')
print(f"Scatter plot saved successfully to: {output_path}")

plt.show()
