import json, re
from ingredients import I
from recipes import R
from extras import NAMES, CUISINE, T, TOP
NUT=["kcal","p","f","c","ca","fe","zn","mg","vc"]
def per(ings):
    return {n:round(sum(I[k][n]*g/100 for k,g in ings)/4,1) for n in NUT}
out=[]
for rec in R:
    for k,g in rec["ings"]: assert k in I,(rec["id"],k)
    for s in rec["steps"]:
        for k in re.findall(r"\{(\w+)\}",s): assert k in dict(rec["ings"]),(rec["id"],k)
    rec=dict(rec); rec["name"]=NAMES.get(rec["id"],rec["name"])
    rec["cuisine"]=rec.get("cuisine") or CUISINE.get(rec["id"],"home")
    t=T[TOP[rec["id"]]]
    rec["topping"]={"name":t[0],"ings":[[k,g] for k,g in t[1]],"how":t[2],"per":per(t[1])}
    rec["ings"]=[[k,g] for k,g in rec["ings"]]; rec["per"]=per(rec["ings"])
    out.append(rec)
assert len({r["id"] for r in out})==len(out) and all(r["id"] in TOP for r in out)
json.dump({"ingredients":I,"recipes":out},open("db.json","w"),ensure_ascii=False,separators=(",",":"))
from collections import Counter
print(len(out), Counter(r["cuisine"] for r in out), Counter(r["sauce"] for r in out))
