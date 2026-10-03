from pathlib import Path
import json, time

base=Path(__file__).parent
fixtures=json.loads((base/'fixtures.json').read_text())
checks=[]
def check(name, actual, expected):
    passed=actual==expected
    checks.append({'check':name,'actual':actual,'expected':expected,'passed':passed})
    assert passed, (name,actual,expected)

start=time.perf_counter()
rows=fixtures['sales_rows']
net_revenue=sum((1 if r['type']=='sale' else -1)*r['quantity']*r['unit_price_usd'] for r in rows)
net_units=sum((1 if r['type']=='sale' else -1)*r['quantity'] for r in rows)
check('T09 net revenue',net_revenue,175)
check('T09 net units',net_units,4)
e=fixtures['economics']
contribution=e['price_per_customer']-e['variable_cost_per_customer']
break_even=(e['monthly_fixed_cost']+contribution-1)//contribution
check('T10 break-even customers',break_even,20)
check('T10 profit at 24',24*contribution-e['monthly_fixed_cost'],60)
check('T19 scenario profits',[n*contribution-e['monthly_fixed_cost'] for n in (10,20,24)],[-150,0,60])

def clean_rows(values):
    result=[]
    for value in values:
        if value is None or value == '':
            continue
        if value not in result:
            result.append(value)
    return result
check('T11 preserves zero/order',clean_rows([None,'',0,'0','a','a',0]),[0,'0','a'])
check('T11 all excluded',clean_rows([None,'',None]),[])
check('T11 negative number/order',clean_rows([-1,0,-1,'x']),[-1,0,'x'])

def mean_or_none(values):
    return sum(values)/len(values) if values else None
check('T12 empty',mean_or_none([]),None)
check('T12 known average',mean_or_none([2,4,6]),4)
check('T12 negative/zero',mean_or_none([-2,0,2]),0)
check('T17 vendor A six-month total',40*6+2*30,300)
check('T17 vendor B six-month total',25*6+6*30,330)
check('T17 build six-month total',20*30+2*6*30,960)

result={'scope':'Local deterministic feasibility pilot; not an isolated model trial','date':'2026-10-03','checks':checks,'passed':sum(c['passed'] for c in checks),'total':len(checks),'elapsed_seconds':time.perf_counter()-start,'model_runs':0}
(base/'feasibility_results.json').write_text(json.dumps(result,indent=2))
print(json.dumps({'scope':result['scope'],'passed':result['passed'],'total':result['total'],'model_runs':0}))
