import datetime


class Localization(object):
    def __init__(self, tag_id: str, iot_id: int, lat: float, lon: float):
        self.tagId = tag_id
        self.iot_id = iot_id
        self.type = 868
        self.areaId = "LST"
        self.motion_state = "unknown"
        self.lat = lat  # 55.67298336627162
        self.lon = lon  # 12.56703788516.0
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.bearing = 0.0
        self.height = 0.0
        self.herr = 0.0
        self.battery_level = 2.9
        self.timestamp = datetime.datetime.utcnow()

    def to_dictionary(self):
        return {
            "tagId": self.tagId,
            "type": "868",
            "areaId": "LST",
            "motion_state": "unknown",
            "lat": self.lat,
            "lon": self.lon,
            "x": self.x,
            "y": self.y,
            "z": self.z,
            "bearing": 0.0,
            "height": 0.0,
            "herr": 0.0,
            "battery_level": 2.9,
            "timestamp": self.timestamp
        }

    def to_scral_dictionary(self):
        return {
            "Datastream": {
                "@iot.id": self.iot_id
            },
            "phenomenonTime": self.timestamp,
            "result": {
                "tagId": self.tagId,
                "type": "868",
                "areaId": "LST",
                "motion_state": "unknown",
                "lat": self.lat,
                "lon": self.lon,
                "x": self.x,
                "y": self.y,
                "z": self.z,
                "bearing": 0.0,
                "height": 0.0,
                "herr": 0.0,
                "battery_level": 2.9,
                "timestamp": self.timestamp
            }
        }
