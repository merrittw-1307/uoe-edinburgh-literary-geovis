import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('postgresql://wangmingyu@localhost:5432/litlong_edinburgh')

query = """
SELECT 
    lm.sentence_id,
    COUNT(DISTINCT l.text) AS place_count,
    STRING_AGG(DISTINCT l.text, ', ') AS places
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
GROUP BY lm.sentence_id
HAVING COUNT(DISTINCT l.text) > 1
ORDER BY place_count DESC
LIMIT 10;
"""

df = pd.read_sql(query, engine)
print(f"有多个地名的句子数量: {len(df)}")
print(df.to_string())
