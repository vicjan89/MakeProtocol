

from interfaces import element
from textengines.interfaces import TextEngine

class Fp(element):
    model: str
    factory_number: int

    def get_electric(self):
        self.te.h2('Фильтр присоединения')
        self.te.h3('Проверка механической части')
        self.te.p('Особое внимание обращено на надёжность крепления соединения корпуса фильтра присоединения с '
                  'заземляющим контуром и на исправность и надёжность контактов заземляющего ножа конденсатора связи')
        self.te.i('Состояние удовлетворительное')
        self.te.h3('Проверка разрядников')
        self.te.p('Проверена исправность мегаомметром на 1000 В')
        self.te.i('Не пробивается')
        self.te.h3('Измерение затухания фильтра присоединения на рабочей частоте')
        self.te.h3('Снятие зависимости затухания фильтра присоединения от частоты на рабочих частотах каналов')

    def get_complex(self):
        ...

class HfKabel(element):
    model: str

    def get_electric(self):
        self.te.h2('Высокочастотный кабель')
        self.te.h3('Проверка механического состояния')
        self.te.p('Проверено состояние разделок, правильность подключения жилы и экрана. Особое внимание обращено на '
                  'прокладку кабеля на подходе к фильтру присоединения')
        self.te.i('Состояние удовлетворительное')

    def get_complex(self):
        ...

class HfChannel(element):
    fp: Fp
    hf_kabel: HfKabel

    def get_electric(self):
        self.fp.get_electric()
        self.hf_kabel.get_electric()
        self.te.h2('Раздельная проверка полукомплектов')
        self.te.h3('Измерение затухания ВЧ кабеля совместно с фильтром присоединения')
        self.te.h3('Измерение входного сопротивления ВЧ тракта, мощности, отдаваемой передатчиком на ВЧ тракт,'
                   'и согласование выхода передатчика с ВЧ трактом')
        self.te.h2('Двусторонняя проверка в канале')
        self.te.h3('Проверка работы переговорного устройства')

    def get_complex(self):
        ...

    def add_te(self, te: TextEngine):
        super().add_te(te)
        self.fp.add_te(te)
        self.hf_kabel.add_te(te)