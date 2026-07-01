import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('/Users/wangmingyu/Downloads/UoE/Dissertation/data/processed/barcode_data.csv', index_col=0)

authors = list(df.index)
places = list(df.columns)
n_places = len(places)

colors = ['#B85042', '#1C7293', '#2C5F2D', '#7F77DD', '#C9A227']

fig, axes = plt.subplots(len(authors), 1, figsize=(14, 8))
fig.suptitle('Author Spatial Fingerprints — Bar-code Style', fontsize=14, fontweight='bold', y=1.01)

for i, author in enumerate(authors):
    ax = axes[i]
    values = df.loc[author].values
    x = np.arange(n_places)
    ax.bar(x, values, width=0.8, color=colors[i], alpha=0.85)
    ax.set_xlim(-0.5, n_places - 0.5)
    ax.set_ylim(0, df.values.max() * 1.1)
    ax.set_ylabel(author, fontsize=9, rotation=0, ha='right', va='center')
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

# 只在最后一行显示地名
axes[-1].set_xticks(np.arange(n_places))
axes[-1].set_xticklabels(places, rotation=45, ha='right', fontsize=7)

plt.tight_layout()
plt.savefig('/Users/wangmingyu/Downloads/UoE/Dissertation/data/processed/barcode_chart.png',
            dpi=150, bbox_inches='tight')
print("图已保存到 processed/barcode_chart.png")
plt.show()
