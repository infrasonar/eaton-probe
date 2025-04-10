from asyncsnmplib.mib.mib_index import MIB_INDEX
from libprobe.asset import Asset
from ..snmpclient import get_snmp_client
from ..snmpquery import snmpquery

QUERIES = (
    (MIB_INDEX['XUPS-MIB']['xupsIdent'], False),
    (MIB_INDEX['XUPS-MIB']['xupsBattery'], False),
    (MIB_INDEX['XUPS-MIB']['xupsInput'], False),
    (MIB_INDEX['XUPS-MIB']['xupsInputEntry'], True),
    (MIB_INDEX['XUPS-MIB']['xupsOutput'], False),
    (MIB_INDEX['XUPS-MIB']['xupsOutputEntry'], True),
    (MIB_INDEX['XUPS-MIB']['xupsBypass'], False),
    (MIB_INDEX['XUPS-MIB']['xupsBypassEntry'], True),
    (MIB_INDEX['XUPS-MIB']['xupsEnvironment'], False),
    (MIB_INDEX['XUPS-MIB']['xupsAlarm'], False),
    (MIB_INDEX['XUPS-MIB']['xupsAlarmEntry'], True),
    (MIB_INDEX['XUPS-MIB']['xupsAlarmEventEntry'], True),
    (MIB_INDEX['XUPS-MIB']['xupsTest'], False),
    (MIB_INDEX['XUPS-MIB']['xupsControl'], False),
    (MIB_INDEX['XUPS-MIB']['xupsConfig'], False),
    (MIB_INDEX['XUPS-MIB']['xupsTrapControl'], False),
    (MIB_INDEX['XUPS-MIB']['xupsRecep'], False),
    (MIB_INDEX['XUPS-MIB']['xupsRecepEntry'], True),
    (MIB_INDEX['XUPS-MIB']['xupsTopology'], False),
)


async def check_ups(
        asset: Asset,
        asset_config: dict,
        check_config: dict) -> dict:
    snmp = get_snmp_client(asset, asset_config, check_config)
    state = await snmpquery(snmp, QUERIES)
    for item in state.get('xupsInputEntry', []):
        if 'xupsInputFrequency' in item:
            item['xupsInputFrequency'] *= 10
    for item in state.get('xupsOutputEntry', []):
        if 'xupsOutputFrequency' in item:
            item['xupsOutputFrequency'] *= 10
    for item in state.get('xupsBypassEntry', []):
        if 'xupsBypassFrequency' in item:
            item['xupsBypassFrequency'] *= 10
    for item in state.get('xupsConfig', []):
        if 'xupsConfigOutputFreq' in item:
            item['xupsConfigOutputFreq'] *= 10
    return state
