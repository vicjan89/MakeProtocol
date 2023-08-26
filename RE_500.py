from pydantic import BaseModel

class Config:

    def __init__(self, path):
        with open(path, 'r', encoding='utf-8') as file:
            self.config_text = ''
            while True:
                try:
                    line = file.readline().replace(' ', '')
                    if not line:
                        break
                    if '_N_' in line:
                        self.config_text += line
                except Exception:
                    ...

    def get_param(self, code: str) -> float:
        index_start = self.config_text.find(f'_N_{code}=') + len(code) + 4
        index_end = self.config_text.find('\n', index_start)
        text_param = self.config_text[index_start:index_end]
        return text_param

class CT(BaseModel):
    Second_current: int
    Primary_current: int

    @property
    def second_current(self):
        cs = (5, 2, 1, 0.2)
        return cs[self.Second_current]