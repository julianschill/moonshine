# LEDControl: Interface to LED Control by jackw01: https://github.com/jackw01/led-control
#
# Copyright (C) 2021 Julian Schill <j.schill@web.de>
#
# This file may be distributed under the terms of the GNU GPLv3 license.

import logging
import os
import asyncio
from tornado.httpclient import AsyncHTTPClient

class LEDControl:
    def __init__(self, config):
        self.server = config.get_server()
        self.name = config.get_name()
        self.server.register_remote_method(
            'set_led', self.set_led)
        self.addr = config.get('address')

    async def set_led(self, 
                brightness='',
                color_temp='',
                saturation='',
                primary_pattern='', 
                primary_speed='', 
                primary_scale='',
                secondary_pattern='',
                secondary_speed='',
                secondary_scale='',
                palette=''
                ):

        calls=[]
        if (brightness):
            calls.append(self.set_param('brightness',brightness))
        if (color_temp):
            calls.append(self.set_param('color_temp',color_temp))
        if (saturation):
            calls.append(self.set_param('saturation',saturation))
        if (primary_pattern):
            calls.append(self.set_param('primary_pattern',primary_pattern))
        if (primary_speed):
            calls.append(self.set_param('primary_speed',primary_speed))
        if (primary_scale):
            calls.append(self.set_param('primary_scale',primary_scale))
        if (secondary_pattern):
            calls.append(self.set_param('secondary_pattern',secondary_pattern))
        if (secondary_speed):
            calls.append(self.set_param('secondary_speed',secondary_speed))
        if (secondary_scale):
            calls.append(self.set_param('secondary_scale',secondary_scale))
        if (palette):
            calls.append(self.set_param('palette',palette))
        
        await asyncio.gather(*calls)
        return "done"

    async def set_param(self, key, value):
        url = f"{self.addr}/setparam?key={key}&value={value}"
        data=""        
        http_client = AsyncHTTPClient()
        try:
            response = await http_client.fetch(url)
            data = response.body
        except Exception:
            msg = f"Ledcontrol: Error setting parameter {key} to value {value}"
            logging.exception(msg)
            raise self.server.error(msg)

def load_component(config):
    return LEDControl(config)




