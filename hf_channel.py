

from interfaces import element
from textengines.interfaces import TextEngine

class Fp(element):
    model: str
    factory_number: int

    def __str__(self):
        return f'Фильтр присоединения {self.model} заводской номер {self.factory_number}'

    def get_electric(self):
        self.te.h2('Фильтр присоединения')
        self.te.h3('Проверка механической части')
        self.te.p('Особое внимание обращено на надёжность крепления соединения корпуса фильтра присоединения с '
                  'заземляющим контуром и на исправность и надёжность контактов заземляющего ножа конденсатора связи')
        self.te.i('Состояние удовлетворительное')
        self.te.h3('Проверка разрядников')
        self.te.p('Проверена исправность мегаомметром на 1000 В')
        self.te.i('Не пробивается')
        # self.te.h3('Измерение затухания фильтра присоединения на рабочей частоте') #почему то на практике не делается
        # self.te.h3('Снятие зависимости затухания фильтра присоединения от частоты на рабочих частотах каналов') #почему то на практике не делается

    def get_complex(self):
        ...

class HfKabel(element):
    model: str
    Riz: int #в МОм
    l: int #длина в метрах

    def __str__(self):
        return f'Высокочастотный кабель марки {self.model} длиной {self.l} метров'

    def get_electric(self):
        self.te.h2('Высокочастотный кабель')
        self.te.h3('Проверка механического состояния')
        self.te.p('Проверено состояние разделок, правильность подключения жилы и экрана. Особое внимание обращено на '
                  'прокладку кабеля на подходе к фильтру присоединения')
        self.te.i('Состояние удовлетворительное')
        self.te.h3('Проверка сопротивления изоляции')
        self.te.p(f'Rиз = {self.Riz} МОм. Норма согласно 9.4.6.2 СТП 33240.48.154-20 {100/self.l*1000} Мом')

    def get_complex(self):
        ...
class Transceiver(element):
    model: str
    factory_number: str
    f_to: int
    df_to: int
    f_from: int
    df_from: int

    def get_electric(self):
        ...

    def get_complex(self):
        ...

    def __str__(self):
        return f'Приёмопередатчик {self.model}, заводской номер {self.factory_number}, частота передачи {self.f_to} + ' \
               f'{self.df_to} кГц, частота приёма {self.f_from} + {self.df_from} кГц'


class HfChannel(element):
    fp: Fp
    hf_kabel: HfKabel
    transceiver: Transceiver
    a_pasport: float # паспортное рабочее затухание ВЧ тракта (п.10.1.2 СТП 33240.48.154-20)


    def get_electric(self):
        self.te.h2('Спецификация аппаратуры')
        self.te.ul(str(self.transceiver))
        self.te.ul(str(self.fp))
        self.te.ul(str(self.hf_kabel))
        self.fp.get_electric()
        self.hf_kabel.get_electric()
        self.te.h2('Раздельная проверка полукомплектов')
        self.te.h3('Измерение затухания ВЧ кабеля совместно с фильтром присоединения')
        self.te.image('retom-hf-1.png')
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