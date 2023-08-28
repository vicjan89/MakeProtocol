from interfaces import TextEngine

class ReStructuredText(TextEngine):

    def h1(self, text: str):
        self.text += '\n' + text + '\n' + '#' * len(text) + '\n\n'

    def h2(self, text: str):
        self.text += '\n' + text + '\n' + '*' * len(text) + '\n\n'

    def h3(self, text: str):
        self.text += '\n' + text + '\n' + '=' * len(text) + '\n\n'

    def h4(self, text: str):
        self.text += '\n' + text + '\n' + '-' * len(text) + '\n\n'

    def h5(self, text: str):
        self.text += '\n' + text + '\n' + '^' * len(text) + '\n\n'

    def p(self, text: str):
        self.text += f'\n{text}\n\n'

    def table_name(self, name: str = ''):
        self.text += f'\n.. list-table:: {name}\n   :header-rows: 1\n'

    def table_head(self, *args: str):
        num = len(args)
        widths = int(100 / num)
        s = [f'{widths}' for i in range(num)]
        s = ', '.join(s)
        self.text += f'   :widths: {s}\n\n'
        first = '   *'
        for col in args:
            self.text += f'{first} - {col}\n'
            if first == '   *':
                first = '    '

    def table_row(self, *args: str):
        first = '   *'
        for col in args:
            self.text += f'{first} - {col}\n'
            if first == '   *':
                first = '    '

    def image(self, image_path: str, name: str = ''):
        self.text += f'\n.. figure:: {image_path}\n\n   {name}\n\n'

    def warning(self, text: str):
        self.text += f'.. warning:: {text}\n\n'

    def tip(self, text: str):
        self.text += f'.. tip:: {text}\n\n'
