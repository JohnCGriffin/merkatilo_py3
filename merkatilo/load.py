
__all__ = [ 'lo' ]

import os
import threading
import merkatilo.core as core
import merkatilo.obs_series as obs_series
import json
import re
import urllib.request

def __normalize_id(name):
    name = name.upper()
    if name.find("::") < 0:
        name = '{}::CLOSE'.format(name)
    return name

__default_loader_config = None

def __default_loader(id):
    
    global __default_loader_config
    if __default_loader_config is None:
        file_name = "default-loader-config.json"
        personal_config = os.getenv("HOME") + "/.merkatilo/" + file_name
        system_config = "/etc/merkatilo/" + file_name
        config_file = ((os.path.exists(personal_config) and personal_config)
                       or
                       (os.path.exists(system_config) and system_config))
        if not config_file:
            raise Exception("neither {} nor {} found".format(personal_config,system_config))
        __default_loader_config = json.load(open(config_file))
            
    conf = __default_loader_config
    data_source = conf['data-source']
    rx = data_source['regex']
    replacement = data_source['replacement']
    headers = data_source.get('headers',[])
    normalized_id = __normalize_id(id)
    p = re.compile(rx)
    url = p.sub(replacement, normalized_id)
    req = urllib.request.Request(url, headers=headers)
    lines = urllib.request.urlopen(req).read().decode("utf-8").strip().split("\n")
    entries = []
    for line in lines:
        try:
            pair = line.split()
            entries.append((core.to_jdate(pair[0]),float(pair[1])))
        except:
            pass
    return obs_series.obs_to_series(entries, name=normalized_id)

__local = threading.local()
__local.loader = __default_loader

# Return active loader with optional setting
def loader(f=None):
    result = __local.loader
    if f:
        __local.loader = f
    return result

def lo(id):
    
    '''The :code:`lo(ID)` command is a sample mechanism for 
    importing time series.  You will likely need to create your 
    own implementation of a loader and set it with
    merkatilo.load.loader(your_function)'''

    return __local.loader(id)


