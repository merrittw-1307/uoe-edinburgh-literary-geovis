import pandas as pd
from sqlalchemy import create_engine
from itertools import combinations

engine = create_engine('postgresql://wangmingyu@localhost:5432/litlong_edinburgh')

query = """
SELECT 
    TRIM(a.forenames) || ' ' || TRIM(a.surname) AS author,
    lm.document_id,
    l.text AS place,
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
GROUP BY a.id, a.forenames, a.surname, lm.document_id, l.text
"""

df = pd.read_sql(query, engine)
print(f"查到 {len(df)} 条记录")

# 每个作者只取前15个最常见地名
top_places_per_author = (
    df.groupby(['author', 'place'])['mention_count']
    .sum()
    .reset_index()
    .sort_values('mention_count', ascending=False)
    .groupby('author')
    .head(15)
)

# 过滤只保留这些地名
df_filtered = df.merge(
    top_places_per_author[['author', 'place']], 
    on=['author', 'place']
)

# 按document计算地名共现
cooccurrence = {}
for doc_id, group in df_filtered.groupby('document_id'):
    places = group['place'].unique().tolist()
    if len(places) > 1:
        for p1, p2 in combinations(sorted(places), 2):
            key = (p1, p2)
            cooccurrence[key] = cooccurrence.get(key, 0) + 1

edges = pd.DataFrame([
    {'source': k[0], 'target': k[1], 'weight': v}
    for k, v in cooccurrence.items()
])

edges = edges[edges['weight'] >= 2].sort_values('weight', ascending=False)
print(f"\n共现地名对数量: {len(edges)}")
print("\n共现最强的前10对:")
print(edges.head(10).to_string())

edges.to_csv('/Users/wangmingyu/Downloads/UoE/Dissertation/data/processed/network/network_edges.csv', index=False)

# 节点信息
nodes = pd.DataFrame({
    'place': df_filtered.groupby('place')['mention_count'].sum().index,
    'total_mentions': df_filtered.groupby('place')['mention_count'].sum().values
})
nodes.to_csv('/Users/wangmingyu/Downloads/UoE/Dissertation/data/processed/network/network_nodes.csv', index=False)
print("\n数据已保存")
