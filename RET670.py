from pydantic import field_validator, BaseModel


from interfaces import Terminal, AnalogInputs, CBASVAL, Channel
from T3WPDIF import T3WPDIF
from CVGAPC import CVGAPC
from OC4PTOC import OC4PTOC
from ROV2PTOV import ROV2PTOV
from FUFSPVC import FUFSPVC




class TRM_7I_5U(AnalogInputs):

    # CTPrim1: int = 3000
    # CTsec1: int = 1
    # CTPrim2: int =3000
    # CTsec2: int = 1
    # CTPrim3: int = 3000
    # CTsec3: int = 1
    # CTPrim4: int = 3000
    # CTsec4: int = 1
    # CTPrim5: int = 3000
    # CTsec5: int = 1
    # CTPrim6: int = 3000
    # CTsec6: int = 1
    # CTPrim7: int = 3000
    # CTsec7: int =1
    # VTPrim8: float = 400
    # VTsec8: float = 110
    # VTPrim9: float = 400
    # VTsec9: float = 110
    # VTPrim10: float = 400
    # VTsec10: float = 110
    # VTPrim11: float = 400
    # VTsec11: float = 110
    # VTPrim12: float = 400
    # VTsec12: float = 110

    @field_validator('channels')
    @classmethod
    def validate_CTPrim(cls, v: list[Channel]) -> str:
        for item in v[:7]:
            assert 1 <= item.prim <= 99999, 'Параметр должен быть в диапазоне от 1 до 99999'
            assert 1 <= item.sec <= 10, 'Параметр должен быть в диапазоне от 1 до 10'
        for item in v[7:12]:
            assert 0.05 <= item.prim <= 2000.0, 'Параметр должен быть в диапазоне от 0.05 до 2000.0'
            assert 0.001 <= item.sec <= 999.9999, 'Параметр должен быть в диапазоне от 0.001 до 999.999'
        return v


class RET670(Terminal):
    func_classes = {'T3WPDIF': T3WPDIF,
                    'CVGAPC': CVGAPC,
                    'OC4PTOC': OC4PTOC,
                    'ROV2PTOV': ROV2PTOV,
                    'FUFSPVC': FUFSPVC}
    analog_input_classes = {'TRM_7I_5U': TRM_7I_5U}

    def __init__(self, data):
        super().__init__(data)

        self.Global_base_values = [CBASVAL(**bv) for bv in data['Global_base_values']]
        for ai in data['analog_inputs']:
            self.analog_inputs.append(self.analog_input_classes[ai['type']](name=ai['name'], channels=ai['settings']))
        for func in data['functions']:
            self.functions.append(self.func_classes[func['func']](contacts=func['contacts'], tests=func['tests'],
                                                                  analog_inputs=self.analog_inputs,
                                                                  Global_base_values=self.Global_base_values,
                                                                  ** func['settings']))

