from interfaces import element


class VT(element):
    up: int
    us1: int
    us2: int | None = None
    us3: int | None = None
    tests: list | None = None

    def get_electric(self):
        self.te.h2('Проверка трансформаторов напряжения')

    def get_complex(self):
        ...

    def s2p(self, value: float) -> float:
        return value / self.us1 * self.up

    @property
    def kt(self):
        return self.up / self.us1
