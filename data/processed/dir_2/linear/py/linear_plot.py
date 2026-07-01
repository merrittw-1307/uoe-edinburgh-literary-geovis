import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

edges = pd.read_csv('/Users/wangmingyu/Downloads/UoE/Dissertation/data/processed/network/network_edges.csv')
nodes = pd.read_csv('/Users/wangmingyu/Downloads/UoE/Dissertation/data/processed/network/network_nodes.csv')

# 只取强连接
edges_strong = edges[edges['weight'] >= 6].copy()

# 取出现在强连接里的节点
active_nodes = set(edges_strong['source'].tolist() + edges_strong['target'].tolist())
nodes_filtered = nodes[nodes['place'].isin(active_nodes)].copy()

# 按提及次数排序，从左到右排列
nodes_filtered = nodes_filtered.sort_values('total_mentions', ascending=False).reset_index(drop=True)
place_order = nodes_filtered['place'].tolist()
x_positions = {place: i for i, place in enumerate(place_order)}
n = len(place_order)

fig, ax = plt.subplots(figsize=(18, 8))
ax.set_facecolor('#F8F9FC')
fig.patch.set_facecolor('#F8F9FC')

# 画弧线
for _, row in edges_strong.iterrows():
    if row['source'] in x_positions and row['target'] in x_positions:
        x1 = x_positions[row['source']]
        x2 = x_positions[row['target']]
        weight = row['weight']
        mid_x = (x1 + x2) / 2
        height = abs(x2 - x1) * 0.4

        # 贝塞尔曲线
        t = np.linspace(0, 1, 100)
        bx = (1-t)**2 * x1 + 2*(1-t)*t * mid_x + t**2 * x2
        by = 2*(1-t)*t * height

        lw = (weight / edges_strong['weight'].max()) ** 2 * 6
        alpha = min(weight / edges_strong['weight'].max() * 0.9, 0.85)
        ax.plot(bx, by, color='#21295C', linewidth=lw, alpha=alpha)

# 画节点
for place, x in x_positions.items():
    mentions = nodes_filtered[nodes_filtered['place'] == place]['total_mentions'].values
    size = np.log1p(mentions[0]) * 4 if len(mentions) > 0 else 5
    ax.scatter(x, 0, s=size**2, color='#B85042', zorder=5, alpha=0.9)
    ax.text(x, -0.08, place, rotation=45, ha='right', fontsize=8, color='#2C2C2A')

ax.set_xlim(-0.5, n - 0.5)
ax.set_ylim(-1.5, max(abs(x2-x1)*0.4 for _, row in edges_strong.iterrows()
                       if row['source'] in x_positions and row['target'] in x_positions
                       for x1, x2 in [(x_positions[row['source']], x_positions[row['target']])]) + 0.5)
ax.axhline(y=0, color='#CCCCCC', linewidth=1.5, zorder=1)
ax.axis('off')
ax.set_title('Narrative Topology — Linear Connection Diagram\nPlace co-occurrence (weight ≥ 6), node size = mention frequency',
             fontsize=13, fontweight='bold')

plt.tight_layout()
plt.savefig('/Users/wangmingyu/Downloads/UoE/Dissertation/data/processed/linear/linear_chart_v1.png',
            dpi=150, bbox_inches='tight')
print("已保存 linear_chart_v1.png")
