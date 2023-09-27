from interfaces import element


class CT(element):
    ip: int
    is1: int
    is2: int | None = None
    is3: int | None = None
    is4: int | None = None
    tests: list | None = None

    def get_electric(self):
        self.te.h2('Проверка трансформаторов тока')
        for num, isec in enumerate(self.tests):
            self.te.table_name(f'ВАХ обмотки {num+1}')
            self.te.table_head(*isec[0])
            for n in range(1,4):
                self.te.table_row(*isec[n])
            self.te.graph_ui(isec, f'ВАХ обмотки {num+1}')

    def get_complex(self):
        ...
