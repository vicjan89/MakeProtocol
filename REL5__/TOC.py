from Function import Function


class TOC(Function):
    Operation: bool
    IP: float # in % from I1b
    tP: float
    nameP: str | None = None
    IN: float # in % from I4b
    tN: float
    nameN: str | None = None

    def get_electric(self):
        head = ('Уставка первич Iср, А', 'Уставка Iср, A', 'Измерено Iср, A', 'Измерено Iвозвр, A', 'Kвозвр')
        if self.tP < 30:
            self.te.h3(f'Проверка функции: {self.nameP}')
            self.te.table_name(self.nameP)
            self.te.table_head(*head)
            i = self.IP * self.configuration["I1b"] / 100
            self.te.table_row(f'{self.ct.s2p(i):.0f}', i, self.tests['P'][0], self.tests['P'][1],
                              f'{self.tests["P"][1]/self.tests["P"][0]:.2f}')
        if self.tN < 30:
            self.te.h3(f'Проверка функции: {self.nameN}')
            self.te.table_name(self.nameN)
            self.te.table_head(*head)
            i = self.IN * self.configuration["I4b"] / 100
            self.te.table_row(f'{self.ct.s2p(i):.0f}', i, self.tests['N'][0], self.tests['N'][1],
                              f'{self.tests["N"][1]/self.tests["N"][0]:.2f}')

    def get_complex(self):
        ...
