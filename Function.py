from interfaces import element
from CT import CT
from VT import VT

class Function(element):
    contacts: list[str] | None = None
    tests: list | dict | None = None
    # analog_inputs: list[AnalogInputs] | None = None
    complex: list | dict | None = None
    ct: CT | None = None
    vt: VT | None = None

    def get_complex(self, table_name: str, num_stage: int = 1):
        if self.complex:
            self.te.table_name(table_name)
            self.te.table_head('Контакт/сигнал', 't,мс', 'Контакт/сигнал', 't,мс', widths=(5, 1, 5, 1))
            complex_texts = []
            for num, cont in enumerate(self.complex[num_stage]):
                if cont:
                    complex_texts.append((self.contacts[num], 'сработал' if cont == True else cont))
            if len(complex_texts) % 2:
                complex_texts.append(('',''))
            for num in range(0, len(complex_texts), 2):
                self.te.table_row(*(*complex_texts[num],*complex_texts[num+1]))
