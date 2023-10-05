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
        settings.append([0, self.IminOp * self.CTFactor * self.configuration['']])

    def get_complex(self, table_name: str):
        ...