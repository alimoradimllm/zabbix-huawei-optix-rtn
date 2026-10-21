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

| Change | Why |
|---|---|
| `zabbix_export.version: '7.4'` → `'6.4'` | Export format version Zabbix 6.4 accepts |
| Linked template `Template Module ICMP Ping` → `ICMP Ping` | Name used by the built-in template in 6.4 |

Nothing else needed changing: the file uses only features available in 6.4 (`walk[]` SNMP OIDs,
dependent items, `SNMP_WALK_TO_JSON` / `SNMP_WALK_VALUE` preprocessing, dependent LLD, value maps).

### Which Zabbix version do I need?

- **6.4 and newer (6.4, 7.0, 7.2...)**: use `Huawei_Optix_RTN_zabbix6.4.yaml`.
- **6.0 LTS: not supported.** SNMP `walk[]` items and the `SNMP_WALK_*` preprocessing steps were
  introduced in 6.4, so this template cannot work on 6.0 even if the version tag were edited.
  Upgrade to 6.4+ or rewrite it with classic SNMP discovery (`discovery[]`).
- **7.4**: use `Huawei_Optix_RTN_original_zabbix7.4.yaml`.

## Import

1. *Data collection → Templates → Import*, choose `Huawei_Optix_RTN_zabbix6.4.yaml`.
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

The conversion was made by editing the export header and linked template name. It has **not been
tested against a live Zabbix 6.4 server**. If your import reports another error, open an issue with the exact message.

## Files

- `Huawei_Optix_RTN_zabbix6.4.yaml` – converted template
- `Huawei_Optix_RTN_original_zabbix7.4.yaml` – original export
