from mqi.v1.api import MQI 
from websocket import create_connection 

m = MQI("ws://mqicontroller.local", "8080")
m.connect()

m.set_current("1", "0")
