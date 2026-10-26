# Huawei OptiX RTN by SNMP (Zabbix 7.0 LTS)

File: [`Huawei_OptiX_RTN_by_SNMP.yaml`](Huawei_OptiX_RTN_by_SNMP.yaml) – export format `7.0`.

This is the same template as the [Zabbix 6.0 version](../zabbix-6.0/README.md), converted to the 7.0 export format.
**Items, discovery rules, triggers, graphs, value maps, macros, OIDs and UUIDs are identical.** Everything in the
[6.0 README](../zabbix-6.0/README.md) (what is collected, triggers, macros, calloff deviation, troubleshooting, changelog)
applies here unchanged.

## What differs from the 6.0 file

Only two lines:

| 6.0 file | 7.0 file | Why |
|---|---|---|
| `version: '6.0'` | `version: '7.0'` | Zabbix 7.0 import version |
| top-level `groups:` | top-level `template_groups:` | The section was renamed in the 6.2+ export format; 7.0 rejects `groups` there |

You can verify it:

```bash
diff ../zabbix-6.0/Huawei_OptiX_RTN_by_SNMP.yaml Huawei_OptiX_RTN_by_SNMP.yaml
```

The template still uses classic `discovery[...]` SNMP discovery (no `walk[]`), which Zabbix 7.0 continues to support.
Because the UUIDs are the same, importing the 7.0 file over a template imported from the 6.0 file updates it in place.

## Install

1. *Data collection → Templates → Import* → select this YAML.
2. Create the host with an **SNMP** interface and link **Huawei OptiX RTN by SNMP**.

## Status

- Valid YAML, export version `7.0`, template content byte-for-byte equal to the 6.0 file after parsing.
- **Not yet imported on a live Zabbix 7.0 server by the repo owner.** The 6.0 file is tested on 6.0 LTS.
  If the 7.0 import fails, open an issue with the exact error message.

Which file do I use?

| Server | File |
|---|---|
| 6.0 LTS | `../zabbix-6.0/` |
| 7.0 LTS | this folder |
