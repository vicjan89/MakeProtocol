from pydantic import field_validator


from interfaces import Function
from interfaces import CBASVAL


class ROV2PTOV(Function):
    Global_base_values: list[CBASVAL]
    INSTNAME: str = ''
    U3P: dict
    GlobalBaseSel: int
    OperationStep1: bool = False
    U1: int = 1
    t1: float = 0
    HystAbs1: float = 0
    OperationStep2: bool = False
    U2: int = 1
    t2: float = 0
    HystAbs2: float = 0

    @field_validator('U1')
    @classmethod
    def validate_U1(cls, v: int):
        assert 1 <= v <= 200, 'Значение должно быть в диапазоне от 1 до 200'
        return v

    @field_validator('U2')
    @classmethod
    def validate_U2(cls, v: int):
        assert 1 <= v <= 100, 'Значение должно быть в диапазоне от 1 до 100'
        return v

    @field_validator('t1')
    @classmethod
    def validate_t1(cls, v: float):
        assert 0.0 <= v <= 6000.0, 'Значение должно быть в диапазоне от 0.0 до 6000.0'
        return v

    @field_validator('t2')
    @classmethod
    def validate_t2(cls, v: float):
        assert 0.0 <= v <= 60.0, 'Значение должно быть в диапазоне от 0.0 до 60.0'
        return v

    @field_validator('HystAbs1', 'HystAbs2')
    @classmethod
    def validate_HystAbs(cls, v: float):
        assert 0.0 <= v <= 100.0, 'Значение должно быть в диапазоне от 0.0 до 100.0'
        return v

    def set_U(self, u: int):
        value = (u * self.Global_base_values[self.GlobalBaseSel-1].UBase / 300) + 0j
        self.analog_inputs[self.U3P['num']].channels[self.U3P['ch']-1].v_prim = value


    def get_electric(self):
        self.te.h3(f'Проверка функции {self.INSTNAME} ROV2PTOV')
        for num, stage in enumerate(((self.OperationStep1, self.U1, self.t1), (self.OperationStep2, self.U2, self.t2))):
            if stage[0]:
                self.te.h4(f'Проверка напряжения срабатывания и возврата {num+1} ступени функции')
                self.te.table_name()
                self.te.table_head('Уставка', 'Uср,А', 'Отклонение %', 'Uв, А', 'Кв')
                self.set_U(stage[1])
                ust = abs(self.analog_inputs[self.U3P["num"]].channels[self.U3P["ch"]-1].v_sec)
                self.te.table_row(f'{ust:.1f}', f'{self.tests[num]["result_u"][0]}',
                        f'{(self.tests[num]["result_u"][0] - ust)/ust*100:.2f}',
                        f'{self.tests[num]["result_u"][1]}',
                        f'{self.tests[num]["result_u"][1]/self.tests[num]["result_u"][0]:.2f}')

    def get_complex(self):
        self.te.h3(f'Проверка функции {self.INSTNAME} ROV2PTOV')
        for num, stage in enumerate(((self.OperationStep1, self.U1, self.t1), (self.OperationStep2, self.U2, self.t2))):
            if stage[0]:
                self.set_U(stage[1])
                ust = abs(self.analog_inputs[self.U3P["num"]].channels[self.U3P["ch"]-1].v_sec)
                self.te.h4(f'Комплексная проверка {num+1} ступени функции при напряжении {ust*1.1:.1f} В')
                self.te.table_name()
                self.te.table_head('Время, сек', 'Сработавший контакт')
                t_contact: float
                for num, t_contact in enumerate(self.tests[num]['result_complex']):
                    t = f'{t_contact:.3f}' if t_contact else 'Не сработал'
                    self.te.table_row(f'{t}', f'{self.contacts[num]}')
                self.te.p(f'При напряжении {ust * 0.9:.1f} В не срабатывает.')