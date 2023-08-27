from random import uniform


from interfaces import Function


class CVGAPC(Function):

    KTT: int
    IBase: float
    nameOC1: str
    StartCurr_OC1: float
    tDef_OC1: float
    nameOC2: str
    StartCurr_OC2: float
    tDef_OC2: float

    @property
    def StartCurr_OC1_A1(self):
        return self.IBase * self.StartCurr_OC1 / 100

    @property
    def StartCurr_OC1_A2(self):
        return self.StartCurr_OC1_A1 / self.KTT

    @property
    def StartCurr_OC2_A1(self):
        return self.IBase * self.StartCurr_OC2 / 100

    @property
    def StartCurr_OC2_A2(self):
        return self.StartCurr_OC2_A1 / self.KTT

    def get_electric(self):
        phases = ('A', 'B', 'C')
        self.te.h3(f'Проверка токов срабатывания и возврата функции {self.nameOC1}')
        self.te.table_head('Фаза', 'Уставка', 'Iср,А', 'Отклонение %', 'Iв, А', 'Кв')
        if not self.tests[0]['result']:
            self.tests[0]['result'] = [{'I>': self.StartCurr_OC1_A2 * uniform(1, 1.01), 'I<': self.StartCurr_OC1_A2 * 0.96 * uniform(1, 1.01)},
                                  {'I>': self.StartCurr_OC1_A2 * uniform(1, 1.01), 'I<': self.StartCurr_OC1_A2 * 0.96 * uniform(1, 1.01)},
                                  {'I>': self.StartCurr_OC1_A2 * uniform(1, 1.01), 'I<': self.StartCurr_OC1_A2 * 0.96 * uniform(1, 1.01)}]
        for num, phase in enumerate(self.tests[0]['result']):
            self.te.table_row(phases[num], f'{self.StartCurr_OC1_A2:.4f}', f'{phase["I>"]:.4f}',
                    f'{100*float(phase["I>"])/self.StartCurr_OC1_A2-100:.4f}', f'{float(phase["I<"]):.4f}',
                    f'{float(phase["I<"])/float(phase["I>"]):.4f}')
        self.te.h3(f'Проверка токов срабатывания и возврата функции {self.nameOC2}')
        self.te.table_head('Фаза', 'Уставка', 'Iср,А', 'Отклонение %', 'Iв, А', 'Кв')
        if not self.tests[2]['result']:
            self.tests[2]['result'] = [
                {'I>': self.StartCurr_OC2_A2 * uniform(1, 1.01), 'I<': self.StartCurr_OC2_A2 * 0.96 * uniform(1, 1.01)},
                {'I>': self.StartCurr_OC2_A2 * uniform(1, 1.01), 'I<': self.StartCurr_OC2_A2 * 0.96 * uniform(1, 1.01)},
                {'I>': self.StartCurr_OC2_A2 * uniform(1, 1.01), 'I<': self.StartCurr_OC2_A2 * 0.96 * uniform(1, 1.01)}]
        for num, phase in enumerate(self.tests[2]['result']):
            self.te.table_row(f'{phases[num]}', f'{self.StartCurr_OC2_A2:.4f}', f'{phase["I>"]:.4f}',
                    f'{100 * float(phase["I>"]) / self.StartCurr_OC2_A2 - 100:.4f}', f'{float(phase["I<"]):.4f}',
                    f'{float(phase["I<"]) / float(phase["I>"]):.4f}')

    def get_complex(self):
        self.te.h3(f'Комплексная проверка функции {self.nameOC1} при токе {self.StartCurr_OC1_A2*1.1:.2f} A')
        self.te.table_head('Время, сек', 'Сработавший контакт')
        for num, t_contact in enumerate(self.tests[1]['result']):
            t = f'{t_contact:.3f}' if t_contact else 'Не сработал'
            self.te.table_row(f'{t}', f'{self.contacts[num]}')
        self.te.p(f'При токе {self.StartCurr_OC1_A2*0.9:.2f} A не срабатывает.')
        self.te.h3(f'Комплексная проверка функции {self.nameOC2} при токе {self.StartCurr_OC2_A2*1.1:.2f} A')
        self.te.table_head('Время, сек', 'Сработавший контакт')
        for num, t_contact in enumerate(self.tests[3]['result']):
            t = f'{t_contact:.3f}' if t_contact else 'Не сработал'
            self.te.table_row(f'{t}', f'{self.contacts[num]}')
        self.te.p(f'При токе {self.StartCurr_OC2_A2*0.9:.2f} A не срабатывает.')