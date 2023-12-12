from Function import Function

class PSD(Function):
    Operation: bool
    Detection: bool | None = None
    X1IN: float
    R1IN: float
    KX: int
    KR: int
    X1INp: float
    R1INp: float
    X1OUTp: float | None = None
    R1OUTp: float | None = None

    def add_context(self, **kwargs):
        super().add_context(**kwargs)
        if not self.X1OUTp:
            self.X1OUTp = self.X1INp * self.KX / 100
            self.R1OUTp = self.R1INp * self.KR / 100

    def get_electric(self):
        k = self.vt.kt / self.ct.kt
        self.te.p(f'Уставки первичные: R1внутр={self.R1INp} Ом, X1внутр={self.X1INp} Ом,'
                  f'R1внеш={self.R1OUTp} Ом, X1внеш={self.X1OUTp} Ом')
        self.te.p(f'Уставки вторичные: R1внутр={self.R1IN} Ом, X1внутр={self.X1IN} Ом,'
                  f'R1внеш={self.R1IN * self.KR / 100} Ом, X1внеш={self.X1IN * self.KX / 100} Ом')
        settings = []
        settings_in = self.get_points_charact_in()
        settings_in.append('Внутренняя характеристика')
        settings_out = self.get_points_charact_out()
        settings_out.append('Внешняя характеристика')
        settings.extend([settings_in, settings_out])
        check_points = self.tests
        check_points.append('Измерения внешней характеристики')
        self.te.table_name('Измерения внешней характеристики в режиме трёхфазного тока ABC')
        self.te.table_head('№', 'r, Ом', 'x, Ом', '№', 'r, Ом', 'x, Ом')
        l = len(check_points[0])
        i = 0
        row = []
        while i < l:
            row.extend([i+1, check_points[0][i], check_points[1][i]])
            if i % 2:
                self.te.table_row(*row)
                row = []
            i += 1
        self.te.graph_z(settings=settings, check_points=[check_points], title='PSD')


    def get_complex(self):
        ...

    def get_points_charact_in(self) -> list:
        r = (self.R1IN, self.R1IN, -self.R1IN, -self.R1IN, self.R1IN)
        x = (-self.X1IN, self.X1IN, self.X1IN, -self.X1IN, -self.X1IN)
        return [r, x]

    def get_points_charact_out(self) -> list:
        r, x = self.get_points_charact_in()
        r = list(map(lambda r: r * self.KR / 100, r))
        x = list(map(lambda x: x * self.KX / 100, x))
        return [r, x]