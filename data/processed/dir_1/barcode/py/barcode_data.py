import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('postgresql://wangmingyu@localhost:5432/litlong_edinburgh')

query = """
SELECT 
    TRIM(a.forenames) || ' ' || TRIM(a.surname) AS author,
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
GROUP BY a.id, a.forenames, a.surname, l.text
ORDER BY mention_count DESC
"""

df = pd.read_sql(query, engine)

top_places = df.groupby('place')['mention_count'].sum().nlargest(30).index.tolist()
df_filtered = df[df['place'].isin(top_places)]

pivot = df_filtered.pivot_table(index='author', columns='place', values='mention_count', fill_value=0)
pivot_norm = pivot.div(pivot.sum(axis=1), axis=0)

pivot_norm.to_csv('/Users/wangmingyu/Downloads/UoE/Dissertation/data/processed/barcode_data.csv')
print(f"地名数量: {len(pivot_norm.columns)}")
print(f"作者数量: {len(pivot_norm.index)}")
print("数据已保存")
