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
        html = f'<h3>Проверка токов срабатывания и возврата функции {self.nameOC1}</h3>\n'
        html += '<table>\n<tr><th>Фаза</th><th>Уставка</th><th>Iср,А</th><th>Отклонение %</th><th>Iв, А</th><th>Кв</th>\n'
        if not self.tests[0]['result']:
            self.tests[0]['result'] = [{'I>': self.StartCurr_OC1_A2 * uniform(1, 1.01), 'I<': self.StartCurr_OC1_A2 * 0.96 * uniform(1, 1.01)},
                                  {'I>': self.StartCurr_OC1_A2 * uniform(1, 1.01), 'I<': self.StartCurr_OC1_A2 * 0.96 * uniform(1, 1.01)},
                                  {'I>': self.StartCurr_OC1_A2 * uniform(1, 1.01), 'I<': self.StartCurr_OC1_A2 * 0.96 * uniform(1, 1.01)}]
        for num, phase in enumerate(self.tests[0]['result']):
            html += f'<tr><td>{phases[num]}</td><td>{self.StartCurr_OC1_A2:.4f}</td><td>{phase["I>"]:.4f}</td>' \
                    f'<td>{100*float(phase["I>"])/self.StartCurr_OC1_A2-100:.4f}</td><td>{float(phase["I<"]):.4f}</td>' \
                    f'<td>{float(phase["I<"])/float(phase["I>"]):.4f}</td>\n'
        html += '</table>\n'
        html += f'<h3>Проверка токов срабатывания и возврата функции {self.nameOC2}</h3>\n'
        html += '<table>\n<tr><th>Фаза</th><th>Уставка</th><th>Iср,А</th><th>Отклонение %</th><th>Iв, А</th><th>Кв</th>\n'
        if not self.tests[2]['result']:
            self.tests[2]['result'] = [
                {'I>': self.StartCurr_OC2_A2 * uniform(1, 1.01), 'I<': self.StartCurr_OC2_A2 * 0.96 * uniform(1, 1.01)},
                {'I>': self.StartCurr_OC2_A2 * uniform(1, 1.01), 'I<': self.StartCurr_OC2_A2 * 0.96 * uniform(1, 1.01)},
                {'I>': self.StartCurr_OC2_A2 * uniform(1, 1.01), 'I<': self.StartCurr_OC2_A2 * 0.96 * uniform(1, 1.01)}]
        for num, phase in enumerate(self.tests[2]['result']):
            html += f'<tr><td>{phases[num]}</td><td>{self.StartCurr_OC2_A2:.4f}</td><td>{phase["I>"]:.4f}</td>' \
                    f'<td>{100 * float(phase["I>"]) / self.StartCurr_OC2_A2 - 100:.4f}</td><td>{float(phase["I<"]):.4f}</td>' \
                    f'<td>{float(phase["I<"]) / float(phase["I>"]):.4f}</td>\n'
        html += '</table>\n'
        return html

    def get_complex(self):
        html = f'<h3>Комплексная проверка функции {self.nameOC1} при токе {self.StartCurr_OC1_A2*1.1:.2f} A</h3>\n'
        html += '<table>\n<tr><th>Время, сек</th><th>Сработавший контакт</th></tr>\n'
        for num, t_contact in enumerate(self.tests[1]['result']):
            t = f'{t_contact:.3f}' if t_contact else 'Не сработал'
            html += f'<tr><td>{t}</td><td>{self.contacts[num]}</td></tr>\n'
        html += '</table>\n'
        html += f'<p>При токе {self.StartCurr_OC1_A2*0.9:.2f} A не срабатывает.</p>\n'
        html += f'<h3>Комплексная проверка функции {self.nameOC2} при токе {self.StartCurr_OC2_A2 * 1.1:.2f} A</h3>\n'
        html += '<table>\n<tr><th>Время, сек</th><th>Сработавший контакт</th></tr>\n'
        for num, t_contact in enumerate(self.tests[3]['result']):
            t = f'{t_contact:.3f}' if t_contact else 'Не сработал'
            html += f'<tr><td>{t}</td><td>{self.contacts[num]}</td></tr>\n'
        html += '</table>\n'
        html += f'<p>При токе {self.StartCurr_OC2_A2 * 0.9:.2f} A не срабатывает.</p>\n'
        return html