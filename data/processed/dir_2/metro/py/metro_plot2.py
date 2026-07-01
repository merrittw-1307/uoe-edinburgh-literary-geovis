import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

fig, ax = plt.subplots(figsize=(20, 14))
ax.set_facecolor('#F0F0F0')
fig.patch.set_facecolor('#F0F0F0')

lines = {
    'North Line': {
        'color': '#1C7293',
        'stations': [
            ('Granton', 1, 11),
            ('Newhaven', 3, 11),
            ('Leith', 5, 11),
            ('Leith Walk', 7, 11),
            ('Broughton Street', 9, 11),
            ('Princes Street', 11, 11),
            ('New Town', 13, 11),
            ('Stockbridge', 15, 11),
            ('Comely Bank', 17, 11),
            ('Cramond', 19, 11),
        ]
    },
    'Old Town Line': {
        'color': '#B85042',
        'stations': [
            ('Grassmarket', 3, 7),
            ('Cowgate', 5, 7),
            ('High Street', 7, 7),
            ('Old Town', 9, 7),
            ('Royal Mile', 11, 7),
            ('Canongate', 13, 7),
            ('Holyrood', 15, 7),
            ("Arthur's Seat", 17, 7),
            ('Duddingston', 19, 7),
        ]
    },
    'South Line': {
        'color': '#2C5F2D',
        'stations': [
            ('Colinton', 1, 3),
            ('Morningside', 4, 3),
            ('Bruntsfield', 7, 3),
            ('The Meadows', 9, 3),
            ('Southside', 11, 3),
            ('Newington', 13, 3),
            ('Portobello', 16, 3),
            ('Musselburgh', 19, 3),
        ]
    },
    'East-West Line': {
        'color': '#C9A227',
        'stations': [
            ('Corstorphine', 1, 7),
            ('Murrayfield', 3, 7),
            ('Haymarket', 6, 8),
            ('West End', 8, 9),
            ('Princes Street', 11, 11),
            ('Waverley Station', 11, 9),
            ('Calton Hill', 13, 9),
            ('Abbeyhill', 15, 9),
            ('Jock\'s Lodge', 17, 9),
            ('Portobello', 19, 9),
        ]
    },
    'Circle Line': {
        'color': '#7F77DD',
        'stations': [
            ('Tollcross', 7, 5),
            ('Bruntsfield', 7, 3),
            ('Marchmont', 9, 2),
            ('The Meadows', 11, 3),
            ('Southside', 11, 5),
            ('Old Town', 11, 7),
            ('Waverley Station', 11, 9),
            ('Princes Street', 11, 11),
            ('George Street', 9, 11),
            ('Charlotte Square', 7, 11),
            ('West End', 7, 9),
            ('Tollcross', 7, 5),
        ]
    },
    'North-South Line': {
        'color': '#A26769',
        'stations': [
            ('Leith', 5, 11),
            ('Broughton', 5, 10),
            ('New Town', 5, 9),
            ('Princes Street', 5, 8),
            ('Old Town', 5, 7),
            ('Grassmarket', 5, 6),
            ('Tollcross', 5, 5),
            ('Bruntsfield', 5, 4),
            ('Morningside', 5, 3),
            ('Fairmilehead', 5, 1),
        ]
    },
    'Outer Line': {
        'color': '#4A4A4A',
        'stations': [
            ('Balerno', 1, 1),
            ('Colinton', 3, 2),
            ('Craiglockhart', 5, 2),
            ('Morningside', 7, 3),
            ('Blackford', 9, 2),
            ('Craigmillar', 13, 2),
            ('Niddrie', 15, 2),
            ('Portobello', 17, 3),
            ('Musselburgh', 19, 4),
            ('Prestonpans', 20, 6),
            ('Musselburgh', 19, 8),
        ]
    },
    'West Line': {
        'color': '#FF6B35',
        'stations': [
            ('Cramond', 1, 9),
            ('Corstorphine', 1, 7),
            ('Murrayfield', 3, 7),
            ('Dalry', 5, 7),
            ('Haymarket', 7, 8),
            ('Lothian Road', 9, 9),
            ('Princes Street', 11, 11),
        ]
    }
}

# 换乘站定义
interchange_stations = {
    'Princes Street', 'Old Town', 'Bruntsfield',
    'The Meadows', 'Morningside', 'Portobello',
    'Musselburgh', 'Leith', 'Waverley Station',
    'Grassmarket', 'Tollcross', 'Corstorphine', 'Haymarket'
}

# 画线路
for line_name, line_data in lines.items():
    color = line_data['color']
    stations = line_data['stations']
    xs = [s[1] for s in stations]
    ys = [s[2] for s in stations]
    ax.plot(xs, ys, '-', color=color, linewidth=5,
            zorder=2, solid_capstyle='round', solid_joinstyle='round')

# 收集所有站点
all_stations = {}
for line_name, line_data in lines.items():
    color = line_data['color']
    for name, x, y in line_data['stations']:
        if name not in all_stations:
            all_stations[name] = (x, y, color)

# 画站点
for name, (x, y, color) in all_stations.items():
    if name in interchange_stations:
        ax.scatter(x, y, s=350, color='white', zorder=4,
                  edgecolors='#333333', linewidth=2.5)
        ax.scatter(x, y, s=100, color='#333333', zorder=5)
        ax.text(x, y - 0.45, name, ha='center', va='top',
               fontsize=7.5, fontweight='bold', color='#222222',
               bbox=dict(boxstyle='round,pad=0.15', facecolor='white',
                        edgecolor='none', alpha=0.85))
    else:
        ax.scatter(x, y, s=150, color='white', zorder=4,
                  edgecolors=color, linewidth=2)
        ax.text(x, y - 0.35, name, ha='center', va='top',
               fontsize=7, color='#444444',
               bbox=dict(boxstyle='round,pad=0.1', facecolor='white',
                        edgecolor='none', alpha=0.8))

# 图例
legend_elements = [
    mpatches.Patch(color='#1C7293', label='North Line'),
    mpatches.Patch(color='#B85042', label='Old Town Line'),
    mpatches.Patch(color='#2C5F2D', label='South Line'),
    mpatches.Patch(color='#C9A227', label='East-West Line'),
    mpatches.Patch(color='#7F77DD', label='Circle Line'),
    mpatches.Patch(color='#A26769', label='North-South Line'),
    mpatches.Patch(color='#4A4A4A', label='Outer Line'),
    mpatches.Patch(color='#FF6B35', label='West Line'),
]
ax.legend(handles=legend_elements, loc='lower right',
         fontsize=9, framealpha=0.9, edgecolor='#CCCCCC')

ax.set_xlim(0, 21)
ax.set_ylim(0, 13)
ax.axis('off')
ax.set_title('Edinburgh Literary Map — Metro Style\nPlace names in literature as narrative network',
             fontsize=15, fontweight='bold', pad=20)

plt.tight_layout()
plt.savefig('/Users/wangmingyu/Downloads/UoE/Dissertation/data/processed/metro/metro_chart_v2.png',
            dpi=150, bbox_inches='tight')
print("已保存 metro_chart_v2.png")
