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

    def p(self, text: str):
        self.text += f'\n{text}\n\n'

    def table_head(self, *args: str):
        self.text += '\n.. list-table::\n   :header-rows: 1\n\n'
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

    def image(self, image_path: str):
        self.text += f'\n.. image:: {image_path}\n\n'

