import json, re
from ingredients import I
from recipes import R
NUT=["kcal","p","f","c","ca","fe","zn","mg","vc"]
out=[]
for rec in R:
    tot={n:0.0 for n in NUT}
    for k,g in rec["ings"]:
        assert k in I, (rec["id"],k)
        for n in NUT: tot[n]+=I[k][n]*g/100
    for s in rec["steps"]:
        for k in re.findall(r"\{(\w+)\}",s):
            assert k in dict(rec["ings"]), (rec["id"],k)
    per={n:round(tot[n]/4,1) for n in NUT}
    out.append({**rec,"ings":[[k,g] for k,g in rec["ings"]],"per":per})
ids=[r["id"] for r in out]; assert len(ids)==len(set(ids))
db={"ingredients":I,"recipes":out}
json.dump(db,open("db.json","w"),ensure_ascii=False,separators=(",",":"))
print(len(out))
from collections import Counter
print(Counter(r["protein"] for r in out)); print(Counter(r["sauce"] for r in out))
for r in out: p=r["per"]; print(f'{r["id"]:28} {p["kcal"]:5.0f} P{p["p"]:5.1f} F{p["f"]:5.1f} C{p["c"]:5.1f} Fe{p["fe"]:4.1f} Ca{p["ca"]:4.0f}')
