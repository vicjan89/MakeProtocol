from interfaces import Function


class EF4(Function):
    Operation: bool
    Step1: str
    IN1: int
    t1: float
    Step2: str
    IN2: int
    t2: float
    Step3: str
    IN3: int
    t3: float
    Step4: str
    Characteristic: str
    INgtinv: int
    k: float
    IN4: int
    t4: float
    configuration: dict | None = None

    def get_electric(self):
        self.te.h3('Уставки')
        self.te.p(self.__str__())
        for n, c in enumerate(self.tests):
            self.te.h3(f'{n+1} ступень')
            self.te.table_name(f'Проверка {n+1} ступени')
            self.te.table_head('F1,°', 'F2,°', 'Iср,А', 'Iвозвр,А', 'Kв', 'Fмч,°')
            self.te.table_row(*c, f'{c[3]/c[2]:.2f}', f'{(c[0] - c[1]) / 2 - 180:.1f}')


    def get_complex(self):
        ...

    def __str__(self):
        return f'Step1 {self.Step1}, IN1> {self.IN1}, t1 {self.t1}, Step2 {self.Step2}, IN2> {self.IN2}, t2 {self.t2}, ' \
               f'Step3 {self.Step3}, IN3> {self.IN3}, t3 {self.t3}, Step4 {self.Step4}, Characteristic {self.Characteristic},' \
               f' IN>inv {self.INgtinv}, k {self.k}, IN4 {self.IN4}, t4 {self.t4}'

