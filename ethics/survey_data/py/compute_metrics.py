import pandas as pd
from collections import Counter
from scipy import stats

df = pd.read_csv('../processed/survey_cleaned_translated_2026-08-20.csv')
df.columns = [c.strip().replace('\xa0','').strip() for c in df.columns]
N = len(df)
n_expert = (df['group']=='expert').sum()
n_general = (df['group']=='general').sum()
print(f"N={N} (expert={n_expert}, general={n_general})\n")

designs = {
    'Radar':  dict(prefix='Q-FP-Radar', f0_correct='Old Town', f1_correct='Walter Scott',
                   m1_key={'A':'Irvine Welsh','B':'Robert Louis Stevenson','C':'Alexander McCall Smith','D':'John Gibson Lockhart','E':'Walter Scott'},
                   p1_correct='Shape D = John Gibson Lockhart, Shape E = Walter Scott'),
    'Bar':    dict(prefix='Q-FP-Bar', f0_correct='Canongate', f1_correct='John Gibson Lockhart',
                   m1_key={'A':'Walter Scott','B':'Alexander McCall Smith','C':'Robert Louis Stevenson','D':'Irvine Welsh','E':'John Gibson Lockhart'},
                   p1_correct='Row A = Walter Scott, Row D = Irvine Welsh'),
    'Multi':  dict(prefix='Q-FP-Multi', f0_correct='Leith', f1_correct='Robert Louis Stevenson',
                   m1_key={'A':'John Gibson Lockhart','B':'Irvine Welsh','C':'Walter Scott','D':'Robert Louis Stevenson','E':'Alexander McCall Smith'},
                   p1_correct='Map A = John Gibson Lockhart, Map D = Robert Louis Stevenson'),
}

print("="*70)
print("FINGERPRINT TASKS")
print("="*70)
for name, d in designs.items():
    p = d['prefix']
    print(f"\n--- {name} (blind author = {d['f1_correct']}) ---")
    f0 = df[f'{p}-F0']
    f0_correct = (f0 == d['f0_correct']).sum()
    print(f"F0 (comprehension check, correct={d['f0_correct']!r}): {f0_correct}/{N} = {f0_correct/N*100:.0f}%")

    f1 = df[f'{p}-F1']
    f1_correct = (f1 == d['f1_correct'])
    print(f"F1 (Top-1 identify): {f1_correct.sum()}/{N} = {f1_correct.sum()/N*100:.0f}%")
    print(f"  F1 answer distribution: {Counter(f1).most_common()}")

    f1b = df[f'{p}-F1b']
    top2 = f1_correct | (f1b == d['f1_correct'])
    print(f"Top-2 (F1 or F1b correct): {top2.sum()}/{N} = {top2.sum()/N*100:.0f}%")

    f2 = df[f'{p}-F2']
    print(f"F2 confidence distribution: {Counter(f2).most_common()}")

    f4 = df[f'{p}-F4']
    print(f"F4 self-explanatory: {Counter(f4).most_common()}")

    # M1 confusion matrix
    print("M1 matching (shape -> answer, correct marked *):")
    m1_correct_count = 0
    m1_total = 0
    confusion = Counter()
    for letter, true_author in d['m1_key'].items():
        col = f'{p}-M1_{"ABCDE".index(letter)+1}'
        vals = df[col]
        for v in vals:
            m1_total += 1
            confusion[(true_author, v)] += 1
            if v == true_author:
                m1_correct_count += 1
    print(f"  M1 overall accuracy (diagonal/total): {m1_correct_count}/{m1_total} = {m1_correct_count/m1_total*100:.0f}%")
    top_confusions = [(k,v) for k,v in confusion.most_common() if k[0]!=k[1]]
    print(f"  Top off-diagonal confusions: {top_confusions[:5]}")

    m2 = df[f'{p}-M2']
    print(f"M2 subjective distinctiveness: {Counter(m2).most_common()}")

    p1 = df[f'{p}-P1']
    p1_correct = (p1 == d['p1_correct']).sum()
    print(f"P1 (hardest-pair 2AFC, correct={d['p1_correct']!r}): {p1_correct}/{N} = {p1_correct/N*100:.0f}%")

print("\n" + "="*70)
print("FINGERPRINT RANKING")
print("="*70)
print(Counter(df['Q-FPRank']).most_common())

print("\n" + "="*70)
print("TOPOLOGY TASKS")
print("="*70)
topo = {
    'Network': dict(prefix='Q-TP-Network', strength_cols=[('New Town & Princes Street',18),('Lochend & Waverley Station',4),('Leith & Silvermills',2)],
                     cluster_correct='New Town, Princes Street, Dundas Street, Stockbridge'),
    'Linear':  dict(prefix='Q-TP-Linear', strength_cols=[('Dundas Street & Princes Street',17),('Old Town & Princes Street',6),("Arthur's Seat & Haddington",2)],
                     cluster_correct='Leith Walk, Lochend, Pilrig, Waverley Station'),
    'Metro':   dict(prefix='Q-TP-Metro', strength_cols=[('Bruntsfield & Dundas Street',16),('Howe Street & Stockbridge',6),('Dalkeith & Linlithgow',2)],
                     cluster_correct='University of Edinburgh, Royal Society of Edinburgh, Castle Street, St Giles'),
}
scale_map = {'Not connected at all':1,'Slightly connected':2,'Moderately connected':3,'Strongly connected':4,'Extremely strongly connected':5}

def norm_place(s):
    if pd.isna(s): return ''
    return str(s).strip().lower().replace('princess','princes').replace("'",'').replace('  ',' ')

for name, d in topo.items():
    p = d['prefix']
    print(f"\n--- {name} ---")
    t1a = df[f'{p}-T1_1'].apply(norm_place)
    t1b_ = df[f'{p}-T1_2'].apply(norm_place)
    correct_pair = {'leith','princes street'}
    t1_correct = [(a in correct_pair and b in correct_pair) for a,b in zip(t1a,t1b_)]
    print(f"T1 (Leith & Princes Street correct): {sum(t1_correct)}/{N} = {sum(t1_correct)/N*100:.0f}%")

    t2 = df[f'{p}-T2'] if f'{p}-T2' in df.columns else df.get(f'{p}-T2 ')
    print(f"T2 near/far distribution: {Counter(t2).most_common()}")

    strength_vals = []
    for col_name, weight in d['strength_cols']:
        col = f'{p}-Strengt_{d["strength_cols"].index((col_name,weight))+1}'
        vals = df[col].map(scale_map)
        for v in vals.dropna():
            strength_vals.append((weight, v))
    if len(strength_vals) > 2:
        weights, ratings = zip(*strength_vals)
        r, pval = stats.pearsonr(weights, ratings)
        print(f"T-Strength correlation (rating vs real weight, n={len(strength_vals)} data points): r={r:.2f}, p={pval:.3f}")
    for col_name, weight in d['strength_cols']:
        idx = d['strength_cols'].index((col_name,weight))+1
        col = f'{p}-Strengt_{idx}'
        print(f"  {col_name} (weight={weight}): {Counter(df[col]).most_common()}")

    cluster_col = f'{p}-Cluster'
    cluster = df[cluster_col]
    cluster_correct = (cluster == d['cluster_correct']).sum()
    print(f"T-ClusterVerify (correct={d['cluster_correct'][:40]}...): {cluster_correct}/{N} = {cluster_correct/N*100:.0f}%")
    print(f"  distribution: {Counter(cluster).most_common()}")

    t5 = df[f'{p}-T5']
    print(f"T5 self-explanatory: {Counter(t5).most_common()}")

print("\n" + "="*70)
print("TOPOLOGY RANKING")
print("="*70)
print(Counter(df['Q-TopoRank']).most_common())
