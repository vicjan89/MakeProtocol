from yaml import load, dump


from CVGAPC import CVGAPC
from OC4PTOC import OC4PTOC
from T3WPDIF import T3WPDIF
from RET670 import *
from REF545 import *

path = r'C:\Users\User\source\repos\TestRTDI\Resources\protocol_tec2_grodno.yaml'

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

with open(path, 'r', encoding='utf-8') as stream:
    data = load(stream, Loader=Loader)
html = '<!DOCTYPE html><html><head><meta charset="utf-8"><link rel="stylesheet" type="text/css" href="protocol.css">' \
       '</head><body>\n'
classes = {'RET670': RET670, 'REF545': REF545}
electric_html = ''
complex_html = ''
for device in data:
    device_cls = classes.get(device['device'], None)
    if device_cls:
        device_obj = device_cls(device)
        electric_html += device_obj.get_electric()
        complex_html += device_obj.get_complex()
html += electric_html
html += complex_html
html += '</body></html>'

with open('protocol.html', 'w', encoding='utf-8') as f:
    f.write(html)