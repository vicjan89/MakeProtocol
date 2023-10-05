from interfaces import Function


class DA(Function):
    name: str
    Operation: bool
    Histeres: int
    HiAlarm: int

    def get_electric(self):
       self.te.p(f'Iср={self.tests[0]} Iвозвр={self.tests[1]} Kвозвр={self.tests[1]/self.tests[0]:.2f}')


