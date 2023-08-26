from abc import ABC, abstractmethod


from pydantic import BaseModel
import numpy as np
from cmath import phase

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

class Function(ABC, BaseModel):
    contacts: list[str]
    tests: list | dict | None
    analog_inputs: list[AnalogInputs] | None = None

    @abstractmethod
    def get_electric(self):
        ...
    @abstractmethod
    def get_complex(self):
        ...

class Terminal:

    def __init__(self, data: dict):
        self.name = data['name']
        self.device = data['device']
        self.analog_inputs: list[AnalogInputs] = []
        self.functions: list[Function] = []

    def get_electric(self):
        html = f'<h2>Проверка терминала {self.name} {self.device}</h2>\n'
        for func in self.functions:
            html += func.get_electric()
        return html

    def get_complex(self):
        html = f'<h2>Комплексная проверка терминала {self.name} {self.device}</h2>\n'
        for func in self.functions:
            html += func.get_complex()
        return html

class CBASVAL(BaseModel):
    UBase: float = 132.0
    IBase: float = 3000
    SBase: float = 229.0

class TextEngine(ABC):

    def __init__(self):
        self.text = ''

    def h1(self, text: str):
        ...

    def h2(self, text: str):
        ...

    def h3(self, text: str):
        ...

    def h4(self, text: str):
        ...

    def p(self, text: str):
        ...

    def table_head(self, *args: str):
        ...

    def table_row(self, *args: str):
        ...

    def image(self, image_path: str):
        ...

    def result(self):
        return self.text