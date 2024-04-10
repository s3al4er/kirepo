import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QGridLayout


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Калькулятор')
        self.setGeometry(100, 100, 300, 300)

        self.layout = QVBoxLayout()
        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.layout.addWidget(self.display)

        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+',
            'C'  # Кнопка для очистки
        ]

        # Создаем сетку для размещения кнопок
        grid_layout = QGridLayout()

        # Индексы для строки и столбца в сетке
        grid_row = 0
        grid_col = 0

        for button_text in buttons:
            button = QPushButton(button_text)
            button.clicked.connect(self.on_button_click)
            grid_layout.addWidget(button, grid_row, grid_col)

            # Увеличиваем столбец
            grid_col += 1
            if grid_col > 3:
                grid_col = 0
                grid_row += 1

        # Добавляем сетку кнопок в основной макет
        self.layout.addLayout(grid_layout)
        self.setLayout(self.layout)

    def on_button_click(self):
        button_text = self.sender().text()

        if button_text == '=':
            try:
                result = str(eval(self.display.text()))
                self.display.setText(result)
            except Exception as e:
                self.display.setText('Error')
        elif button_text == 'C':
            self.display.clear()  # Очистить содержимое поля ввода
        else:
            current_text = self.display.text()
            new_text = current_text + button_text
            if self.is_valid_input(new_text):
                self.display.setText(new_text)

    def is_valid_input(self, text):
        valid_chars = set('0123456789./*-+')
        return all(char in valid_chars for char in text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec_())
