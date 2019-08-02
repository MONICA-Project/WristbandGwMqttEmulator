import paho.mqtt.publish as publish
import json
from typing import Dict, Any
import datetime


class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.isoformat() + 'Z'

        return json.JSONEncoder.default(self, o)


class ServerMQTT(object):
    @staticmethod
    def publish(hostname: str, port: int, topic: str, client_id: str,  dictionary: Dict[str, Any]):
        try:
            if not dictionary:
                print('No Datat To Transfer')
                return False
            string_json = json.dumps(obj=dictionary,
                                     cls=DateTimeEncoder)
            publish.single(topic=topic,
                           payload=string_json,
                           hostname=hostname,
                           port=port,
                           client_id=client_id,
                           retain=False,
                           )
            print('Success Sending: {}'.format(string_json))
        except Exception as ex:
            print('Exception ServerMQTT Publish: {}'.format(ex))