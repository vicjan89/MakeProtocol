from interfaces import Function


class TOC(Function):
    Operation: bool
    IP: float
    tP: float
    IN: float
    tN: float
    name: str

    def get_electric(self):
        self.te.table_name(self.name)
        self.te.table_head('Уставка Iср, A', 'Измерено Iср, A', 'Измерено Iвозвр, A', 'Kвозвр')
        self.te.table_row(self.IN * self.configuration["I1b"] / 100, self.tests[0], self.tests[1], f'{self.tests[1]/self.tests[0]:.2f}')

    def get_complex(self):
        ...
