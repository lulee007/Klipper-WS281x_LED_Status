'''
Functions to connect to the Moonraker API and perform actions.
'''
import json
import math
import requests


def printer_state(moonraker_settings):
    ''' Get printer status '''
    url = f"http://{moonraker_settings['host']}:{str(moonraker_settings['port'])}" \
        "/printer/objects/query?print_stats"
    try:
        ret = requests.get(url)
    except requests.exceptions.ConnectionError:
        return False
    try:
        return json.loads(ret.text)['result']['status']['print_stats']['state']
    except KeyError:
        return False


def power_status(moonraker_settings):
    ''' Get printer power status '''
    url = f"http://{moonraker_settings['host']}:{str(moonraker_settings['port'])}" \
        "/machine/device_power/devices?device=printer"
    ret = requests.get(url)
    return json.loads(ret.text)['result']['devices'][0]['status']


def printing_stats(moonraker_settings, base_temps):
    ''' Get stats for bed heater, hotend, and printing percent '''
    url = f"http://{moonraker_settings['host']}:{str(moonraker_settings['port'])}" \
        "/printer/objects/query?heater_bed&extruder&display_status"
    data = json.loads(requests.get(url).text)

    bed_temp = data['result']['status']['heater_bed']['temperature']
    bed_target = data['result']['status']['heater_bed']['target']
    bed_base_temp = base_temps[0] if base_temps else 0

    extruder_temp = data['result']['status']['extruder']['temperature']
    extruder_target = data['result']['status']['extruder']['target']
    extruder_base_temp = base_temps[1] if base_temps else 0
    bed_percent = heating_percent(bed_temp, bed_target, bed_base_temp)
    hotend_percent = heating_percent(
        extruder_temp, extruder_target, extruder_base_temp)
    # print(bed_percent,hotend_percent)
    return {
        'bed': {
            'temp': float(bed_temp)
        },
        'extruder': {
            'temp': float(extruder_temp)
        },
        'heating': {
            # 'total_percent': 100,
            'total_percent': (bed_percent+hotend_percent)/2,
        },
        'printing': {
            # 'done_percent': 62
            'done_percent': round(data['result']['status']['display_status']['progress'] * 100)
        }
    }


def heating_percent(temp, target, base_temp):
    ''' Get heating percent for given component '''
    if target == 0.0:
        return 0
    # temp float value can cause 0.5 diff
    if (target - temp) < 0.5:
        return 100
    return max(math.floor(((temp - base_temp) * 100) / (target - base_temp)), 0)


def power_off(moonraker_settings):
    ''' Power off the printer '''
    url = f"http://{moonraker_settings['host']}:{str(moonraker_settings['port'])}" \
        "/machine/device_power/off?printer"
    return requests.post(url).text
