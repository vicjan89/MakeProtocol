from  hf_channel import HfChannel
from interfaces import element
from REL5__.REL511 import REL511
from REL5__.REL551 import REL551
from REF54_.REF545 import REF545
from TOR.TOR import TOR
from CT import CT
from VT import VT
from ETL540 import ETL540
from SF import SF


class Pris(element):
    hf_channel: HfChannel | None = None
    rel511k1: REL511 | None = None
    rel551: REL551 | None = None
    rel511k2: REL511 | None = None
    ref545: REF545 | None = None
    tor: TOR | None = None
    etl: ETL540 | None = None
    spec: str | None = None
    ct: CT | None = None
    vt: VT | None = None
    izol: list
    rele: list | None = None
    out_electric: str | None = None
    tests: dict | None = None
    vzaimodeistvie: list
    vzaimodeistvie_vnesh: list
    work_current: list
    list_sf: list[SF]
    contacts: list | None = None
    measurements: list[str]
    on_switch: list[str] | None = None
    sign: list[list]

    def add_context(self, **kwargs):
        super().add_context(**kwargs)
        if self.hf_channel:
            self.hf_channel.add_context(**kwargs)
        if self.ct:
            self.ct.add_context(**kwargs)
            kwargs.update({'ct': self.ct, 'vt': self.vt})
        if self.rel511k1:
            self.rel511k1.add_context(**kwargs)
        if self.rel551:
            self.rel551.add_context(**kwargs)
        if self.rel511k2:
            self.rel511k2.add_context(**kwargs)
        if self.ref545:
            self.ref545.add_context(**kwargs)
        if self.tor:
            self.tor.add_context(**kwargs)
        if self.etl:
            self.etl.add_context(**kwargs)
        for sf in self.list_sf:
            sf.add_context(**kwargs)

    def get_protocol(self):
        if self.spec:
            self.te.h1('Основные характеристики аппаратуры')
            self.te.include(self.spec)
        self.te.h1('Внешний осмотр панелей, шкафов и другого оборудования')
        self.te.ul('Надёжность крепления панели, шкафа, ящика, аппаратуры.')
        self.te.i('Крепления и аппаратура установлены надежно.')
        self.te.ul('Отсутствие механических повреждений аппаратуры, состояние изоляции выводов реле и другой аппаратуры.')
        self.te.i('Повреждения отсутствуют, состояние изоляции удовлетворительное.')
        self.te.ul('Отсутствие пыли и грязи на кожухах аппаратуры и рядах зажимов.')
        self.te.i('Загрязнения отсутствуют.')
        self.te.ul('Состояние окраски панелей, шкафов, ящиков и др.элементов устройства.')
        self.te.i('Состояние удовлетворительное.')
        self.te.ul('Состояние монтажа проводов и кабелей, надежность контактных соединений на радах зажимов, ответвлениях'
                   ' от шинок, шпильках реле, испытательных блоках, резисторах, а также надежность паек всех элементов.')
        self.te.i('Состояние удовлетворительное.')
        self.te.ul('Состояние концевых разделок кабелей вторичных соединений.')
        self.te.i('Состояние удовлетворительное.')
        self.te.ul('Состояние уплотнений дверок шкафов, кожухов') # выводов на стороне вторичных цепей трансформаторов тока'
                   # ' и напряжения и т.д.')
        self.te.i('Состояние удовлетворительное.')
        # self.te.ul('Состояние заземления вторичных цепей.')
        # self.te.i('Состояние удовлетворительное.')
        # self.te.ul('Состояние электромагнитов управления и блок - контактов разъединителей, выключателей, автоматов'
        #            ' и другой коммутационной аппаратуры.')
        # self.te.i('Состояние удовлетворительное.')
        self.te.ul('Наличие надписей на панелях, шкафах, ящиках и аппаратуре, наличие маркировки кабелей, жил кабелей'
                   ' и проводов.')
        self.te.i('Надписи в наличии и верны.')
        # self.te.h1('Предварительная проверка заданных уставок')
        # self.te.i('Предварительная проверка не выявила отклонений.')
        self.te.h1('Внутренний осмотр, чистка и проверка механической части аппаратуры')
        # self.te.ul('Проверка состояния уплотнения кожухов и целости стекол.')
        # self.te.i('Состояние удовлетворительное.')
        self.te.ul('Проверка состояния деталей, правильности их установки и надежности крепления.')
        self.te.i('Детали в целости, закреплены надежно. Заземления имеются. Надписи выполнены согласно проекта')
        # self.te.ul('Чистка от пыли.')
        # self.te.i('Чистка выполнена.')
        self.te.ul('Проверка надежности контактных соединений и паек.')
        self.te.i('Контактные соединения выполнены надежно.')
        # self.te.ul('Проверка затяжки болтов, стягивающих сердечники трансформаторов, дросселей и т.п.')
        # self.te.i('Сердечники трансформаторов стянуты надежно.')
        self.te.ul('Проверка состояния изоляции соединительных проводов и обмоток аппаратуры.')
        self.te.i('Состояние удовлетворительное.')
        self.te.ul('Проверка состояния контактных поверхностей.')
        self.te.i('Состояние удовлетворительное.')
        self.te.ul('Проверка и (при необходимости) регулирование механических характеристик аппаратуры.')
        self.te.i('Люфты и зазоры незначительны')
        self.te.h1('Провека сопротивления изоляции')
        self.te.table_name('Измерение изоляции')
        self.te.table_head('№ группы', 'Цепь', 'Режим', 'Сопротивление,МОм', widths=(1, 5, 2, 2))
        for n, gr in enumerate(self.izol):
            self.te.table_row(n+1, gr[0], gr[1] if gr[1] else '-', gr[2])
        self.te.i('Состояние изоляции удовлетворительное')
        self.te.h1('Проверка соответствия проекту смонтированных устройств')
        self.te.ul('Фактическое исполнение соединений между кассетами,блоками,модулями, реле, переключателями и другими'
                   'элементами на пенелях, в шкафах, ящиках с одновременной проверкой правильности маркировки')
        self.te.i('Состояние удовлетворительное.')
        self.te.ul('Фактическое исполнение всех цепей связи между проверяемыми устройством и другими устройствами РЗА, '
                   'управления, сигнализации. Одновременно проводится проверка правильности маркировки жил кабелей')
        self.te.i('Состояние удовлетворительное.')
        self.get_electric()
        self.te.h1('Проверка взаимодействия элементов устройства')
        for row in self.vzaimodeistvie:
            self.te.ul(row)
        self.te.h1('Измерение и испытание изоляции')
        self.te.table_name('Измерение изоляции')
        self.te.table_head('№ группы', 'Цепь', 'Режим', 'Сопротивление,МОм', widths=(1, 5, 2, 2))
        for n, gr in enumerate(self.izol):
            self.te.table_row(n+1, gr[0], gr[1] if gr[1] else '-', gr[2])
        self.te.p('Изоляция вторичных цепей испытана напряжением 1000В в течение 1 минуты. Изоляция испытание выдержала.')
        self.get_complex()
        self.te.h1('Проверка взаимодействия проверяемого устройства с другими включенными в работу устройствами защит, '
                   'электроавтоматики, управления и сигнализации, действия устройства на коммутационные аппараты')
        self.te.p('Проведено опробование устройств защиты с действием на выходные цепи в соответствии с заданной логикой '
                  'устройства и проекту:')
        for row in self.vzaimodeistvie_vnesh:
            self.te.ul(row)
        # self.te.ul('проверено управление выключателем 110кВ от ключа и устройства АСУ;')
        # self.te.ul('проверена работа АПВ при аварийном отключении выключателя;')
        self.te.ul('проверена работа аварийной и вызывной сигнализации.')
        # self.te.ul('проверено прохождение сигналов по цепям РАС;')
        if self.on_switch:
            for cs in self.on_switch:
                self.te.ul(cs)
        self.te.h1('Проверка рабочим током и напряжением')
        self.te.table_name('Измерение токов и напряжений')
        self.te.table_head(*self.work_current[0], widths=(3, 1, 1, 1, 1))
        for row in self.work_current[1:]:
            self.te.table_row(*row)
        self.te.b('Заключение')
        self.te.p('Устройства РЗА исправны и пригодны к эксплуатации')
        self.te.b('Измерения производились приборами:')
        for m in self.measurements:
            self.te.ul(m)
        self.te.b('Испытания проводили')
        for sign in self.sign:
            self.te.text += f'{sign[0]} |{sign[2]}| {sign[1]}\n\n'
        self.te.text += '\n'
        for sign in self.sign:
            self.te.text += f'.. |{sign[2]}| image:: {sign[2]}\n   :width: 140px\n\n'

    def get_electric(self):
        self.te.h1('Проверка электрических характеристик')
        self.te.h2('Реле, автоматические выключатели') # , соленоиды управления высоковольтных выключателей')
        self.te.h3('Проверка автоматических выключателей')
        self.te.p('Проведён внешний осмотр выключателей, состояние удовлетворительное')
        for sf in self.list_sf:
            sf.get_electric()
        self.te.i('Выключатели исправны и пригодны к эксплуатации.')
        if self.rele:
            self.te.h3('Проверка реле')
            self.te.table_name('Результат проверки')
            self.te.table_head('Название', 'Марка', 'Место уставновки', 'Срабатывание,B', 'Возврат,B', 'Кв')
            for r in self.rele:
                self.te.table_row(r['name'], r['type'], r['location'], r['is'], r['iv'], f'{r["iv"]/r["is"]:.2f}')
            self.te.i('Реле исправны и пригодны для эксплуатации')
        if self.ct:
            self.ct.get_electric()
        if self.rel511k1:
            self.rel511k1.get_electric()
        if self.rel551:
            self.rel551.get_electric()
        if self.rel511k2:
            self.rel511k2.get_electric()
        if self.ref545:
            self.ref545.get_electric()
        if self.tor:
            self.tor.get_electric()
        if self.etl:
            self.etl.get_electric()
        if self.hf_channel:
            self.hf_channel.get_electric()

    def get_complex(self):
        self.te.h1('Комплексная проверка')
        if self.rel511k1:
            self.rel511k1.get_complex()
        if self.rel551:
            self.rel551.get_complex()
        if self.rel511k2:
            self.rel511k2.get_complex()
        if self.ref545:
            self.ref545.get_complex()
        if self.tor:
            self.tor.get_complex()
