# Huawei OptiX RTN – Zabbix 6.4 template

Zabbix template for monitoring Huawei OptiX RTN microwave radio links over SNMP
(Ethernet ports, IF/ODU radio units, TX/RX power, frequency, modulation, uptime, ICMP ping).

## The problem

Importing the original file into Zabbix 6.x fails with:

```
Invalid tag "/zabbix_export/version": unsupported version number.
```

The template was exported from **Zabbix 7.4** (`version: '7.4'`). Zabbix only imports files whose
export version is equal to or lower than its own, so a 6.x server rejects it.

## The fix

Zabbix only imports export files whose `version` is **equal to or lower than the server's**.
Editing the version tag is not enough for 6.0, because the template relies on features that 6.0 lacks:

| 7.4 / 6.4 feature used | In 6.0 |
|---|---|
| `walk[...]` SNMP master items | not available (added in 6.4) |
| `SNMP_WALK_TO_JSON` / `SNMP_WALK_VALUE` preprocessing | not available (6.4) |
| Dependent low-level discovery | different |
| `template_groups` export section | called `groups` in 6.0 (renamed in 6.2) |

So the 6.0 file is **re-implemented**: every discovery rule is a classic SNMP discovery
`discovery[{#MACRO},OID,...]`, and every item prototype is a plain SNMP agent item using
`<OID>.{#SNMPINDEX}`. Same OIDs, keys, units, value maps, tags, filters, and macros as the original.
The cost: each item is polled with its own SNMP request instead of one bulk walk (default 5m interval), so it is a little heavier on the device.

| File | Zabbix version |
|---|---|
| `Huawei_Optix_RTN_zabbix6.0.yaml` | **6.0 LTS** (generated) |
| `Huawei_Optix_RTN_zabbix6.4.yaml` | 6.4+ (header + linked-template name edit only) |
| `Huawei_Optix_RTN_original_zabbix7.4.yaml` | 7.4 (original export) |

The 6.0 file is produced from the original by `tools/convert_to_zabbix6.0.py`:

```bash
python tools/convert_to_zabbix6.0.py Huawei_Optix_RTN_original_zabbix7.4.yaml Huawei_Optix_RTN_zabbix6.0.yaml
```
(needs `pip install pyyaml`)

## Import

1. *Data collection → Templates → Import*, choose the file matching your version (see table above).
2. If import complains about a missing template, make sure the built-in **ICMP Ping**
   template exists (or change the linked name in the YAML to match yours).
3. Create the host with an **SNMP interface** (v2c/v3), link `Huawei Optix RTN`.

## What is monitored

- `system.net.uptime` – sysUpTime
- Master SNMP walk items: `walk.eth`, `walk.if`, `walk.if.net`, `walk.rf` (history disabled, text)
- Discovery of Ethernet interfaces (oper status ≠ 0): rx/tx bits, speed, state
- Discovery of IF and ODU/RF interfaces: state, TX/RX frequency, TX power, RSL, modulation
- ICMP ping/loss/response time via the linked ICMP Ping template

### Macros

| Macro | Default | Meaning |
|---|---|---|
| `{$ICMP_RESPONSE_TIME_WARN}` | `0.5` | ICMP response time warning (s) |
| `{$RSL_WARN}` | `-60` | RSL warning (dBm) |
| `{$RSL_CRIT}` | `-70` | RSL critical (dBm) |

## Status / caveats

None of these files has been tested against a live Zabbix server (none was available when written). 
The 6.0 file was checked structurally only.
Known oddity inherited from the original: the "Bits received/sent" regex is stored as `10 : (\\d+)` (double backslash); if those items stay empty, change it to `10 : (\d+)`. If your import reports another error, open an issue with the exact message.

## Files

- `Huawei_Optix_RTN_zabbix6.0.yaml` – Zabbix 6.0 LTS template
- `Huawei_Optix_RTN_zabbix6.4.yaml` – Zabbix 6.4+ template
- `tools/convert_to_zabbix6.0.py` – converter
- `Huawei_Optix_RTN_original_zabbix7.4.yaml` – original export
