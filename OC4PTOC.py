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
        html = ''
        for num_stage, stage in enumerate(self.stages):
            html += f'<h3>Проверка токов срабатывания и возврата функции {stage.name}</h3>\n'
            html += '<table>\n<tr><th>Фаза</th><th>Уставка</th><th>Iср,А</th><th>Отклонение %</th><th>Iв, А</th><th>Кв</th>\n'
            i2 = stage.I1 * self.IBase / self.KTT / 100
            if not self.tests[num_stage]['result_isz']:
                self.tests[num_stage]['result_isz'] = [{'I>': i2 * uniform(1, 1.01),
                                       'I<': i2 * 0.96 * uniform(1, 1.01)},
                                      {'I>': i2 * uniform(1, 1.01),
                                       'I<': i2 * 0.96 * uniform(1, 1.01)},
                                      {'I>': i2 * uniform(1, 1.01),
                                       'I<': i2 * 0.96 * uniform(1, 1.01)}]
            for num, phase in enumerate(self.tests[num_stage]['result_isz']):
                html += f'<tr><td>{phases[num]}</td><td>{i2:.4f}</td><td>{phase["I>"]:.4f}</td>' \
                        f'<td>{100 * float(phase["I>"]) / i2 - 100:.4f}</td><td>{float(phase["I<"]):.4f}</td>' \
                        f'<td>{float(phase["I<"]) / float(phase["I>"]):.4f}</td>\n'
            html += '</table>\n'

        return html

    def get_complex(self):
        html = ''
        for num_stage, stage in enumerate(self.stages):
            i2 = stage.I1 * self.IBase / self.KTT / 100
            html += f'<h3>Комплексная проверка функции {stage.name} при токе {i2 * 1.1:.2f} A</h3>\n'
            html += '<table>\n<tr><th>Время, сек</th><th>Сработавший контакт</th></tr>\n'
            for num, t_contact in enumerate(self.tests[num_stage]['result_complex']):
                t = f'{t_contact:.3f}' if t_contact else 'Не сработал'
                html += f'<tr><td>{t}</td><td>{self.contacts[num]}</td></tr>\n'
            html += '</table>\n'
            html += f'<p>При токе {i2 * 0.9:.2f} A не срабатывает.</p>\n'
        return html