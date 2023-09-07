import sys


from yaml import load, dump


# from RET670 import *
# from REF545 import *
from hf_trakt import HfChannel


from textengines.ReStructuredText import ReStructuredText

path = sys.argv[1]

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

with open(path, 'r', encoding='utf-8') as stream:
    data = load(stream, Loader=Loader)

rst = ReStructuredText(path=path.split('.')[0]+'.rst')
# classes = {'RET670': RET670, 'REF545': REF545}
# device_obj = []
# for device in data:
#     device_cls = classes.get(device['device'], None)
#     if device_cls:
#         device_obj.append(device_cls(device, rst))
#         device_obj[-1].get_electric()
# rst.save()
# rst = ReStructuredText(path='source/complex_tec2_grodno.rst')
# classes = {'RET670': RET670, 'REF545': REF545}
# device_obj = []
# for device in data:
#     device_cls = classes.get(device['device'], None)
#     if device_cls:
#         device_obj.append(device_cls(device, rst))
#         device_obj[-1].get_complex()
# rst.save()
# rst = ReStructuredText(path='source/work_current.rst')
# classes = {'RET670': RET670, 'REF545': REF545}
# device_obj = []
# for device in data:
#     device_cls = classes.get(device['device'], None)
#     if device_cls:
#         device_obj.append(device_cls(device, rst))
#         device_obj[-1].get_work_current()
# rst.save()

hf = HfChannel(**data)
hf.add_te(rst)
hf.get_electric()
hf.get_complex()
rst.save()