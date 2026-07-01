import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

edges = pd.read_csv('/Users/wangmingyu/Downloads/UoE/Dissertation/data/processed/network/network_edges.csv')
nodes = pd.read_csv('/Users/wangmingyu/Downloads/UoE/Dissertation/data/processed/network/network_nodes.csv')

edges_top = edges.head(50)

G = nx.Graph()
for _, row in edges_top.iterrows():
    G.add_edge(row['source'], row['target'], weight=row['weight'])

node_mentions = nodes.set_index('place')['total_mentions'].to_dict()
node_sizes = [np.log1p(node_mentions.get(n, 1)) * 80 for n in G.nodes()]

# 平方根缩放，差异更明显
edge_weights = [np.sqrt(G[u][v]['weight']) * 1.5 for u, v in G.edges()]

pos = nx.spring_layout(G, seed=42, k=2)

fig, ax = plt.subplots(figsize=(14, 10))
ax.set_facecolor('#F8F9FC')
fig.patch.set_facecolor('#F8F9FC')

nx.draw_networkx_edges(G, pos,
                        width=edge_weights,
                        edge_color='#A26769',
                        alpha=0.5,
                        ax=ax)

nx.draw_networkx_nodes(G, pos,
                        node_size=node_sizes,
                        node_color='#21295C',
                        alpha=0.85,
                        ax=ax)

nx.draw_networkx_labels(G, pos,
                         font_size=8,
                         font_color='white',
                         font_weight='bold',
                         ax=ax)

ax.set_title('Narrative Topology Network\nPlace co-occurrence across literary works (top 50 connections)',
             fontsize=13, fontweight='bold', pad=20)
ax.axis('off')

plt.tight_layout()
plt.savefig('/Users/wangmingyu/Downloads/UoE/Dissertation/data/processed/network/network_chart.png',
            dpi=150, bbox_inches='tight')
print("已保存 network_chart.png")
