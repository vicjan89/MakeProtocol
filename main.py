import sys

from yaml import load
from textengines.ReStructuredText import ReStructuredText

# from RET670 import *
# from REF545 import *
from Pris import Pris

path = sys.argv[1]

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

with open(path, 'r', encoding='utf-8') as stream:
    data = load(stream, Loader=Loader)

rst = ReStructuredText(path=path.split('.')[0]+'.rst', static='_static')
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

pris = Pris(**data)
pris.add_te(rst)
pris.get_protocol()
rst.save()

# x = []
# y = []
# c = []
# i = 5
# print(f'при токе {i}А')
# print('1 ступень междуфазное')
# print(pris.rel511.zm1.get_points_charact_2ph_str())
# print(pris.rel511.zm1)
# print('1 ступень однофазное')
# print(pris.rel511.zm1.get_points_charact_1ph_str())
# print('2 ступень междуфазное')
# print(pris.rel511.zm2.get_points_charact_2ph_str())
# # print(pris.rel511.zm2)
# print('2 ступень однофазное')
# print(pris.rel511.zm2.get_points_charact_1ph_str())
# print('3 ступень междуфазное')
# print(pris.rel511.zm3.get_points_charact_2ph_str())
# # print(pris.rel511.zm3)
# print('3 ступень однофазное')
# print(pris.rel511.zm3.get_points_charact_1ph_str())
# print('4 ступень междуфазное')
# print(pris.rel511.zm4.get_points_charact_2ph_str())
# print(pris.rel511.zm4)
# print('4 ступень однофазное')
# print(pris.rel511.zm4.get_points_charact_1ph_str())
# print('5 ступень междуфазное')
# print(pris.rel511.zm5.get_points_charact_2ph_str())
# print(pris.rel511.zm5)
# print('5 ступень однофазное')
# print(pris.rel511.zm5.get_points_charact_1ph_str())
# x, y = pris.rel511.zm1.get_points_charact_1ph()
# plt.plot(x, y, c='C1', label='z1ph1')
# x, y = pris.rel511.zm2.get_points_charact_1ph()
# plt.plot(x, y, c='C2', label='z2ph1')
# x, y = pris.rel511.zm3.get_points_charact_1ph()
# plt.plot(x, y, c='C3', label='z3ph1')
# x, y = pris.rel511.zm4.get_points_charact_1ph()
# plt.plot(x, y, c='C4', label='z4ph1')
# x, y = pris.rel511.zm5.get_points_charact_1ph()
# plt.plot(x, y, c='C5', label='z5ph1')
# x, y = pris.rel511.zm1.get_points_charact_2ph()
# plt.plot(x, y, c='C6', label='z1ph2')
# x, y = pris.rel511.zm2.get_points_charact_2ph()
# plt.plot(x, y, c='C7', label='z2ph2')
# x, y = pris.rel511.zm3.get_points_charact_2ph()
# plt.plot(x, y, c='C8', label='z3ph2')
# x, y = pris.rel511.zm4.get_points_charact_2ph()
# plt.plot(x, y, c='C9', label='z4ph2')
# x, y = pris.rel511.zm5.get_points_charact_2ph()
# plt.plot(x, y, c='C10', label='z5ph2')
# x, y = pris.rel511.psd.get_points_charact_in()
# plt.plot(x, y, c='C11', label='PSD-IN')
# plt.legend()
# plt.grid()
# plt.show()