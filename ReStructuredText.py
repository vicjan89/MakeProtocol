from interfaces import TextEngine

class ReStructuredText(TextEngine):

    def h1(self, text: str):
        self.text += text + '\n' + '#' * len(text)

    def h2(self, text: str):
        self.text += text + '\n' + '*' * len(text)

    def h3(self, text: str):
        self.text += text + '\n' + '=' * len(text)

    def h4(self, text: str):
        self.text += text + '\n' + '-' * len(text)

    def p(self, text: str):
        self.text += f'\n{text}\n'

    def table_head(self, *args: str):
        line1 = '+'
        line2 = '|'
        line3 = '+'
        for col in args:
            line1 += '-' * (len(col) + 2) + '+'
            line2 += f' {col} |'
            line3 += '=' * (len(col) + 2) + '+'
        self.text += f'{line1}\n{line2}\n{line3}\n'

    def table_row(self, *args: str):
        line1 = '|'
        line2 = '+'
        for col in args:
            line1 += f' {col} |'
            line2 += '-' * (len(col) + 2) + '+'
        self.text += f'{line1}\n{line2}\n'

    def image(self, image_path: str):
        self.text += f'.. image:: {image_path}\n'

