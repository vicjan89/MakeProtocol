from REL5__.REL5__ import REL5__
from REL5__.DIFL import DIFL

class REL551(REL5__):
    difl: DIFL
    def get_electric(self):
        self.te.h2(f'Проверка терминала {self.name} REL551')
        super().get_electric()
        if self.difl and self.difl.Operation:
            self.difl.get_electric()


    def get_complex(self):
        self.te.h2(f'Комплексная проверка терминала {self.name} REF551')
        super().get_complex()


    def add_context(self, **kwargs):
        super().add_context(**kwargs)
        if self.difl:
            self.difl.add_context(**kwargs, configuration=self.configuration)