from interfaces import element

class ETL540(element):
    tests: dict

    def get_electric(self):
        self.te.h2(f'Проверка ETL540')
        self.te.table_name('Проверка блока питания')
        self.te.table_head('Место измерения', 'Напряжение, В', 'Норма, В')
        self.te.table_row('Выход внешнего БП', self.tests['u_ps'], '-15/+20%')
        self.te.table_row('Гнездо OV-(-40-60V', self.tests['ov_40_60'], '46...52')
        self.te.table_row('Гнездо OV-BAT', self.tests['ov_bat'], '46...56')
        self.te.p('Проверено прохождение команд между защитами и ETL540')
        self.te.literalinclude(self.tests['status'], caption='Результат петлевого теста')

    def get_complex(self):
        ...