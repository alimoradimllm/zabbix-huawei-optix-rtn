# Huawei OptiX RTN – Zabbix templates

SNMP monitoring templates for **Huawei OptiX RTN microwave radios** (RTN 905, 910A, 950A, 980, 380H).

| Folder | What | Zabbix |
|---|---|---|
| [`zabbix-6.0/`](zabbix-6.0/) | `Huawei OptiX RTN by SNMP`: full-featured template with triggers, graphs, value maps and macros. Full documentation is here | **6.0 LTS** (tested) |
| [`zabbix-7.0/`](zabbix-7.0/) | The same template in the 7.0 export format (see [what differs](zabbix-7.0/README.md#what-differs-from-the-60-file)) | **7.0 LTS** |
| [`legacy/`](legacy/) | First, simpler template (walk-based original, 6.4 port, 6.0 re-implementation) and its converter script. See [legacy/README.md](legacy/README.md) | 7.4 / 6.4 / 6.0 |

## Quick start

1. *Data collection → Templates → Import* → `zabbix-6.0/Huawei_OptiX_RTN_by_SNMP.yaml` for Zabbix 6.0, or `zabbix-7.0/Huawei_OptiX_RTN_by_SNMP.yaml` for Zabbix 7.0.
2. Create a host for the radio with an **SNMP interface** (v2c community or v3) and link **Huawei OptiX RTN by SNMP**.
3. Wait for discovery (default 1 h; see [Troubleshooting](zabbix-6.0/README.md#troubleshooting)).

Full documentation: **[zabbix-6.0/README.md](zabbix-6.0/README.md)**.

## Status

- `zabbix-6.0/Huawei_OptiX_RTN_by_SNMP.yaml` was imported and tested on **Zabbix 6.0 LTS** and works.
- `zabbix-7.0/Huawei_OptiX_RTN_by_SNMP.yaml` differs from it by two lines (export version, `template_groups`); it has not yet been tested on a live Zabbix 7.0 server.
- The files in `legacy/` were only checked for structure.

If an import fails, open an issue with the exact Zabbix error message.
