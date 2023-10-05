from interfaces import element


class SF(element):
    name: str
    location: str
    type: str
    inom: float
    tests: list

    def get_electric(self):
        self.te.p(f'{self.location} {self.name} {self.type} Iном={self.inom}А')
        for test in self.tests:
            self.te.ul(f'полюс {test[0]}: {test[1]} A  {test[2]} сек.')

    def get_complex(self):
        ...