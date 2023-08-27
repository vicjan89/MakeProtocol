from cmath import rect, pi


from pydantic import field_validator


from interfaces import Function, CBASVAL


class FUFSPVC(Function):
    INSTNAME: str
    Global_base_values: list[CBASVAL]
    GlobalBaseSel: int
    I3P: dict
    U3P: dict
    OpMode: str = 'UZsIZs'
    gt3U0: int
    lt3I0: int
    gtU2: int
    ltI2: int
    OpDUDI: bool
    DUgt: int
    DIlt: int
    UPhgt: int
    IPhgt: int
    SealIn: bool
    USealInlt: int
    IDLDlt: int
    UDLDlt: int

    @field_validator('OpMode')
    @classmethod
    def validate_OpMode(cls, v: str):
        assert v in ('UZsIZs', 'UZsIZs OR UNsINs'), 'Значение должно быть одним из UZsIZs, UZsIZs OR UNsINs'
        return v

    def set_3U0(self, v: int):
        '''
        Устанавливает аналоговые входа в соответствие с уставкой 3U0
        :param v: уставка в % от UBase
        '''
        k = self.Global_base_values[self.GlobalBaseSel-1].UBase
        self.analog_inputs[self.U3P['num']].channels[self.U3P['u0']-1].v_prim = v * k / 300

    def get_3U0(self):
        return self.analog_inputs[self.U3P["num"]].channels[self.U3P["u0"] - 1].v_sec

    def set_3I0(self, v: int):
        '''
        Устанавливает аналоговые входа в соответствие с уставкой 3I0
        :param v: уставка в % от IBase
        '''
        k = self.Global_base_values[self.GlobalBaseSel - 1].IBase
        self.analog_inputs[self.I3P['num']].channels[self.I3P['l1'] - 1].v_prim = v * k / 300 + 0j
        self.analog_inputs[self.I3P['num']].channels[self.I3P['l2'] - 1].v_prim = v * k / 300 + 0j
        self.analog_inputs[self.I3P['num']].channels[self.I3P['l3'] - 1].v_prim = v * k / 300 + 0j

    def get_3I0(self):
        l1 = self.analog_inputs[self.I3P['num']].channels[self.I3P['l1'] - 1].v_sec
        l2 = self.analog_inputs[self.I3P['num']].channels[self.I3P['l2'] - 1].v_sec
        l3 = self.analog_inputs[self.I3P['num']].channels[self.I3P['l3'] - 1].v_sec
        _3i0 = l1 + l2 + l3
        return _3i0

    def set_3U2(self, v: int):
        k = self.Global_base_values[self.GlobalBaseSel - 1].UBase
        self.analog_inputs[self.U3P['num']].channels[self.U3P['l1'] - 1].v_prim = v * k / 300 + 0j
        self.analog_inputs[self.U3P['num']].channels[self.U3P['l2'] - 1].v_prim = rect(v * k / 300, 2*pi/3)
        self.analog_inputs[self.U3P['num']].channels[self.U3P['l3'] - 1].v_prim = rect(v * k / 300, 4*pi/3)

    def get_3U2(self):
        a = rect(1, 2*pi/3)
        a2 = rect(1, 4*pi/3)
        l1 = self.analog_inputs[self.U3P['num']].channels[self.U3P['l1'] - 1].v_sec
        l2 = self.analog_inputs[self.U3P['num']].channels[self.U3P['l2'] - 1].v_sec
        l3 = self.analog_inputs[self.U3P['num']].channels[self.U3P['l3'] - 1].v_sec
        _3u2 = l1 + l2*a2 + l3*a
        return _3u2

    def set_3I2(self, v: int):
        k = self.Global_base_values[self.GlobalBaseSel - 1].IBase
        self.analog_inputs[self.I3P['num']].channels[self.I3P['l1'] - 1].v_prim = v * k / 300 + 0j
        self.analog_inputs[self.I3P['num']].channels[self.I3P['l2'] - 1].v_prim = rect(v * k / 300, 2 * pi / 3)
        self.analog_inputs[self.I3P['num']].channels[self.I3P['l3'] - 1].v_prim = rect(v * k / 300, 4 * pi / 3)

    def get_3I2(self):
        a = rect(1, 2 * pi / 3)
        a2 = rect(1, 4 * pi / 3)
        l1 = self.analog_inputs[self.I3P['num']].channels[self.I3P['l1'] - 1].v_sec
        l2 = self.analog_inputs[self.I3P['num']].channels[self.I3P['l2'] - 1].v_sec
        l3 = self.analog_inputs[self.I3P['num']].channels[self.I3P['l3'] - 1].v_sec
        _3i2 = l1 + l2 * a2 + l3 * a
        return _3i2

    def get_electric(self):
        self.te.h3(f'Проверка функции {self.INSTNAME} FUFSPVC')
        self.te.h4('Проверка напряжения срабатывания и возврата контроля нулевой последовательности')
        self.te.table_head('Уставка', '3U0ср,В', 'Отклонение %', '3U0в, В', 'Кв')
        self.set_3U0(self.gt3U0)
        ust = abs(self.get_3U0())
        self.te.table_row(f'{ust:.1f}', f'{self.tests["result_3u0"][0]}', f'{(self.tests["result_3u0"][0] - ust)/ust*100:.2f}',
                f'{self.tests["result_3u0"][1]}', f'{self.tests["result_3u0"][1]/self.tests["result_3u0"][0]:.2f}')

        self.te.h4('Проверка тока срабатывания и возврата контроля нулевой последовательности')
        self.te.table_head('Уставка', '3I0ср,А', 'Отклонение %', '3I0в, А', 'Кв')
        self.set_3I0(self.lt3I0)
        ust = abs(self.get_3I0())
        self.te.table_row(f'{ust:.3f}', f'{self.tests["result_3i0"][0]:.3f}', f'{(self.tests["result_3i0"][0] - ust) / ust * 100:.2f}',
                f'{self.tests["result_3i0"][1]:.3f}', f'{self.tests["result_3i0"][1] / self.tests["result_3i0"][0]:.2f}')

        self.te.h4('Проверка напряжения срабатывания и возврата контроля обратной последовательности')
        self.te.table_head('Уставка', '3U2ср,В', 'Отклонение %', '3U2в, В', 'Кв')
        self.set_3U2(self.gtU2)
        ust = abs(self.get_3U2())
        self.te.table_row(f'{ust:.1f}', f'{self.tests["result_3u2"][0]}', f'{(self.tests["result_3u2"][0] - ust) / ust * 100:.2f}',
                f'{self.tests["result_3u2"][1]}', f'{self.tests["result_3u2"][1] / self.tests["result_3u2"][0]:.2f}')

        self.te.h4('Проверка тока срабатывания и возврата контроля обратной последовательности')
        self.te.table_head('Уставка', '3I2ср,А', 'Отклонение %', '3I2в, А', 'Кв')
        self.set_3I2(self.ltI2)
        ust = abs(self.get_3I2())
        self.te.table_row(f'{ust:.3f}', f'{self.tests["result_3i2"][0]:.3f}',
                f'{(self.tests["result_3i2"][0] - ust) / ust * 100:.2f}',
                f'{self.tests["result_3i2"][1]:.3f}',
                f'{self.tests["result_3i2"][1] / self.tests["result_3i2"][0]:.2f}')
        self.te.p(self.tests.get('note', ''))

    def get_complex(self):
        return ''