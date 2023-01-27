from asyncsnmplib.mib.mib_index import MIB_INDEX
from asyncsnmplib.exceptions import SnmpNoAuthParams, SnmpNoConnection
from asyncsnmplib.utils import InvalidConfigException, snmp_queries
from libprobe.asset import Asset
from libprobe.exceptions import CheckException, IgnoreResultException

QUERIES = (
    MIB_INDEX['XUPS-MIB']['xupsIdent'],
    MIB_INDEX['XUPS-MIB']['xupsBattery'],
    MIB_INDEX['XUPS-MIB']['xupsInput'],
    MIB_INDEX['XUPS-MIB']['xupsInputEntry'],
    MIB_INDEX['XUPS-MIB']['xupsOutput'],
    MIB_INDEX['XUPS-MIB']['xupsOutputEntry'],
    MIB_INDEX['XUPS-MIB']['xupsBypass'],
    MIB_INDEX['XUPS-MIB']['xupsBypassEntry'],
    MIB_INDEX['XUPS-MIB']['xupsEnvironment'],
    MIB_INDEX['XUPS-MIB']['xupsAlarm'],
    MIB_INDEX['XUPS-MIB']['xupsAlarmEntry'],
    MIB_INDEX['XUPS-MIB']['xupsAlarmEventEntry'],
    MIB_INDEX['XUPS-MIB']['xupsTest'],
    MIB_INDEX['XUPS-MIB']['xupsControl'],
    MIB_INDEX['XUPS-MIB']['xupsConfig'],
    MIB_INDEX['XUPS-MIB']['xupsTrapControl'],
    MIB_INDEX['XUPS-MIB']['xupsRecep'],
    MIB_INDEX['XUPS-MIB']['xupsRecepEntry'],
    MIB_INDEX['XUPS-MIB']['xupsTopology'],
)


async def check_ups(
        asset: Asset,
        asset_config: dict,
        check_config: dict) -> dict:
    address = check_config.get('address')
    if address is None:
        address = asset.name
    try:
        state = await snmp_queries(address, asset_config, QUERIES)
    except SnmpNoConnection as e:
        raise CheckException('unable to connect')
    except (InvalidConfigException, SnmpNoAuthParams):
        raise IgnoreResultException
    except Exception:
        raise

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
