from textengines.interfaces import TextEngine


from interfaces import Terminal
from RE_5__.GFC import GFC
from RE_5__.ZM import ZM
from RE_5__.PSD import PSD
from RE_5__.FUSE import FUSE
from RE_5__.EF4 import EF4

class REL511(Terminal):
    mode: str | None = None
    configuration: dict
    gfc: GFC
    zm1: ZM
    zm2: ZM
    zm3: ZM
    zm4: ZM
    zm5: ZM
    psd: PSD
    fuse: FUSE
    ef4: EF4

    def get_electric(self):
        self.te.h2(f'Проверка терминала {self.name} REF511')
        if self.mode:
            self.te.p(self.mode)
        if self.gfc.Operation:
            self.gfc.get_electric()
        self.te.h3('Проверка функции блокировки при неисправности цепей напряжения')
        self.fuse.get_electric()
        if self.psd.Operation:
            self.te.h3('Проверка функции блокировки от качаний')
            self.psd.get_electric()
        if self.zm1.Operation:
            self.te.h3('Проверка первой ступени дистанционной защиты')
            self.zm1.get_electric()
        if self.zm2.Operation:
            self.te.h3('Проверка второй ступени дистанционной защиты')
            self.zm2.get_electric()
        if self.zm3.Operation:
            self.te.h3('Проверка третьей ступени дистанционной защиты')
            self.zm3.get_electric()
        if self.zm4.Operation:
            self.te.h3('Проверка четвёртой ступени дистанционной защиты')
            self.zm4.get_electric()
        if self.zm5.Operation:
            self.te.h3('Проверка пятой ступени дистанционной защиты')
            self.zm5.get_electric()
        if self.ef4.Operation:
            self.te.h3('Проверка НТЗНП')
            self.ef4.get_electric()

    def get_complex(self):
        self.te.h2(f'Комплексная проверка терминала {self.name} REF511')
        if self.gfc.Operation:
            self.gfc.get_complex()

    def add_te(self, te: TextEngine):
        super().add_te(te)
        self.gfc.add_te(te)
        self.psd.add_te(te)
        self.zm1.add_te(te)
        self.zm2.add_te(te)
        self.zm3.add_te(te)
        self.zm4.add_te(te)
        self.zm5.add_te(te)
        self.fuse.add_te(te)
        self.fuse.configuration = self.configuration
        self.ef4.add_te(te)
        self.ef4.configuration = self.configuration

