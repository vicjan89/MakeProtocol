import cmath
import math

from interfaces import Function


class DIFL(Function):
    Operation: bool
    CTFactor: float
    IMinSat: int
    IminOp: int
    IDiffLvl1: int
    IDiffLvl2: int
    ILvl1_2Cross: int
    Evaluate: str

    def get_electric(self):
        self.te.p('Перевести терминал в режим теста с разблокированной функцией DIFL')
        settings = []
        k = self.CTFactor * self.configuration['I1b']
        b2 = self.ILvl1_2Cross * k / 100
        settings.append([0, self.IminOp * k / self.IDiffLvl1, b2, b2 * 1.5])
        d0 = self.IminOp * k / 100
        d2 = b2 * self.IDiffLvl1 / 100
        settings.append([d0, d0, d2, d2 + 0.5 * b2 * self.IDiffLvl2 / 100])
        settings.append('DIFL')
        settings = [settings]
        d = []
        b = []
        self.te.table_name('Проверка тормозной характеристики ДЗЛ в режиме DiffTestMode=ReleaseLocal')
        self.te.table_head('Ia,A', 'Ib,A', 'Ic,A', 'Idif_a,A', 'Ibias_a', 'Idif_b,A', 'Ibias_b', 'Idif_c,A', 'Ibias_c',)
        for cs in self.tests:
            i1a = cmath.rect(cs[0], math.radians(cs[1]))
            i1b = cmath.rect(cs[2], math.radians(cs[3]))
            i1c = cmath.rect(cs[4], math.radians(cs[5]))
            dif_a, dif_b, dif_c, bias_a, bias_b, bias_c = self.calc_dif_bias(i1a, i1b, i1c, i1c, i1a, i1b)
            if dif_a > 0.9 * d0:
                d.append(dif_a)
                b.append(bias_a)
            self.te.table_row(f'{cs[0]} {cs[1]}°', f'{cs[2]} {cs[3]}°', f'{cs[4]} {cs[5]}°', f'{dif_a:.2f}',
                              f'{bias_a:.2f}', f'{dif_b:.2f}', f'{bias_b:.2f}', f'{dif_c:.2f}', f'{bias_c:.2f}')
        check_points = [b, d, 'Измерено']
        check_points = [check_points]
        self.te.graph_dif(settings, check_points=check_points, title='Характеристика ДЗЛ (DIFL)')

    def get_complex(self):
        if self.complex:
            for num in range(0, len(self.complex), 2):
                head = self.complex[num]
                table_name = f'ДЗЛ (DIFL) при I={head[0]} A'
                super().get_complex(table_name, num_stage=num + 1)

    @staticmethod
    def calc_dif_bias(i1a: complex, i1b: complex, i1c: complex, i2a: complex, i2b: complex, i2c: complex):
        dif_a = abs(i1a + i2a)
        dif_b = abs(i1b + i2b)
        dif_c = abs(i1c + i2c)
        _bias_a = (abs(i1a) + abs(i2a)) / 2
        _bias_b = (abs(i1b) + abs(i2b)) / 2
        _bias_c = (abs(i1c) + abs(i2c)) / 2
        bias_a = max(_bias_a, _bias_b / 2, _bias_c /2)
        bias_b = max(_bias_b, _bias_a / 2, _bias_c /2)
        bias_c = max(_bias_c, _bias_b / 2, _bias_a /2)
        return dif_a, dif_b, dif_c, bias_a, bias_b, bias_c
