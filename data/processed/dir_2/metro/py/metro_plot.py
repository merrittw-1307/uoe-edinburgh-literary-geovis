import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

fig, ax = plt.subplots(figsize=(16, 10))
ax.set_facecolor('#F0F0F0')
fig.patch.set_facecolor('#F0F0F0')

# 定义线路和站点坐标
lines = {
    'North Line': {
        'color': '#1C7293',
        'stations': [
            ('Leith', 1, 8),
            ('Leith Walk', 3, 8),
            ('Princes Street', 6, 8),
            ('New Town', 9, 8),
        ]
    },
    'Old Town Line': {
        'color': '#B85042',
        'stations': [
            ('Grassmarket', 2, 5),
            ('High Street', 4, 5),
            ('Old Town', 6, 5),
            ('Canongate', 8, 5),
            ('Holyrood', 10, 5),
        ]
    },
    'South Line': {
        'color': '#2C5F2D',
        'stations': [
            ('Morningside', 2, 2),
            ('Bruntsfield', 4, 2),
            ('The Meadows', 6, 2),
            ('South Edinburgh', 9, 2),
        ]
    },
    'East-West Line': {
        'color': '#C9A227',
        'stations': [
            ('Corstorphine', 1, 5),
            ('Murrayfield', 3, 5),
            ('Princes Street', 6, 8),
            ('Calton Hill', 9, 6),
            ("Arthur's Seat", 11, 5),
        ]
    }
}

# 换乘站
interchange = {'Princes Street'}

# 画线路
for line_name, line_data in lines.items():
    color = line_data['color']
    stations = line_data['stations']
    
    # 画线
    xs = [s[1] for s in stations]
    ys = [s[2] for s in stations]
    ax.plot(xs, ys, '-', color=color, linewidth=6, zorder=2, solid_capstyle='round')

# 画站点
all_stations = {}
for line_name, line_data in lines.items():
    color = line_data['color']
    for name, x, y in line_data['stations']:
        if name not in all_stations:
            all_stations[name] = (x, y, color)

for name, (x, y, color) in all_stations.items():
    if name in interchange:
        # 换乘站：白色大圆圈
        ax.scatter(x, y, s=400, color='white', zorder=4, 
                  edgecolors='#333333', linewidth=3)
        ax.scatter(x, y, s=150, color='#333333', zorder=5)
        ax.text(x, y - 0.5, name, ha='center', va='top', 
               fontsize=10, fontweight='bold', color='#333333',
               bbox=dict(boxstyle='round,pad=0.2', facecolor='white', 
                        edgecolor='none', alpha=0.8))
    else:
        # 普通站：白色小圆圈
        ax.scatter(x, y, s=200, color='white', zorder=4,
                  edgecolors=color, linewidth=2.5)
        ax.text(x, y - 0.4, name, ha='center', va='top',
               fontsize=8.5, color='#333333',
               bbox=dict(boxstyle='round,pad=0.2', facecolor='white',
                        edgecolor='none', alpha=0.8))

# 图例
legend_elements = [
    mpatches.Patch(color='#1C7293', label='North Line'),
    mpatches.Patch(color='#B85042', label='Old Town Line'),
    mpatches.Patch(color='#2C5F2D', label='South Line'),
    mpatches.Patch(color='#C9A227', label='East-West Line'),
]
ax.legend(handles=legend_elements, loc='lower right', fontsize=10,
         framealpha=0.9, edgecolor='#CCCCCC')

ax.set_xlim(0, 13)
ax.set_ylim(0, 10)
ax.axis('off')
ax.set_title('Edinburgh Literary Map — Metro Style\nPlace co-occurrence as narrative connections', 
             fontsize=14, fontweight='bold', pad=20)

plt.tight_layout()
plt.savefig('/Users/wangmingyu/Downloads/UoE/Dissertation/data/processed/metro/metro_chart_v1.png',
            dpi=150, bbox_inches='tight')
print("已保存 metro_chart_v1.png")
