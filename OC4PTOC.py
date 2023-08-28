from random import uniform


from pydantic import BaseModel


from interfaces import Function


class StageOC4PTOC(BaseModel):
    name: str
    I1: float
    t1: float


class OC4PTOC(Function):

    KTT: int
    IBase: float
    stages: list[StageOC4PTOC]


    def get_electric(self):
        phases = ('A', 'B', 'C')
        self.te.h3('Проверка функции OC4PTOC')
        for num_stage, stage in enumerate(self.stages):
            self.te.h4(f'Проверка токов срабатывания и возврата функции {stage.name}')
            self.te.table_name()
            self.te.table_head('Фаза', 'Уставка', 'Iср,А', 'Отклонение %', 'Iв, А', 'Кв')
            i2 = stage.I1 * self.IBase / self.KTT / 100
            if not self.tests[num_stage]['result_isz']:
                self.tests[num_stage]['result_isz'] = [{'I>': i2 * uniform(1, 1.01),
                                       'I<': i2 * 0.96 * uniform(1, 1.01)},
                                      {'I>': i2 * uniform(1, 1.01),
                                       'I<': i2 * 0.96 * uniform(1, 1.01)},
                                      {'I>': i2 * uniform(1, 1.01),
                                       'I<': i2 * 0.96 * uniform(1, 1.01)}]
            for num, phase in enumerate(self.tests[num_stage]['result_isz']):
                self.te.table_row(f'{phases[num]}', f'{i2:.4f}', f'{phase["I>"]:.4f}',
                        f'{100 * float(phase["I>"]) / i2 - 100:.4f}', f'{float(phase["I<"]):.4f}',
                        f'{float(phase["I<"]) / float(phase["I>"]):.4f}')


    def get_complex(self):
        html = ''
        for num_stage, stage in enumerate(self.stages):
            i2 = stage.I1 * self.IBase / self.KTT / 100
            self.te.h3(f'Комплексная проверка функции {stage.name} при токе {i2 * 1.1:.2f} A')
            self.te.table_name()
            self.te.table_head('Время, сек', 'Сработавший контакт')
            for num, t_contact in enumerate(self.tests[num_stage]['result_complex']):
                t = f'{t_contact:.3f}' if t_contact else 'Не сработал'
                self.te.table_row(f'{t}', f'{self.contacts[num]}')
            self.te.p(f'При токе {i2 * 0.9:.2f} A не срабатывает.')