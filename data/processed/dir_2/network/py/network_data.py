import pandas as pd
from sqlalchemy import create_engine
from itertools import combinations

engine = create_engine('postgresql://wangmingyu@localhost:5432/litlong_edinburgh')

# 查询5个作者的所有地名提及，按句子分组
query = """
SELECT 
    TRIM(a.forenames) || ' ' || TRIM(a.surname) AS author,
    lm.sentence_id,
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
GROUP BY a.id, a.forenames, a.surname, lm.sentence_id, l.text
"""

df = pd.read_sql(query, engine)
print(f"查到 {len(df)} 条记录")

# 按句子分组，找同一句子里同时出现的地名对
cooccurrence = {}

for sentence_id, group in df.groupby('sentence_id'):
    places = group['place'].unique().tolist()
    if len(places) > 1:
        for p1, p2 in combinations(sorted(places), 2):
            key = (p1, p2)
            cooccurrence[key] = cooccurrence.get(key, 0) + 1

# 转成DataFrame
edges = pd.DataFrame([
    {'source': k[0], 'target': k[1], 'weight': v}
    for k, v in cooccurrence.items()
])

# 只保留共现次数>=2的边，避免图太乱
edges = edges[edges['weight'] >= 2].sort_values('weight', ascending=False)

print(f"共现地名对数量: {len(edges)}")
print("\n共现最强的前10对:")
print(edges.head(10).to_string())

edges.to_csv('/Users/wangmingyu/Downloads/UoE/Dissertation/data/processed/network/network_edges.csv', index=False)
print("\n数据已保存")
