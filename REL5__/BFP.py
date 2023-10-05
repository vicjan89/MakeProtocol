from pydantic import field_validator


from interfaces import Function


class BFP(Function):
    Operation: bool
    IP: float
    t2: float
    RetripType: str
    t1: float

    @field_validator('RetripType')
    @classmethod
    def validate_retrip_type(cls, v: str):
        if v not in ('Retrip Off', 'I> Check', 'No I> Check'):
            raise ValueError('RetripType not valid')
        return v

    def get_electric(self):
        self.te.table_name('BFP')
        self.te.table_head('Уставка tср на себя', 'Измерено tср на себя', 'Уставка tср на внешние',
                           'Измерено tср на внешние')
        self.te.table_row(self.t1, self.tests[0], self.t2, self.tests[1])

    def get_complex(self):
        if self.complex:
            head = self.complex[0]
            table_name = f'Проверка УРОВ после работы защиты:{head[3]} при I={head[0]} A ' \
                         f'U={head[1]} В угол напряжения {head[2]}°'
            super().get_complex(table_name)
