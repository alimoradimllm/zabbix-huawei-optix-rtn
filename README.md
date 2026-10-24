# Huawei OptiX RTN – Zabbix templates

SNMP monitoring templates for **Huawei OptiX RTN microwave radios** (RTN 905, 910A, 950A, 980, 380H).

| Folder | What | Zabbix |
|---|---|---|
| [`zabbix-6.0/`](zabbix-6.0/) | **Recommended.** `Huawei OptiX RTN by SNMP`: full-featured template with triggers, graphs, value maps and macros | **6.0 LTS** (newer servers import 6.0 exports too) |
| [`legacy/`](legacy/) | First, simpler template (walk-based original, 6.4 port, 6.0 re-implementation) and its converter script. See [legacy/README.md](legacy/README.md) | 7.4 / 6.4 / 6.0 |

## Quick start

1. *Data collection → Templates → Import* → `zabbix-6.0/Huawei_OptiX_RTN_by_SNMP.yaml`.
2. Create a host for the radio with an **SNMP interface** (v2c community or v3) and link **Huawei OptiX RTN by SNMP**.
3. Wait for discovery (default 1 h; see [Troubleshooting](zabbix-6.0/README.md#troubleshooting)).

Full documentation: **[zabbix-6.0/README.md](zabbix-6.0/README.md)**.

## Status

These files have not been imported into a live Zabbix server by the repo author. They were checked for structure
(valid YAML, 102 unique UUIDs, 6.0 export layout, `formulaid` on filter conditions).
If an import fails, open an issue with the exact Zabbix error message.
