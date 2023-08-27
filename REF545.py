from interfaces import Terminal
from NOC3HIGH import NOC3HIGH
from RE_500 import Config, CT
from interfaces import TextEngine



class REF545(Terminal):
    func_classes = {'NOC3HIGH': NOC3HIGH}
    current_transformers = ('F003', (('V001', 'V002'), ('V011', 'V012'), ('V021', 'V022'), ('V031', 'V032'),
                                     ('V041', 'V042'), ('V151', 'V152'), ('V161', 'V162'), ('V171', 'V172'),
                                     ('V181', 'V182'), ('V191', 'V192')))

    def __init__(self, data: dict, text_engine: TextEngine):
        super().__init__(data, text_engine)
        config = Config(data['path'])
        self.CT = []
        for ct in self.current_transformers[1]:
            sc = config.get_param(f'{self.current_transformers[0]}{ct[0]}')
            pc = config.get_param(f'{self.current_transformers[0]}{ct[1]}')
            self.CT.append(CT(Second_current=sc, Primary_current=pc))
        self.functions = []
        for func in data['functions']:
            self.functions.append(self.func_classes[func['func']](contacts=func['contacts'], tests=func['tests'],
                                                                  config=config, name=func['name'], ct=self.CT,
                                                                  te=self.te))
