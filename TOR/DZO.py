import cmath
import math

from Function import Function


class DZO(Function):
    id_nach: int

    def __str__(self):
        return f'ДЗО Iднач={self.id_nach}'

    def get_electric(self):
        self.te.p(f'Уставка: {str(self)}')
        self.te.table_name('Проверка тормозных характеристик ДЗО')
        settings = [((0, self.id_nach * 2, self.id_nach * 4),
                     (self.id_nach, self.id_nach, self.id_nach * 2),
                     'Уставка'),]
        for case_test in self.tests:
            self.te.table_name(case_test[0])
            self.te.table_head('I1,A', 'I2,A', 'Iдиф,о.е.', 'Iторм,о.е.')
            d = []
            b = []
            for cs in case_test[4:]:
                i1 = cmath.rect(cs[0], math.radians(cs[1]))
                i2 = cmath.rect(cs[2], math.radians(cs[3]))
                dif, bias = self.calc_dif_bias(i1, i2, case_test[1], case_test[2], case_test[3])
                d.append(dif)
                b.append(bias)
                self.te.table_row(f'{cs[0]:.2f}A {cs[1]:.0f}°', f'{cs[2]:.2f} {cs[3]:.0f}°', f'{dif:.2f}', f'{bias:.2f}')
            check_points = [b, d, 'Измерено']
            check_points = [check_points]
            self.te.graph(settings=settings, check_points=check_points, xlabel='Iторм, %', ylabel='Iдиф, %',
                          title=case_test[0])

    def get_complex(self):
        if self.complex:
            for num in range(0, len(self.complex), 2):
                head = self.complex[num]
                table_name = f'ДЗЛ (DIFL) при I={head[0]} A'
                super().get_complex(table_name, num_stage=num + 1)

    @staticmethod
    def calc_dif_bias(i1: complex, i2: complex, dir: bool, k1: int, k2: int):
        i1 *= k1
        i2 *= k2
        if dir:
            dif = abs(i1 - i2) / 5
        else:
            dif = abs(i1 + i2) / 5
        bias = max(abs(i1), abs(i2)) / 5
        return dif, bias
