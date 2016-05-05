from kafka import KafkaClient, SimpleProducer
from kafka.protocol import CODEC_SNAPPY
import json
import time

class HeartBeat:

    def __init__(self,qinfo):

        self.topic = qinfo['kafka_topic']
        self.client = KafkaClient(qinfo['kafka_broke'])
        self.producer = SimpleProducer(self.client, codec=CODEC_SNAPPY)


    def send(self,name,num=1):
        data = {
            "name":name,
            "num":num,
            "time":int(time.time())
        }
        print "***************send********************"
        data_str = json.dumps(data)
        self.producer.send_messages(self.topic, data_str)

    def close(self):
        self.client.close()
        self.producer.stop()
