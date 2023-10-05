from abc import ABC, abstractmethod


from pydantic import BaseModel
import numpy as np
from cmath import phase


from textengines.interfaces import TextEngine

# class I(BaseModel):
#     i: complex
#
#     def __repr__(self):
#         return f'{abs(self.i):.3f}A {np.degrees(phase(self.i)):.1f}°'
#
# class I3(BaseModel):
#     i: list[I, I, I]
#
#     def __repr__(self):
#         return f'L1: {repr(self.i[0])} L2: {repr(self.i[1])} L3: {repr(self.i[2])}'

class element(ABC, BaseModel):
    te: TextEngine | None = None

    @abstractmethod
    def get_electric(self):
        ...


    @abstractmethod
    def get_complex(self):
        ...

    def add_te(self, te: TextEngine):
        self.te = te

    def add_context(self, **kwargs):
        self.__dict__.update(kwargs)


class Channel(BaseModel):
    prim: int | float = 0
    sec: int | float = 0
    _v_prim: complex = 0 + 0j
    _v_sec: complex = 0 + 0j

    def __repr__(self):
        return f'{abs(self._v_prim):.3f} {np.degrees(phase(self._v_prim)):.1f}°'

    @property
    def ratio(self):
        return self.prim / self.sec

    @property
    def v_prim(self):
        return self._v_prim

    @property
    def v_sec(self):
        return self._v_sec

    @v_prim.setter
    def v_prim(self, v: complex):
        self._v_prim = v
        self._v_sec = v / self.prim * self.sec

    @v_sec.setter
    def v_sec(self, v: complex):
        self._v_sec = v
        self._v_prim = v * self.prim / self.sec

class AnalogInputs(BaseModel):
    name: str
    channels: list[Channel]

class Function(element):
    contacts: list[str] | None = None
    tests: list | dict | None = None
    analog_inputs: list[AnalogInputs] | None = None
    complex: list | None = None

    def get_complex(self, table_name: str, num_stage: int = 1):
        if self.complex:
            self.te.table_name(table_name)
            self.te.table_head('Контакт/сигнал', 'tсраб, мс', widths=(80, 20))
            for num, cont in enumerate(self.complex[num_stage]):
                if cont:
                    self.te.table_row(self.contacts[num], 'сработал' if cont == True else cont)

class Terminal(element):
    name: str


# class Terminal:
#
#     def __init__(self, data: dict, text_engine: TextEngine):
#         self.name = data['name']
#         self.device = data['device']
#         self.work_current = data.get('work_current')
#         self.te = text_engine
#         self.analog_inputs: list[AnalogInputs] = []
#         self.functions: list[Function] = []
#
#     def get_electric(self):
#         self.te.h2(f'Проверка терминала {self.name} {self.device}')
#         for func in self.functions:
#             func.get_electric()
#
#     def get_complex(self):
#         self.te.h2(f'Комплексная проверка терминала {self.name} {self.device}')
#         for func in self.functions:
#             func.get_complex()
#
#     def get_work_current(self):
#         if self.work_current:
#             self.te.h2(f'Проверка рабочим током и напряжением терминала {self.name} {self.device}')
#             for key, value in self.work_current.items():
#                 head = [item[0] for item in value]
#                 row = [item[1] for item in value]
#                 self.te.table_name(key)
#                 self.te.table_head(*head)
#                 self.te.table_row(*row)

class CBASVAL(BaseModel):
    UBase: float = 132.0
    IBase: float = 3000
    SBase: float = 229.0


