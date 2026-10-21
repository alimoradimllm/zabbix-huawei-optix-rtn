#!/usr/bin/env python3
"""Convert the Zabbix 7.4/6.4 'Huawei Optix RTN' template (SNMP walk[] + dependent items)
into a Zabbix 6.0 compatible one (classic SNMP discovery[] + plain SNMP agent items)."""
import sys, yaml, copy

def oid(o): return ('1.' + o[4:]) if o.startswith('iso.') else o.lstrip('.')

src, dst = sys.argv[1], sys.argv[2]
d = yaml.safe_load(open(src, encoding='utf-8'))
z = d['zabbix_export']; z['version'] = '6.0'
z['groups'] = z.pop('template_groups')  # 6.0 uses 'groups' (template_groups arrived in 6.2)
t = z['templates'][0]
t['templates'] = [{'name': 'ICMP Ping'}]
# drop the walk[] master items (not supported in 6.0); keep uptime
t['items'] = [i for i in t['items'] if not i['key'].startswith('walk.')]

for r in t['discovery_rules']:
    pp = r['preprocessing'][0]['parameters']          # [macro, oid, '0', macro, oid, '0', ...]
    args = []
    for i in range(0, len(pp), 3):
        args += [pp[i], oid(pp[i + 1])]
    r['type'] = 'SNMP_AGENT'
    r['snmp_oid'] = 'discovery[' + ','.join(args) + ']'
    r['delay'] = '1h'
    r.pop('master_item', None); r.pop('preprocessing', None)
    for p in r['item_prototypes']:
        steps = p['preprocessing']
        first = steps[0]
        assert first['type'] == 'SNMP_WALK_VALUE'
        p['type'] = 'SNMP_AGENT'
        p['snmp_oid'] = oid(first['parameters'][0])
        p['delay'] = '5m'
        p.pop('master_item', None)
        rest = [s for s in steps[1:]]
        if rest: p['preprocessing'] = rest
        else: p.pop('preprocessing')
yaml.safe_dump(d, open(dst, 'w', encoding='utf-8', newline='\n'), sort_keys=False, allow_unicode=True, width=200)
