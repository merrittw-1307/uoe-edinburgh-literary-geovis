import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

edges = pd.read_csv('/Users/wangmingyu/Downloads/UoE/Dissertation/data/processed/network/network_edges.csv')
nodes = pd.read_csv('/Users/wangmingyu/Downloads/UoE/Dissertation/data/processed/network/network_nodes.csv')

# 只取权重>=8的强连接，减少密度
edges_strong = edges[edges['weight'] >= 8].copy()
print(f"强连接数量: {len(edges_strong)}")
print(edges_strong.to_string())

G = nx.Graph()
for _, row in edges_strong.iterrows():
    G.add_edge(row['source'], row['target'], weight=row['weight'])

node_mentions = nodes.set_index('place')['total_mentions'].to_dict()
node_sizes = [np.log1p(node_mentions.get(n, 1)) * 100 for n in G.nodes()]

# 三次方缩放，让强弱差异极其明显
edge_weights = [(G[u][v]['weight'] / edges_strong['weight'].max()) ** 2 * 12 
                for u, v in G.edges()]

pos = nx.spring_layout(G, seed=42, k=3.5)

fig, ax = plt.subplots(figsize=(14, 10))
ax.set_facecolor('#F8F9FC')
fig.patch.set_facecolor('#F8F9FC')

nx.draw_networkx_edges(G, pos,
                        width=edge_weights,
                        edge_color='#A26769',
                        alpha=0.6,
                        ax=ax)

nx.draw_networkx_nodes(G, pos,
                        node_size=node_sizes,
                        node_color='#21295C',
                        alpha=0.85,
                        ax=ax)

nx.draw_networkx_labels(G, pos,
                         font_size=9,
                         font_color='white',
                         font_weight='bold',
                         ax=ax)

ax.set_title('Narrative Topology Network\nStrong place co-occurrence (weight ≥ 8)',
             fontsize=13, fontweight='bold', pad=20)
ax.axis('off')

plt.tight_layout()
plt.savefig('/Users/wangmingyu/Downloads/UoE/Dissertation/data/processed/network/network_chart.png',
            dpi=150, bbox_inches='tight')
print("已保存 network_chart.png")
