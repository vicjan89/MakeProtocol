from interfaces import Terminal
from REL5__.GFC import GFC
from REL5__.ZM import ZM
from REL5__.PSD import PSD
from REL5__.FUSE import FUSE
from REL5__.EF4 import EF4
from REL5__.BFP import BFP
from REL5__.TOC import TOC
from REL5__.DA import DA

class REL5__(Terminal):
    mode: str | None = None
    configuration: dict
    calibration: list
    gfc: GFC | None = None
    zm1: ZM | None = None
    zm2: ZM | None = None
    zm3: ZM | None = None
    zm4: ZM | None = None
    zm5: ZM | None = None
    psd: PSD | None = None
    fuse: FUSE | None = None
    ef4: EF4 | None = None
    bfp: BFP | None = None
    toc: TOC | None = None
    da06: DA | None = None
    da07: DA | None = None
    da08: DA | None = None
    contacts: list | None = None

    def get_electric(self):
        self.te.h3('Проверка конфигурации устройства в соответствии с заданными функциями защиты')
        self.te.i('Конфигурация соответствует заданным функциям защиты')
        self.te.h3('Проверка уставок устройства защиты в соответствии с заданной конфигурацией')
        self.te.i('Уставки соответствуют таблице уставок')
        self.te.table_name('Проверка правильности отображения значений и фазовых углов токов (напряжений), поданных от постороннего источника.')
        self.te.table_head('Канал', 'Обозначение', 'Подано', 'Отображено на терминале')
        for c in self.calibration:
            self.te.table_row(*c)
        if self.mode:
            self.te.p(self.mode)
        if self.gfc and self.gfc.Operation:
            self.gfc.get_electric()
        if self.fuse:
            self.te.h3('Проверка функции блокировки при неисправности цепей напряжения')
            self.fuse.get_electric()
        if self.psd and self.psd.Operation:
            self.te.h3('Проверка функции блокировки от качаний')
            self.psd.get_electric()
        if self.zm1 and self.zm1.Operation:
            self.te.h3('Проверка первой ступени дистанционной защиты')
            self.zm1.get_electric(1)
        if self.zm2 and self.zm2.Operation:
            self.te.h3('Проверка второй ступени дистанционной защиты')
            self.zm2.get_electric(2)
        if self.zm3 and self.zm3.Operation:
            self.te.h3('Проверка третьей ступени дистанционной защиты')
            self.zm3.get_electric(3)
        if self.zm4 and self.zm4.Operation:
            self.te.h3('Проверка четвёртой ступени дистанционной защиты')
            self.zm4.get_electric(4)
        if self.zm5 and self.zm5.Operation:
            self.te.h3('Проверка пятой ступени дистанционной защиты')
            self.zm5.get_electric(5)
        if self.ef4 and self.ef4.Operation:
            self.te.h3('Проверка НТЗНП')
            self.ef4.get_electric()
        if self.bfp and self.bfp.Operation:
            self.te.h3('Проверка УРОВ')
            self.bfp.get_electric()
        if self.toc and self.toc.Operation:
            self.te.h3(f'Проверка функции: {self.toc.name}')
            self.toc.get_electric()
        if self.da06 and self.da06.Operation:
            self.te.h3(f'Проверка функции: {self.da06.name}')
            self.da06.get_electric()
        if self.da07 and self.da07.Operation:
            self.te.h3(f'Проверка функции: {self.da07.name}')
            self.da07.get_electric()
        if self.da08 and self.da08.Operation:
            self.te.h3(f'Проверка функции: {self.da08.name}')
            self.da08.get_electric()

    def get_complex(self):
        if self.zm1 and self.zm1.Operation:
            self.zm1.get_complex(1)
        if self.zm2 and self.zm2.Operation:
            self.zm2.get_complex(2)
        if self.zm3 and self.zm3.Operation:
            self.zm3.get_complex(3)
        if self.zm4 and self.zm4.Operation:
            self.zm4.get_complex(4)
        if self.zm5 and self.zm5.Operation:
            self.zm5.get_complex(5)
        if self.ef4 and self.ef4.Operation:
            self.ef4.get_complex()
        if self.bfp and self.bfp.Operation:
            self.bfp.get_complex()
        if self.toc and self.toc.Operation:
            self.toc.get_complex()
        if self.da06 and self.da06.Operation:
            self.da06.get_complex(f'{self.da06.name}')
        if self.da07 and self.da07.Operation:
            self.da07.get_complex(f'{self.da07.name}')
        if self.da08 and self.da08.Operation:
            self.da08.get_complex(f'{self.da08.name}')

    def add_context(self, **kwargs):
        super().add_context(**kwargs)
        if self.gfc:
            self.gfc.add_context(**kwargs)
        if self.psd:
            self.psd.add_context(**kwargs)
        if self.zm1:
            self.zm1.add_context(**kwargs)
        if self.zm2:
            self.zm2.add_context(**kwargs)
        if self.zm3:
            self.zm3.add_context(**kwargs)
        if self.zm4:
            self.zm4.add_context(**kwargs)
        if self.zm5:
            self.zm5.add_context(**kwargs)
        if self.fuse:
            self.fuse.add_context(**kwargs, configuration=self.configuration)
        if self.ef4:
            self.ef4.add_context(**kwargs, configuration=self.configuration)
        if self.bfp:
            self.bfp.add_context(**kwargs)
        if self.toc:
            self.toc.add_context(**kwargs)
        if self.da06:
            self.da06.add_context(**kwargs)
        if self.da07:
            self.da07.add_context(**kwargs)
        if self.da08:
            self.da08.add_context(**kwargs)
