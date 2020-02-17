class Settings:
    list_events_publish = list()
    flag_connected = 0
    job_id = 'publish_mqtt_scral_observables'
    just_one_time_execution = 0

    hostname = 'localhost'
    port = 1883
    client_id = 'mqtt_wb_simulator'

    interval_sending_secs = 7
    device_number = 5
    device_name = "GeoTag"
    topic_prefix = "GOST/"
    device = "Wristband"
    property = "Localization"


class RemoteSettings:
    list_events_publish = list()
    flag_connected = 0
    job_id = 'publish_mqtt_scral_observables'
    just_one_time_execution = 1

    # hostname_wp3 = "monappdwp3.monica-cloud.eu"
    hostname = 'monapp-lst.monica-cloud.eu'
    # hostname_rab = 'mpclsifrmq01.monica-cloud.eu'
    port = 1884
    client_id = 'mqtt_wb_simulator'

    interval_sending_secs = 5
    device_number = 10
    device_name = "GeoTag"
    # topic_prefix = "GOST_WOODSTOWER/"
    topic_prefix_lst = "GOST_LARGE_SCALE_TEST/"
    device = "Wristband"
    property = "Localization"