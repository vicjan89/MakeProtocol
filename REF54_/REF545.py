from interfaces import Terminal



class REF545(Terminal):
    protocol: str

    def get_electric(self):
        self.te.h2('Проверка терминала REF545')
        self.te.include(self.protocol)

    def get_complex(self):
        ...
