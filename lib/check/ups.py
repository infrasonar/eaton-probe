from asyncsnmplib.mib.mib_index import MIB_INDEX
from libprobe.asset import Asset
from ..snmpquery import snmpquery

QUERIES = (
    (MIB_INDEX['XUPS-MIB']['xupsIdent'], 'indent'),
    (MIB_INDEX['XUPS-MIB']['xupsBattery'], 'battery'),
    (MIB_INDEX['XUPS-MIB']['xupsInput'], 'input'),
    (MIB_INDEX['XUPS-MIB']['xupsInputEntry'], 'inputTable'),
    (MIB_INDEX['XUPS-MIB']['xupsOutput'], 'output'),
    (MIB_INDEX['XUPS-MIB']['xupsOutputEntry'], 'outputTable'),
    (MIB_INDEX['XUPS-MIB']['xupsBypass'], 'bypass'),
    (MIB_INDEX['XUPS-MIB']['xupsBypassEntry'], 'bypassTable'),
    (MIB_INDEX['XUPS-MIB']['xupsEnvironment'], 'environment'),
    (MIB_INDEX['XUPS-MIB']['xupsAlarm'], 'alarm'),
    (MIB_INDEX['XUPS-MIB']['xupsAlarmEntry'], 'alarmTable'),
    (MIB_INDEX['XUPS-MIB']['xupsAlarmEventEntry'], 'alarmEventTable'),
    (MIB_INDEX['XUPS-MIB']['xupsTest'], 'test'),
    (MIB_INDEX['XUPS-MIB']['xupsControl'], 'control'),
    (MIB_INDEX['XUPS-MIB']['xupsConfig'], 'config'),
    (MIB_INDEX['XUPS-MIB']['xupsTrapControl'], 'trapControl'),
    (MIB_INDEX['XUPS-MIB']['xupsRecep'], 'recep'),
    (MIB_INDEX['XUPS-MIB']['xupsRecepEntry'], 'recepTable'),
    (MIB_INDEX['XUPS-MIB']['xupsTopology'], 'topology'),
)


async def check_ups(
        asset: Asset,
        asset_config: dict,
        check_config: dict) -> dict:

    state = await snmpquery(asset, asset_config, check_config, QUERIES)
    for item in state.get('input', []):
        if 'Frequency' in item:
            item['Frequency'] *= 10
    for item in state.get('output', []):
        if 'Frequency' in item:
            item['Frequency'] *= 10
    for item in state.get('bypass', []):
        if 'Frequency' in item:
            item['Frequency'] *= 10
    for item in state.get('config', []):
        if 'Freq' in item:
            item['Freq'] *= 10        
    return state
