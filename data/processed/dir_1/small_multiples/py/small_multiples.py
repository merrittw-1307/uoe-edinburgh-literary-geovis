import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sqlalchemy import create_engine

engine = create_engine('postgresql://wangmingyu@localhost:5432/litlong_edinburgh')

query = """
SELECT 
    TRIM(a.forenames) || ' ' || TRIM(a.surname) AS author,
    l.text AS place,
    l.lat,
    l.lon,
    COUNT(lm.id) AS mention_count
FROM api_locationmention lm
JOIN api_location l ON lm.location_id = l.id
JOIN api_document_author da ON lm.document_id = da.document_id
JOIN api_author a ON da.author_id = a.id
WHERE (
    (TRIM(a.forenames) = 'Walter' AND TRIM(a.surname) = 'Scott') OR
    (TRIM(a.forenames) = 'Robert Louis' AND TRIM(a.surname) = 'Stevenson') OR
    (TRIM(a.forenames) = 'Irvine' AND TRIM(a.surname) = 'Welsh') OR
    (TRIM(a.forenames) = 'John Gibson' AND TRIM(a.surname) = 'Lockhart') OR
    (TRIM(a.forenames) = 'Alexander' AND TRIM(a.surname) = 'McCall Smith')
)
AND l.lat IS NOT NULL
AND l.lon IS NOT NULL
GROUP BY a.id, a.forenames, a.surname, l.id, l.text, l.lat, l.lon
"""

df = pd.read_sql(query, engine)

authors = ['Alexander McCall Smith', 'Irvine Welsh', 'John Gibson Lockhart',
           'Robert Louis Stevenson', 'Walter Scott']
colors = ['#B85042', '#1C7293', '#2C5F2D', '#7F77DD', '#C9A227']

fig, axes = plt.subplots(1, 5, figsize=(18, 5))
fig.suptitle('Author Spatial Fingerprints — Small Multiples\n(bubble size = mention frequency)', 
             fontsize=13, fontweight='bold')

for i, (author, color) in enumerate(zip(authors, colors)):
    ax = axes[i]
    data = df[df['author'] == author].copy()
    
    # 取前15个地名
    data = data.nlargest(15, 'mention_count')
    
    # log scale bubble size
    sizes = np.log1p(data['mention_count']) * 20
    
    ax.scatter(data['lon'], data['lat'], 
               s=sizes, 
               color=color, 
               alpha=0.6,
               edgecolors='white',
               linewidth=0.5)
    
    ax.set_title(author.replace(' ', '\n'), fontsize=9, fontweight='bold', color=color)
    ax.set_xlim(-3.35, -3.05)
    ax.set_ylim(55.88, 56.02)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_color('#DDDDDD')

plt.tight_layout()
plt.savefig('/Users/wangmingyu/Downloads/UoE/Dissertation/data/processed/small_multiples.png',
            dpi=150, bbox_inches='tight')
print("已保存 small_multiples.png")
