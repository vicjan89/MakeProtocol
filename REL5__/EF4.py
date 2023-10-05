import math

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
    INDir: int
    configuration: dict | None = None

    def get_electric(self):
        self.te.h4('Уставки')
        self.te.p(self.__str__())
        self.te.table_name('Схема подключения проверочного устройства')
        self.te.table_head('Выход РЕТОМ', 'Вход шкафа РЗА', 'Выход РЕТОМ', 'Вход шкафа РЗА')
        self.te.table_row('Uc', 'H611', 'Un', 'B600')
        self.te.table_row('Ia', 'A4xx', 'In', 'N4xx')
        self.te.p('Напряжение проверочного устройства Uc (3U0) подано 57 В 0°. Ток 3I0 = - Ia.')
        IN = (self.IN1, self.IN2, self.IN3, self.IN4)
        for n, c in enumerate(self.tests):
            self.te.h4(f'{n+1} ступень')
            self.te.table_name(f'Проверка {n+1} ступени')
            self.te.table_head('F1 Ia,°', 'F2 Ia,°', 'Iср,А', 'Iвозвр,А', 'I проверки Fмч, A', 'F1 3I0,°', 'F2 3I0°', 'Kв', 'Fмч,°')
            f = (c[1] + c[0]) / 2 + 180
            f13i0 = c[0] + 180
            if f13i0 > 360:
                f13i0 -= 360
            f23i0 = c[1] + 180
            if f23i0 > 360:
                f23i0 -= 360
            self.te.table_row(*c, f13i0, f23i0, f'{c[3]/c[2]:.2f}', f'{f:.1f}')
            arccos = math.degrees(math.acos(self.INDir * self.configuration['I1b'] / 100 / c[4]))
            f2 = 295 + arccos
            f2 = f2 if f2 <= 360 else f2 - 360
            in1 = IN[n] * self.configuration['I1b'] / 100
            self.te.graph_vector([(c[4], f13i0, 'F1'), #F1
                                  (c[4], f23i0, 'F2'), #F2
                                  (c[2], f, 'Fмч'),    #Fмч
                                  (c[4], 295 - arccos, self.INDir * self.configuration['I1b'] / 100, 295, c[4], f2, 'STFW'),
                                  (c[4], 0, 'Uc=3U0')])


    def get_complex(self):
        if self.complex:
            for num in range(0, len(self.complex), 2):
                head = self.complex[num]
                table_name = f'{head[3]} ступень НТЗНП при I={head[0]} A ' \
                             f'U={head[1]} В угол напряжения {head[2]}°'
                super().get_complex(table_name, num_stage=num + 1)

    def __str__(self):
        return f'Step1 {self.Step1}, IN1> {self.IN1}, t1 {self.t1}, Step2 {self.Step2}, IN2> {self.IN2}, t2 {self.t2}, ' \
               f'Step3 {self.Step3}, IN3> {self.IN3}, t3 {self.t3}, Step4 {self.Step4}, Characteristic {self.Characteristic},' \
               f' IN>inv {self.INgtinv}, k {self.k}, IN4 {self.IN4}, t4 {self.t4}'

