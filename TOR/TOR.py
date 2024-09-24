from interfaces import Terminal


from TOR.DZO import DZO


class TOR(Terminal):
    mode: str | None = None
    configuration: dict | None = None
    calibration: list
    dzo: DZO | None = None
    contacts: list | None = None
    check_complex: dict = None

    def get_electric(self):
        self.te.h2('Проверка терминала защит ТОР-300 ДЗО-503')
        self.te.h3('Проверка конфигурации устройства в соответствии с заданными функциями защиты')
        self.te.i('Конфигурация соответствует заданным функциям защиты')
        self.te.h3('Проверка уставок устройства защиты в соответствии с заданной конфигурацией')
        self.te.i('Уставки соответствуют таблице уставок')
        self.te.h4('Проверка правильности отображения значений и фазовых углов токов (напряжений), поданных от постороннего источника.')
        self.te.table_name('Результаты проверки')
        self.te.table_head('Канал', 'Обозначение', 'Подано', 'Отображено на терминале')
        for c in self.calibration:
            self.te.table_row(*c)
        if self.mode:
            self.te.p(self.mode)
        if self.dzo:
            self.dzo.get_electric()

    def get_complex(self):
        contacts = self.check_complex['contacts']
        self.te.h3('Комплексная проверка')
        cases = dict()
        for cs in self.check_complex['cases']:
            if cs[0] in cases:
                cases[cs[0]][0] = cs[1]
                cases[cs[0]][1] = cs[2]
                cases[cs[0]][2].append([cs[3], cs[4:]])
            else:
                cases[cs[0]] = [cs[1], cs[2], [[cs[3], cs[4:]]]]
        for name, cs in cases.items():
            self.te.table_name(f'{name}. Ток {cs[0]:.2f}A. Время выдачи {cs[1]}сек.')
            self.te.table_head('Контакт', 'Время,сек', 'Действие')
            for group_cont, cont in cs[2]:
                for c in cont:
                    self.te.table_row(contacts[group_cont][c[0]-1], f'{c[1]:.3f}', 'Замкнулся' if c[2] else 'Разомкнулся')



    def add_context(self, **kwargs):
        super().add_context(**kwargs)
        if self.dzo:
            self.dzo.add_context(**kwargs)
