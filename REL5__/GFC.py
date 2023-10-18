import cmath
import math


from Function import Function


class GFC(Function):
    Operation: bool
    OperationZlt: bool
    OperationIgt: bool
    ARGLd: int
    RLd: float
    X1RvPP: float
    X1FwPP: float
    RFPP: float
    IPgt: int
    Timer_tPP: bool
    tPP: float
    X1RvPE: float
    X1FwPE: float
    X0FwPE: float
    X0RvPE: float
    RFPE: float
    INgt: int
    Timer_tPE: bool
    tPE: float
    INReleasePE: int
    INBlockPP: int

    def get_electric(self):
        ...

    def get_complex(self):
        ...

    def trip(self, z: complex):
        if -self.X1RvPP < z.imag < self.X1FwPP:
            phi = math.degrees(cmath.phase(z))
            if self.ARGLd < phi < 90 or (self.ARGLd + 180) < phi < 270:
                if abs(z.real) < self.RFPP / 2:
                    return True
            else:
                if abs(z.real) < self.RLd / 2:
                    return True
        return False

    def get_2ph_points(self):
        end = min((self.X1FwPP, self.X1RvPP, self.RFPP/2, self.RLd/2)) * 0.9
        start = math.sqrt(max((self.X1FwPP, self.X1RvPP, self.RFPP/2, self.RLd/2)) ** 2 * 2) * 1.1
        step = (start - end) / 3000
        f = 0
        end_f = 2 * cmath.pi
        step_f = cmath.pi / 600
        while f < end_f:
            z = start
            while not self.trip(cmath.rect(z, f)):
                z -= step
                if z < end:
                    break
            yield cmath.rect(z, f)
            f += step_f


    def get_1ph_points(self):
        end = min((self.X1FwPP, self.X1RvPP, self.RFPP / 2, self.RLd / 2)) * 0.9
        start = math.sqrt(max((self.X1FwPP, self.X1RvPP, self.RFPP / 2, self.RLd / 2)) ** 2 * 2) * 1.1
        step = (start - end) / 3000
        f = 0
        end_f = 2 * cmath.pi
        step_f = cmath.pi / 600
        while f < end_f:
            z = start
            while self.trip(cmath.rect(z, f)):
                z -= step
                if z < end:
                    print('Точка не найдена')
                    break
            yield cmath.rect(z, f)
            f += step_f

    def get_point_charact_2ph(self):
        r = []
        x = []
        for point in self.get_2ph_points():
            r.append(point.real)
            x.append(point.imag)
        return [r, x]


    def get_point_charact_1ph(self):
        r = []
        x = []
        for point in self.get_1ph_points():
            r.append(point.real)
            x.append(point.imag)
        return [r, x]
