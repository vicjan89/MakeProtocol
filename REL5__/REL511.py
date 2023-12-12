from REL5__.REL5__ import REL5__

class REL511(REL5__):

    def get_electric(self):
        self.te.h2(f'Проверка терминала {self.name} REL511')
        super().get_electric()

    def get_complex(self):
        self.te.h2(f'Комплексная проверка терминала {self.name} REL511')
        super().get_complex()
