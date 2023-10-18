from interfaces import element
from CT import CT
from VT import VT

class Function(element):
    contacts: list[str] | None = None
    tests: list | dict | None = None
    # analog_inputs: list[AnalogInputs] | None = None
    complex: list | None = None
    ct: CT | None = None
    vt: VT | None = None

    def get_complex(self, table_name: str, num_stage: int = 1):
        if self.complex:
            self.te.table_name(table_name)
            self.te.table_head('Контакт/сигнал', 'tсраб, мс', widths=(80, 20))
            for num, cont in enumerate(self.complex[num_stage]):
                if cont:
                    self.te.table_row(self.contacts[num], 'сработал' if cont == True else cont)
