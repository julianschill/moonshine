# LEDControl: Interface to LED Control by jackw01: https://github.com/jackw01/led-control
#
# Copyright (C) 2021 Julian Schill <j.schill@web.de>
#
# This file may be distributed under the terms of the GNU GPLv3 license.

import logging
import json
from tornado.httpclient import AsyncHTTPClient

class LEDControl:
    def __init__(self, config):
        self.server = config.get_server()
        self.name = config.get_name()
        self.server.register_remote_method(
            'set_led', self.set_led)
        self.addr = config.get('address')

    async def set_led(self, 
                preset = '',
                group = 'main',
                brightness='',
                saturation='',
                pattern='', 
                speed='', 
                scale='',
                palette='',
                global_brightness='',
                global_saturation=''
                ):
        
        http_client = AsyncHTTPClient()
        payload={}
        payload["groups"]={}
        if preset: 
            url = f"{self.addr}/getpresets"
            
            try:
                response = await http_client.fetch(url, method='GET', headers={"Content-Type": "application/json"})
                presets=json.loads(response.body)
                payload["groups"] = presets[preset]
            except Exception:
                msg = f"Ledcontrol: Error reading presets."
                logging.exception(msg)
                raise self.server.error(msg)
        else:
            url = f"{self.addr}/getsettings"
            try:
                response = await http_client.fetch(url, method='GET', headers={"Content-Type": "application/json"})
                response_body=json.loads(response.body)
                groups = response_body["groups"]
                for g in groups:
                    if groups[g]["name"] == group:
                        group = g

            except Exception:
                msg = f"Ledcontrol: Error reading settings."
                logging.exception(msg)
                raise self.server.error(msg)

            payload["groups"][group]={}
            if (brightness):
                payload["groups"][group]["brightness"] = float(brightness)
            if (saturation):
                payload["groups"][group]["saturation"] = float(saturation)
            if (pattern):
                payload["groups"][group]["function"] = int(pattern)
            if (speed):
                payload["groups"][group]["speed"] = float(speed)
            if (scale):
                payload["groups"][group]["scale"] = float(scale)
            if (palette):
                payload["groups"][group]["palette"] = int(palette)

        if (global_brightness):
            payload["global_brightness"] = float(global_brightness)
        if (global_saturation):
            payload["global_saturation"] = float(global_saturation)

        url = f"{self.addr}/updatesettings"
        body = json.dumps(payload)
        try:
            response = await http_client.fetch(url, method='POST', headers={"Content-Type": "application/json"}, body=body)
        except Exception:
            msg = f"Ledcontrol: Error setting parameter. Payload: {payload}"
            logging.exception(msg)
            raise self.server.error(msg)

        return "done"

def load_component(config):
    return LEDControl(config)
