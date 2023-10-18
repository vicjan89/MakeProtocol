import cmath


from Function import Function


class FUSE(Function):
    NegativeSeq: bool
    gt3U2: float
    lt3I2: float
    dUdI: bool
    Igt: float
    DUgt: float
    DIlt: float
    configuration: dict | None = None

    def get_electric(self):
        if self.NegativeSeq:
            self.te.h4('Проверка срабатывания по обратной последовательности')
            u2 = abs(cmath.rect(self.tests[0], 0) + cmath.rect(57, cmath.pi * 2 / 3) + cmath.rect(57, cmath.pi * 4 / 3))
            self.te.p(f'Подали трёхфазное напряжение прямой последовательности 57 В и начали снижать напряжение фазы'
                      f'А до срабатывания фанкции. Срабатывание произошло при Ua={self.tests[0]}В 0° Ub=57В 240° Uc=57В'
                      f' 120° что соответствует напряжению обратной последовательности 3U2 равному {u2:.2f}В что составляет '
                      f'{u2 / self.configuration["U1b"] * 100:.2f}% от U1b.')
            self.te.h4('Проверка блокировки по току обратной последовательности')
            self.te.p(f'При сработанной функции по напряжению обратной последовательности начали повышать ток обратной '
                      f'последовательности. Функция вернулась в несработанное состояние при токе обратной '
                      f'последовательности I2 {self.tests[1]}A (3I2={3 * self.tests[1]}A) что составляет '
                      f'{3 * self.tests[1] / self.configuration["I1b"] * 100:.2f}% от I1b.')

    def get_complex(self):
        ...
