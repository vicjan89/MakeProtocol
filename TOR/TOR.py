from interfaces import Terminal


from TOR.DZO import DZO


class TOR(Terminal):
    mode: str | None = None
    configuration: dict
    calibration: list
    dzo: DZO | None = None
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
        if self.dzo:
            self.dzo.get_electric()

    def get_complex(self):
        ...

    def add_context(self, **kwargs):
        super().add_context(**kwargs)
        if self.dzo:
            self.dzo.add_context(**kwargs)
