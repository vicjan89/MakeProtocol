from RE_500 import Config, CT

class NOC3HIGH:

    def __init__(self, contacts: list, tests: dict, config: Config, ct: CT, name: str = ''):
        self.contacts = contacts
        self.tests = tests
        self.ct = ct
        self.name = name
        self.Start_current: float = float(config.get_param('F032S072'))
        self.Operate_time: float = float(config.get_param('F032S073'))
        self.CBFP_time: int = float(config.get_param('F032V008'))

    def get_electric(self):
        phases = ('A', 'B', 'C')
        html = f'<h3>Проверка токов срабатывания и возврата функции NOC3HIGH {self.name}</h3>\n'
        html += '<table>\n<tr><th>Фаза</th><th>Уставка</th><th>Iср,А</th><th>Отклонение %</th><th>Iв, А</th><th>Кв</th>\n'
        for num, phase in enumerate(self.tests['result_i']):
            ust = self.Start_current * self.ct[num].second_current
            html += f'<tr><td>{phases[num]}</td><td>{ust:.4f}</td>' \
                    f'<td>{phase[0]:.4f}</td>' \
                    f'<td>{(phase[0] - ust)/ust * 100:.4f}</td><td>{phase[1]:.4f}</td>' \
                    f'<td>{phase[1]/phase[0]:.4f}</td>\n'
        html += '</table>\n'
        return html

    def get_complex(self):
        return ''