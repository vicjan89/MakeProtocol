from RE_500 import Config, CT
from interfaces import TextEngine


class NOC3HIGH:

    def __init__(self, contacts: list, tests: dict, config: Config, ct: CT, te: TextEngine, name: str = ''):
        self.contacts = contacts
        self.te = te
        self.tests = tests
        self.ct = ct
        self.name = name
        self.Start_current: float = float(config.get_param('F032S072'))
        self.Operate_time: float = float(config.get_param('F032S073'))
        self.CBFP_time: int = float(config.get_param('F032V008'))

    def get_electric(self):
        phases = ('A', 'B', 'C')
        self.te.h3(f'Проверка токов срабатывания и возврата функции NOC3HIGH {self.name}')
        self.te.table_head('Фаза', 'Уставка', 'Iср,А', 'Отклонение %', 'Iв, А', 'Кв')
        for num, phase in enumerate(self.tests['result_i']):
            ust = self.Start_current * self.ct[num].second_current
            self.te.table_row(f'{phases[num]}', f'{ust:.4f}', f'{phase[0]:.4f}', f'{(phase[0] - ust)/ust * 100:.4f}',
            f'{phase[1]:.4f}', f'{phase[1]/phase[0]:.4f}')

    def get_complex(self):
        ...