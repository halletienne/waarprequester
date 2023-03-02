#!/usr/bin/env python3
## This help import current Flows/Partners/Sites/FlowTemplates into the Flask DB

from waarp import WaarpHelper
import os
import configparser


## Real start of function
# Set default value for SSL verification
ssl_verify = True

config_file_path = os.path.join(os.environ['HOME'], '.waarp.env')

if os.path.exists(config_file_path):
    print('Reading info from config file')
    config = configparser.ConfigParser()
    config.read(config_file_path)
    if 'SERVER' in config['WAARP-MANAGER']:
      server = config['WAARP-MANAGER'].get('SERVER')
    if 'USERNAME' in config['WAARP-MANAGER']:
      username = config['WAARP-MANAGER'].get('USERNAME')
    if 'PASSWORD' in config['WAARP-MANAGER']:
      password = config['WAARP-MANAGER'].get('PASSWORD')
    if 'SSL_VERIFY' in config['WAARP-MANAGER']:
      if config['WAARP-MANAGER'].get('SSL_VERIFY').lower() in ["false", "0", "no"]:
        ssl_verify = False

waarp = WaarpHelper(waarp_manager_addr=server, 
  waarp_manager_user=username,
  waarp_manager_passwd=password,
  ssl_verify=ssl_verify)

## This inventory need higher privilege
#waarp.link_inventory()
waarp.flow_inventory()
waarp.partner_inventory()
waarp.site_inventory()
waarp.template_inventory()