# Copyright 2024 The MQI Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

import websocket 
import rel
import json

"""MQI is the main entry point of the api used to do most high level tasks"""
class MQI:
    def __init__(self, hostname, port):
       	self.hostname = hostname 
        self.port = port
        self.ws = None 

    """
    connect will create a connection to the cosen Raspberry Pi websocket. 
    If there is no avaialable a "NotFound" error is returned.

    @returns void

    """
    def connect(self):
        self.ws = websocket.WebSocket()
        self.ws.connect(self.hostname + ":" + self.port)

    """
    set_current will set the bias of the given arduino channel to the value

    @param arduino_id:int -- id of the arduino (0-4)
    @param channel:int -- channel id, can vary but will probably be in the range 0-7
    @param value:float -- the current value in mA
    @returns bool 

    """
    def set_current(self, channel, value, arduino_id=0):

        data = {
                "__MESSAGE__": "message",
                "command": "setCurrent",
                "id": channel,
                "name": "",
                "value": value

        }

        self.ws.send(json.dumps(data))
        print(self.ws.recv())

        return True
    """
    get_bias will return the bias of the channel for the given arduino id

    @param arduino_id:int -- id of the arduino (0-7)
    @param channel:int -- value of the channel, can vary but will be in the range 0-8
    @returns JsonObject

    """
    def get_bias(channel, arduino_id=0):
        data = {
                "__MESSAGE__": "message",
                "command": "getBias",
                "id": channel,
                "name": "",
                "value": "0"

        }

        self.ws.send(json.dumps(data))
        print(self.ws.recv())

        return True

    """
    get_resolution will return the resolution of the arduino

    @param arduino_id
    @returns JsonObject
    """
    def get_resolution(arduino_id):
        pass


    """
    get_all_bias will return the bias currents of all channels of the arduino

    @param arduino_id:int -- the id of the arduino to select
    @returns JsonObject -- the id of the arduino to select
    """
    def get_all_bias(arduino_id):
        data = {
          "__MESSAGE__": "message",
          "command": "allChannels",
          "id": "",
          "name": "",
          "value": "0"
        }
        print(self.ws.recv())
        return True

    """
    current_sweep will initiate a current sweep for the channel chosen

    @param arduino_id:int -- id of the arduino to select
    @param fr:float -- short for from, this is the current to start from (mA)
    @param to:float -- the current to stop at (mA)
    @param channel:int -- channel to select
    @param step_size:float -- the value to increment by
    @returns bool
    
    """
    def current_sweep(arduino_id, fr, to, channel, step_size):
        pass


    """
    current_sweep_full will initiate a current sweep for all channels on the arduino

    @param arduino_id:int -- id of the arduino to select
    @param fr:float -- short for from, this is the current to start from (mA)
    @param to:float -- the current to stop at (mA)
    @param channel:int -- channel to select
    @param step_size:float -- the value to increment by
    @returns bool

    """
    def current_sweep_full(arduino_id, fr, to, channel, step_size):
        pass

    """
    get_arduino_info will return the hardware specs of the arduino

    @param arduino_id:int -- id of the arduino to select
    @returns JsonObject
    """
    def get_arduino_info(arduino_id):
        pass

    """
    get_arduino_config will return the current config of the selected arduino

    @param arduino_id:int -- id of the arduino to select
    """
    def get_arduino_config(arduino_id):
        data = {
                "__MESSAGE__": "message",
                "command": "initinfo",
                "id": "",
                "name": "",
                "value": "" 

        }

        self.ws.send(json.dumps(data))
        print(self.ws.recv())

        return True
        pass

    """
    set_arduino_config will set the config for the selected arduino

    @param arduino_id: int -- id of the arduino to select
    @returns bool

    """
    def set_arduino_config(arduino_id):
        pass


    """ 

    auth will authenticate a user

    @param username: string -- this is the username usually just an email
    @param password:string -- a secret password 
    @returns bool

    """
    def auth(username, password):
        data = {
                "__MESSAGE__": "message",
                "command": "login",
                "id": username,
                "name": "",
                "value": password

        }

        self.ws.send(json.dumps(data))
        print(self.ws.recv())

        return True

    """
    get_logs will return the logs of the managing_module 

    @param filename:string
    @returns bool

    """
    def get_logs(filename):
        pass

    """
    set_channels will update the number of channels for the given arduino

    @param arduino_id:int -- the arduino to update
    @param channel_num:int -- the new number of channels
    @returns bool
    """
    def set_channels(channel_num, arduino_id=0):

        data = {
                "__MESSAGE__": "message",
                "command": "setChannels",
                "id": channel,
                "name": "",
                "value": channel_num 

        }

        self.ws.send(json.dumps(data))
        print(self.ws.recv())

        return True

    """

    @returns JsonObject
    """
    def get_current_ws():
        return ws;

    """
    get_number_of_arduinos returns the number of arduinos currently connected

    @returns int
    """
    def get_number_of_arduinos():
        pass


    """
    get_max_currents returns the switching currents for all channels

    @returns int[]
    """
    def get_max_currents():
        pass


    """
    get_max_current returns the switching currents for the given arduino
    """
    def get_max_current(arduino_id):
        pass


    """
    get_current_sweep returns timeseries of the current sweep

    @param arduino_id:int -- id of the arduino
    """
    def get_current_sweep(arduino_id):
        pass


    """
    get_current_sweep_all 

    @returns int[]
    """
    def get_current_sweep_all():
        pass

