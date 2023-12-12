import cmath
import math

from Function import Function
from REL5__.GFC import GFC

class ZM(Function):
    Operation: str
    OperationPP: bool
    X1PP: float | None = None #secondary setting
    X1PPp: float | None = None #primary setting
    R1PP: float | None = None #secondary setting
    R1PPp: float | None = None #primary setting
    RFPP: float | None = None #secondary setting
    RFPPp: float | None = None #primary setting
    OperationPE: bool
    X1PE: float | None = None #secondary setting
    X1PEp: float | None = None #primary setting
    R1PE: float | None = None #secondary setting
    R1PEp: float | None = None #primary setting
    X0PE: float | None = None #secondary setting
    X0PEp: float | None = None #primary setting
    R0PE: float | None = None #secondary setting
    R0PEp: float | None = None #primary setting
    RFPE: float | None = None #secondary setting
    RFPEp: float | None = None #primary setting
    gfc: GFC | None = None

    def add_context(self, **kwargs):
        super().add_context(**kwargs)
        # calculate missing values
        error_text = 'discrepancy between primary and secondary values'
        error = 20 #error betwin setting primary and secondary in %
        k = self.vt.kt / self.ct.kt
        if self.X1PPp and self.X1PP:
            error_value = (self.X1PP * k - self.X1PPp) / self.X1PP * 100
            assert error_value < error, error_text + f'{error_value:.1f}%'
        if self.R1PPp and self.R1PP:
            error_value = (self.R1PP * k - self.R1PPp) / self.R1PP * 100
            assert error_value < error, error_text + f'{error_value:.1f}%'
        if self.RFPPp and self.RFPP:
            error_value = (self.RFPP * k - self.RFPPp) / self.RFPP * 100
            assert error_value < error, error_text + f'{error_value:.1f}%'
        if self.X1PEp and self.X1PE:
            error_value = (self.X1PE * k - self.X1PEp) / self.X1PE * 100
            assert error_value < error, error_text + f'{error_value:.1f}%'
        if self.R1PEp and self.R1PE:
            error_value = (self.R1PE * k - self.R1PEp) / self.R1PE * 100
            assert error_value < error, error_text + f'{error_value:.1f}%'
        if self.X0PEp and self.X0PE:
            error_value = (self.X0PE * k - self.X0PEp) / self.X0PE * 100
            assert error_value < error, error_text + f'{error_value:.1f}%'
        if self.R0PEp and self.R0PE:
            error_value = (self.R0PE * k - self.R0PEp) / self.R0PE * 100
            assert error_value < error, error_text + f'{error_value:.1f}%'
        if self.RFPEp and self.RFPE:
            error_value = (self.RFPE * k - self.RFPEp) / self.RFPE * 100
            assert error_value < error, error_text + f'{error_value:.1f}%'

        if self.X1PPp and not self.X1PP:
            self.X1PP = self.X1PPp / k
        if self.R1PPp and not self.R1PP:
            self.R1PP = self.R1PPp / k
        if self.RFPPp and not self.RFPP:
            self.RFPP = self.RFPPp / k
        if self.X1PEp and not self.X1PE:
            self.X1PE = self.X1PEp / k
        if self.R1PEp and not self.R1PE:
            self.R1PE = self.R1PEp / k
        if self.X0PEp and not self.X0PE:
            self.X0PE = self.X0PEp / k
        if self.R0PEp and not self.R0PE:
            self.R0PE = self.R0PEp / k
        if self.RFPEp and not self.RFPE:
            self.RFPE = self.RFPEp / k
        if not self.X1PPp and self.X1PP:
            self.X1PPp = self.X1PP * k
        if not self.R1PPp and self.R1PP:
            self.R1PPp = self.R1PP * k
        if not self.RFPPp and self.RFPP:
            self.RFPPp = self.RFPP * k
        if not self.X1PEp and self.X1PE:
            self.X1PEp = self.X1PE * k
        if not self.R1PEp and self.R1PE:
            self.R1PEp = self.R1PE * k
        if not self.X0PEp and self.X0PE:
            self.X0PEp = self.X0PE * k
        if not self.R0PEp and self.R0PE:
            self.R0PEp = self.R0PE * k
        if not self.RFPEp and self.RFPE:
            self.RFPEp = self.RFPE * k

    def get_electric(self, n: int):
        self.te.p(str(self))
        settings = []
        check_points = []
        if self.OperationPP:
            self.te.h4('От междуфазных КЗ')
            setting_2ph = self.get_points_charact_2ph()
            setting_2ph.append('Уставка от междуфазных КЗ')
            settings.append(setting_2ph)
        if self.OperationPE:
            self.te.h4('От однофазных КЗ')
            setting_1ph = self.get_points_charact_1ph()
            setting_1ph.append('Уставка от однофазных КЗ')
            settings.append(setting_1ph)
        for points in self.tests:
            if len(points) != 3: #TODO: то нужно преобразование из токов и напряжений в сопротивления реализовано для однофазных КЗ
                new_check_points = []
                for i in range(2):
                    new_check_points.append([])
                # Z0 = complex(self.R0PE, self.X0PE)
                # Z1 = complex(self.R1PE, self.X1PE)
                # Kn = (Z0 - Z1) / Z1 / 3
                new_check_points.append(points[-1])
                self.te.table_name(f'Измерения характеристики {n} ступени в режиме {points[-1]}')
                self.te.table_head('№', 'I, A', 'U, В', 'z, Ом', 'r, Ом', 'x, Ом')
                if points[-2] == '1ph':
                    for i in range(len(points[0])):
                        U = cmath.rect(points[2][i], math.radians(points[3][i]))
                        I = cmath.rect(points[0][i], math.radians(points[1][i]))
                        Z = U / I#TODO / (1 + Kn) просто подобрал, нужно продумать математику
                        new_check_points[0].append(Z.real)
                        new_check_points[1].append(Z.imag)
                        self.te.table_row(i+1, f'{points[0][i]} {points[1][i]}°', f'{points[2][i]} {points[3][i]}°',
                                          f'{abs(Z):.2f} {math.degrees(cmath.phase(Z)):.1f}°', f'{Z.real:.2f}', f'{Z.imag:.2f}')
                elif points[-2] == '2ph':
                    for i in range(len(points[0])):
                        U = cmath.rect(points[2][i], math.radians(points[3][i]))
                        I = cmath.rect(points[0][i], math.radians(points[1][i])) * 2
                        Z = U / I#TODO / (1 + Kn) просто подобрал, нужно продумать математику
                        new_check_points[0].append(Z.real)
                        new_check_points[1].append(Z.imag)
                        self.te.table_row(i+1, f'{points[0][i]} {points[1][i]}°', f'{points[2][i]} {points[3][i]}°',
                                          f'{abs(Z):.2f} {math.degrees(cmath.phase(Z)):.1f}°', f'{Z.real:.2f}', f'{Z.imag:.2f}')

                else:
                    raise ValueError('Тип повреждения должен быть 1ph или 2ph')
                points = new_check_points
            else:
                self.te.table_name(f'Измерения характеристики {n} ступени в режиме {points[2]}')
                self.te.table_head('№', 'r, Ом', 'x, Ом', '№', 'r, Ом', 'x, Ом')
                l = len(points[0])
                i = 0
                row = []
                while i < l:
                    row.extend([i+1, f'{points[0][i]:.3f}', f'{points[1][i]:.3f}'])
                    if i % 2:
                        self.te.table_row(*row)
                        row = []
                    i += 1
            check_points.append(points)
        setting_gfc_2ph = self.gfc.get_point_charact_2ph()
        setting_gfc_2ph.append('GFC междуфазн.')
        setting_gfc_1ph = self.gfc.get_point_charact_1ph()
        setting_gfc_1ph.append('GFC однофазн.')
        self.te.graph_z(settings=settings, check_points=check_points, title=f'{n} ступень дистанционной защиты',
                        settings_unlim=(setting_gfc_2ph, setting_gfc_1ph))

    def get_complex(self, n: int):
        if self.complex:
            table_name = f'{n} ступень дистанционной защиты при r={self.complex[0][0]} Ом x={self.complex[0][1]} Ом вид ' \
                         f'КЗ {self.complex[0][2]}'
            super().get_complex(table_name)

    def trip(self, z: complex, ph1: bool = False): #TODO: реализовать однофазные КЗ
        phi = math.degrees(cmath.phase(z))
        if phi < 0:
            phi += 360
        if ((phi < 115 or phi > 345) and self.Operation == 'Forward') or ((165 < phi < 295) and self.Operation == 'Reverse'):
            p = z.imag / self.X1PP
            if -self.X1PP < z.imag < self.X1PP:
                r = self.R1PP * p
                if r - self.RFPP / 2 < z.real < r + self.RFPP / 2:
                        return True
        else:
            return False
        return False


    def search_2ph_points(self):
        end = 0
        start = math.sqrt((self.X1PP ** 2 + (self.R1PP + self.RFPP/2) ** 2))  * 1.1
        step = (start - end) / 200
        f = 0
        end_f = 2 * cmath.pi
        step_f = cmath.pi / 200
        while f < end_f:
            z = start
            while not self.trip(cmath.rect(z, f)):
                z -= step
                if z < end:
                    break
            yield cmath.rect(z, f)
            f += step_f

    def get_points_charact_2ph(self) -> list:
        s = math.sin(math.radians(15))
        r = self.RFPP*self.X1PP/2/self.R1PP/(self.X1PP/self.R1PP + s)
        x = -r * s
        z = math.sqrt(r ** 2 + x ** 2)
        phi = math.degrees(math.atan(x/r))
        r2 = self.R1PP + self.RFPP / 2
        x2 = self.X1PP
        tan25 = math.tan(math.radians(25))
        r4 = - self.RFPP * self.X1PP / 2 / self.R1PP / (self.X1PP / self.R1PP + 1 / tan25)
        x4 = - r4 / tan25
        if x4 <= self.X1PP:
            x3 = self.X1PP
            r3 =  self.R1PP - self.RFPP / 2
        else:
            x3 = x4 = self.X1PP
            r3 = r4 = - self.X1PP * tan25
        rm = (r, r2, r3, r4, 0, r)
        im = (x, x2, x3, x4, 0, x)
        if self.Operation == 'Reverse':
            rm = tuple(map(lambda x: -x, rm))
            im = tuple(map(lambda x: -x, im))
        return [rm, im]

    def get_points_charact_1ph(self) -> list:
        if self.OperationPE:
            sin15 = math.sin(math.radians(15))
            rpe = self.R1PE + (self.R0PE - self.R1PE) / 3
            xpe = self.X1PE + (self.X0PE - self.X1PE) / 3
            x = - self.RFPE / (rpe  / self.X1PE + 1 / sin15)
            r = - x / sin15
            r2 = rpe + self.RFPE
            x2 = xpe
            tan25 = math.tan(math.radians(25))
            r4 = - self.RFPE / (1 + rpe * tan25 / self.X1PE)
            x4 = - r4 / tan25
            if x4 <= self.X1PP:
                x3 = xpe
                r3 =  (self.R1PE + (self.R0PE - self.R1PE) / 3) * xpe / self.X1PE - self.RFPE
            else:
                x3 = x4 = xpe
                r3 = r4 = - xpe * tan25
            rm = (r, r2, r3, r4, 0, r)
            im = (x, x2, x3, x4, 0, x)
            if self.Operation == 'Reverse':
                rm = tuple(map(lambda x: -x, rm))
                im = tuple(map(lambda x: -x, im))
            return [rm, im]
        else:
            return [(0,), (0,)]

    @staticmethod
    def get_points_charact_str(data: tuple):
        if data == ((0,), (0,)):
            return 'Выведено\n'
        (r, r2, r3, r4, _, _), (x, x2, x3, x4, _, _) = data
        return f'1: {r:.3f} + j{x:.3f} / {math.sqrt(r ** 2 + x ** 2):.3f} Ом {math.degrees(math.atan(x/r)):.1f}гр\n' \
               f'2: {r2:.3f} + j{x2:.3f} / {math.sqrt(r2 ** 2 + x2 ** 2):.3f} Ом {math.degrees(math.atan(x2/r2)):.1f}гр\n' \
               f'3: {r3:.3f} + j{x3:.3f} / {math.sqrt(r3 ** 2 + x3 ** 2):.3f} Ом {math.degrees(math.atan(x3/r3)) + 180:.1f}гр\n' \
               f'4: {r4:.3f} + j{x4:.3f} / {math.sqrt(r4 ** 2 + x4 ** 2):.3f} Ом {math.degrees(math.atan(x4/r4)) + 180:.1f}гр\n'

    def get_points_charact_2ph_str(self):
        return self.get_points_charact_str(self.get_points_charact_2ph())

    def get_points_charact_1ph_str(self):
        return self.get_points_charact_str(self.get_points_charact_1ph())

    def __str__(self):
        # r = self.R1PE + (self.R0PE - self.R1PE) / 3
        # x = self.X1PE + (self.X0PE - self.X1PE) / 3
        # k0 = complex(self.R0PE, self.X0PE)/complex(self.R1PE, self.X1PE)
        s = ''
        if self.OperationPP:
            s += f'Уставка междуфазных КЗ первичных Z={self.R1PPp:.3f}+j{self.X1PPp:.3f} Ом RFPP={self.RFPPp:.3f} Ом, ' \
                 f'вторичныx Z={self.R1PP:.3f}+j{self.X1PP:.3f} Ом RFPP={self.RFPP:.3f} Ом, '
        if self.OperationPE:
            s += f'Уставка однофазных КЗ первичных Z0={self.R0PEp:.3f}+j{self.X0PEp:.3f} Ом ' \
                 f'Z1={self.R1PEp:.3f}+j{self.X1PEp:.3f} Ом RFPE={self.RFPEp:.3f} Ом, ' \
                     f'вторичныx Z0={self.R0PE:.3f}+j{self.X0PE:.3f} Ом ' \
                 f'Z1={self.R1PE:.3f}+j{self.X1PE:.3f} Ом RFPE={self.RFPE:.3f} Ом'
        return s