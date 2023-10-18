from Function import Function


class DA(Function):
    name: str
    Operation: bool
    Histeres: int
    HiAlarm: int #primary value in amper

    def get_electric(self):
        self.te.p(f'Уставка: {self.HiAlarm}A первичных или {self.ct.p2s(self.HiAlarm):.2f}A вторичных')
        self.te.p(f'Iср={self.tests[0]} Iвозвр={self.tests[1]} Kвозвр={self.tests[1]/self.tests[0]:.2f}')


