from typing import Dict, List

DICTIONARY_OBSERVABLE_TOPICS: Dict[int, List[str]] = {
    4157: ['GOST_LARGE_SCALE_TEST/Datastreams(4157)/Observations', 'WRISTBAND-GW/868/Localization-Wristband/GeoTag00'],
    4159: ['GOST_LARGE_SCALE_TEST/Datastreams(4159)/Observations', 'WRISTBAND-GW/868/Localization-Wristband/GeoTag01'],
    4161: ['GOST_LARGE_SCALE_TEST/Datastreams(4161)/Observations', 'WRISTBAND-GW/868/Localization-Wristband/GeoTag02'],
    4163: ['GOST_LARGE_SCALE_TEST/Datastreams(4163)/Observations', 'WRISTBAND-GW/868/Localization-Wristband/GeoTag03'],
    4165: ['GOST_LARGE_SCALE_TEST/Datastreams(4165)/Observations', 'WRISTBAND-GW/868/Localization-Wristband/GeoTag04'],
    4169: ['GOST_LARGE_SCALE_TEST/Datastreams(4169)/Observations', 'WRISTBAND-GW/868/Localization-Wristband/GeoTag06'],
    4167: ['GOST_LARGE_SCALE_TEST/Datastreams(4167)/Observations', 'WRISTBAND-GW/868/Localization-Wristband/GeoTag05']
}

DICTIONARY_MQTT_WB_LOCAL_TOPICS = {
    1: ['GOST/SCRAL/Wristband/Localization', 'GeoTag00']
}

DICTIONARY_MQTT_WB_LST_TOPICS = {
    1: ['GOST_LARGE_SCALE_TEST/SCRAL/Wristband/Localization', 'GeoTag00']
}
