import os
from tpds.devices import TpdsDevices

# Add the Part information
TpdsDevices().add_device_info(os.path.join(os.path.dirname(__file__), 'parts'))
