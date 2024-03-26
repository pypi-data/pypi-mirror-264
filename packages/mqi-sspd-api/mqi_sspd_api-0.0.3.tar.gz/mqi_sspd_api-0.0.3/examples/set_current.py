import sys
sys.path.append("../mqi-api")
from v1.api import MQI 

m = MQI("ws://mqicontroller.local", "8080")
m.connect()

# Will set current of channel 1 to 0
m.set_current("1", "0")
