# Huawei OptiX RTN by SNMP (Zabbix 6.0)

File: [`Huawei_OptiX_RTN_by_SNMP.yaml`](Huawei_OptiX_RTN_by_SNMP.yaml) – export format `6.0`, group `Templates/Network devices`.

Covers RTN 905, 910A, 950A, 980 and 380H. OIDs come from the Huawei OPTIX MIBs (enterprise `1.3.6.1.4.1.2011.2.25`),
built from SNMP walks of 419 NEs. Everything uses plain SNMP agent items and classic `discovery[...]` rules, so it works on
**Zabbix 6.0** (no SNMP `walk[]`, no dependent discovery).

> The description inside the file mentions model-specific child templates (e.g. *Huawei OptiX RTN 950A by SNMP*).
> Only the common template is included here; link it directly.

## Requirements

- Zabbix server/proxy 6.0+ with net-snmp and `fping` (for the ICMP items).
- SNMP enabled on the radio, with read access to the Huawei tree (`1.3.6.1.4.1.2011`) and `1.3.6.1.2.1.1`.
- A host with an SNMP interface.

## Changelog

**v2**
- New discovery rule *Radio link neighbour discovery*: far-end NE name per radio link, with a trigger when it changes.
- New *Calloff deviation* item and trigger per ODU (degradation since commissioning).
- Alarm triggers have flap protection (`{$RTN.ALARM.MIN.SAMPLES}` / `{$RTN.ALARM.MIN.ACTIVE}`).
- Ethernet utilization triggers replaced by Warning (`.WARN`) and Average (`.HIGH`) levels, evaluated over `{$RTN.ETH.UTIL.PERIOD}`, tunable per port.
- Low-RSL trigger context is now the ODU slot.
- New defaults: `{$RTN.ETH.UTIL.WARN}` 90 → 70, `{$RTN.INTERVAL.ALARM}` 2m → 5m, more ignored alarm IDs.

**v1** – initial release.

## Install

1. *Data collection → Templates → Import* → select the YAML.
2. *Data collection → Hosts → Create host*: add an **SNMP** interface (version, community or v3 credentials).
3. Link template **Huawei OptiX RTN by SNMP**.

## What it collects

### Plain items

| Item | Key | OID / source | Interval macro |
|---|---|---|---|
| ICMP ping / loss / response time | `icmpping`, `icmppingloss`, `icmppingsec` | simple check | default |
| NE ID | `rtn.ne.id` | `1.3.6.1.4.1.2011.2.25.3.40.2.1.1.0` | `{$RTN.INTERVAL.INVENTORY}` |
| NE IP address | `rtn.ne.ip` | `1.3.6.1.4.1.2011.2.25.3.40.2.2.1.0` | inventory |
| NE name | `rtn.ne.name` | `1.3.6.1.4.1.2011.2.25.4.30.21.1.1.0` | inventory |
| Device model | `rtn.ne.model` | `1.3.6.1.4.1.2011.2.25.4.30.21.1.8.0` | inventory |
| Software version | `rtn.ne.software` | `1.3.6.1.2.1.1.1.0` (sysDescr) | inventory |
| NE state | `rtn.ne.state` | `1.3.6.1.4.1.2011.2.25.4.30.21.1.7.0` | `{$RTN.INTERVAL.STATUS}` |
| Uptime | `rtn.ne.uptime` | `1.3.6.1.2.1.1.3.0` | status |
| SNMP availability | `zabbix[host,snmp,available]` | internal | – |

### Low-level discovery rules (15)

All run every `{$RTN.LLD.INTERVAL}` (1 h). Each uses `discovery[{#MACRO},OID]`; the prototypes read `<OID>.{#SNMPINDEX}`.

| Rule | Prototypes | Trigger / graph |
|---|---|---|
| Active alarm discovery | Alarm severity (ignores alarm IDs in `{$RTN.ALARM.EID.IGNORE}` and severities other than 1–3) | critical / major / minor problems with flap protection |
| Board discovery | Board state | – |
| Board temperature discovery | Temperature, high threshold | 2 triggers |
| Ethernet port discovery | RX/TX bits, RX/TX instant rate | Traffic graph |
| Ethernet RX drop / TX drop / FCS discovery | Dropped packets (pps), FCS errors | – |
| Ethernet port utilization discovery | RX / TX utilization % | Warning and Average triggers per direction |
| Radio IF discovery | RX/TX modulation, RX/TX/guaranteed/full capacity | 1 trigger, Capacity graph |
| Radio link neighbour discovery | Far-end NE name (from the neighbour the radio learns over the link) | Trigger when the far-end NE changes |
| Radio IF performance discovery | SNR avg/min/max, MSE avg/best/worst, BER (15-min PM) | MSE and SNR graphs |
| ODU discovery | RX/TX power, configured TX power, RX/TX frequency, T/R spacing, **calloff deviation** | RX and TX power graph, calloff trigger |
| ODU performance discovery | RSL and TSL min/avg/max (15-min PM) | 1 trigger, RSL graph |
| ODU frequency band discovery | Frequency band (GHz) | – |
| ODU transmitter state discovery | TX state | – |

Each metric has its own discovery rule because radios expose different tables (only rows that exist get items), so an
unsupported table leaves one rule empty instead of breaking the rest.

### Triggers

| Severity | Trigger | Condition |
|---|---|---|
| High | Unavailable by ICMP ping | last 3 pings failed |
| Warning | High ICMP ping loss | loss > `{$RTN.ICMP.LOSS.WARN}` for 5 m and < 100 % (depends on the ping trigger) |
| Warning | High ICMP ping response time | avg 5 m > `{$RTN.ICMP.RESPONSE.WARN}` |
| Average | NE is not in running state | `rtn.ne.state` = 0 |
| Warning | Device has been restarted | uptime < 10 m |
| Average | No SNMP data collection | SNMP unavailable for `{$SNMP.TIMEOUT}` |
| High | Board temperature above the board's high threshold | min 5 m ≥ threshold |
| Warning | Board temperature near the threshold | min 5 m ≥ threshold − `{$RTN.TEMP.MARGIN}` |
| Warning | Radio IF below full capacity (modulation downshift) | RX capacity < full capacity for 10 m |
| Warning | ODU low received signal level | max RX power 5 m < `{$RTN.ODU.RX.WARN}` (context = ODU slot) |
| Warning | ODU fading | RSL avg − RSL min > `{$RTN.RSL.FADE}` dB in the 15-min period |

| High / Average / Warning | Active alarm (critical / major / minor) | Alarm severity 1 / 2 / 3 present, and seen in at least `{$RTN.ALARM.MIN.SAMPLES}` polls within `{$RTN.ALARM.MIN.ACTIVE}` (flap protection) |
| Warning | Port RX / TX utilization above `{$RTN.ETH.UTIL.WARN}`% | min over `{$RTN.ETH.UTIL.PERIOD}` |
| Average | Port RX / TX utilization above `{$RTN.ETH.UTIL.HIGH}`% | min over `{$RTN.ETH.UTIL.PERIOD}` |
| Warning | Far-end NE changed | the neighbour name on a radio link changed (possible re-cabling or wrong link) |
| High | Calloff deviation above `{$RTN.CALLOFF.MAX}` dB for `{$RTN.CALLOFF.PERIOD}` | link has degraded since commissioning |

### Calloff deviation (link degradation since commissioning)

Item `{#ODU.NAME}: Calloff deviation` = (TX actual − TX configured) − (RX actual − calloff RX).
With TX at its configured power, this is how many dB the received level has dropped since commissioning.

Set the commissioning RX level **per ODU on the host** with the ODU number as context:

```
{$CALLOFF.RX:27} = -38      # ODU 27 was commissioned at -38 dBm
```

With no value (default `0`) the item stays 0 and the trigger never fires.

### Per-port and per-link tuning

Thresholds accept contexts, so one host can have different limits per port or ODU, e.g.
`{$RTN.ETH.UTIL.HIGH:17/5}` for port 17/5, `{$RTN.ODU.RX.WARN:"ODU 21 (IF 1/1)"}` for one ODU.

### Value maps

Huawei RTN alarm severity, board state, device type, modulation, NE state, ODU transmitter.

## Macros

| Macro | Default | Meaning |
|---|---|---|
| `{$RTN.INTERVAL.INVENTORY}` | `1h` | NE info polling |
| `{$RTN.INTERVAL.STATUS}` | `5m` | NE state and uptime |
| `{$RTN.INTERVAL.RADIO}` | `1m` | Radio (ODU/IF) values |
| `{$RTN.INTERVAL.TRAFFIC}` | `1m` | Ethernet/radio traffic |
| `{$RTN.INTERVAL.PM}` | `5m` | 15-minute performance counters |
| `{$RTN.INTERVAL.ALARM}` | `5m` | Active alarm polling |
| `{$RTN.LLD.INTERVAL}` | `1h` | All discovery rules |
| `{$RTN.ICMP.LOSS.WARN}` | `20` | ICMP loss % warning |
| `{$RTN.ICMP.RESPONSE.WARN}` | `0.3` | ICMP response time warning (s) |
| `{$RTN.ETH.UTIL.WARN}` | `70` | Ethernet utilization Warning (%) |
| `{$RTN.ETH.UTIL.HIGH}` | `80` | Ethernet utilization Average problem (%) |
| `{$RTN.ETH.UTIL.PERIOD}` | `5m` | How long utilization must stay above the level |
| `{$CALLOFF.RX}` | `0` | Commissioning RX power (dBm), set per ODU with context; 0 = off |
| `{$RTN.CALLOFF.MAX}` | `7` | Calloff deviation (dB) that raises a High problem |
| `{$RTN.CALLOFF.PERIOD}` | `12h` | How long the deviation must stay above the maximum |
| `{$RTN.ALARM.MIN.SAMPLES}` | `4` | Polls an alarm must be seen in before a problem opens |
| `{$RTN.ALARM.MIN.ACTIVE}` | `5m` | Window for those polls (flap protection) |
| `{$RTN.ODU.RX.WARN}` | `-65` | ODU RX level warning (dBm) |
| `{$RTN.ODU.RX.DROP}` | `10` | ODU RX drop threshold (dB) |
| `{$RTN.ODU.RX.NOSIGNAL}` | `-85` | ODU no-signal level (dBm) |
| `{$RTN.RSL.FADE}` | `10` | Fading depth (dB) |
| `{$RTN.TEMP.MARGIN}` | `10` | °C below the high threshold for the warning |
| `{$RTN.ALARM.EID.IGNORE}` | `^(13047\|412\|13144\|12860\|333)$` | Regex of alarm IDs that never raise problems (password-change, power-abnormal, licence and clock free-run alarms). Remove `412` to alarm on loss of a power input. |
| `{$RTN.ALARM.NODATA}` | `5m` | No-data window for alarms |
| `{$SNMP.TIMEOUT}` | `5m` | Window for "No SNMP data collection" |

Override macros on the host to tune per link.

## Troubleshooting

**`Invalid tag "/zabbix_export/version": unsupported version number`** – the file's export version is newer than the server.
This file is `6.0`, which 6.0 and newer accept. A 7.x export will not import into 6.0.

**Discovery creates no items**
1. *Hosts → Discovery*: hover the red icon on the rule to read the exact error.
2. Rules run hourly. To test, set `{$RTN.LLD.INTERVAL}` to `1m` on the host and press **Execute now**.
3. Check that Uptime has data, which proves SNMP access works.
4. Check that the radio answers the discovery OID, e.g. from the Zabbix server:
   ```bash
   snmpwalk -v2c -c COMMUNITY IP 1.3.6.1.4.1.2011.2.25.4.40.4.10.30.1.9   # ODU
   snmpwalk -v2c -c COMMUNITY IP 1.3.6.1.4.1.2011.2.25.4.30.14.1.1.1.2    # boards
   ```
   No output means the model lacks that table or the SNMP view blocks it, so that rule stays empty.
5. Not every model or firmware supports every table; 15-minute performance data may be disabled on the NE.

**Items "Not supported"** – check community/view access, and try disabling "Use combined requests" on the host's SNMP interface if the radio has a small SNMP PDU size.

## Validation

- Valid YAML, `zabbix_export.version: '6.0'`, 1 template, 11 items, 15 discovery rules, 6 value maps.
- 111 UUIDs, all unique and 32 hex characters.
- Filter conditions carry `formulaid` (a 6.0 requirement).
- **Tested by the repo owner on a live Zabbix 6.0 LTS server: imports and works.**
