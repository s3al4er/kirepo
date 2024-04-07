import sys
import random
import string
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
import pyperclip

class PasswordGeneratorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Создаем вертикальный layout
        layout = QVBoxLayout()

        # Создаем кнопку для генерации пароля
        generate_button = QPushButton('Сгенерировать пароль', self)
        generate_button.clicked.connect(self.generate_password)

        # Создаем кнопку для отображения информации о программе
        info_button = QPushButton('О программе', self)
        info_button.clicked.connect(self.show_info)

        # Метка для отображения сгенерированного пароля или информации о программе
        self.result_label = QLabel(self)
        self.result_label.setText('')

        # Добавляем виджеты в layout
        layout.addWidget(generate_button)
        layout.addWidget(info_button)
        layout.addWidget(self.result_label)

        # Устанавливаем layout для основного виджета (окна)
        self.setLayout(layout)

        # Устанавливаем заголовок окна
        self.setWindowTitle('Passgen')

    def generate_password(self):
        # Генерируем пароль минимум из 10 символов
        password_length = 10
        password = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=password_length))
        
        # Копируем сгенерированный пароль в буфер обмена
        pyperclip.copy(password)
        
        self.result_label.setText(f'Сгенерированный пароль: {password}')

    def show_info(self):
        # Показываем информацию о программе
        info_text = 'Passgen\nKitsaOS 1.0\n(c) KitsaStudio 2024'
        self.result_label.setText(info_text)

if __name__ == '__main__':
    # Создаем экземпляр приложения Qt
    app = QApplication(sys.argv)
    
    # Создаем экземпляр класса PasswordGeneratorApp
    window = PasswordGeneratorApp()
    
    # Отображаем окно
    window.show()
    
    # Запускаем цикл обработки событий
    sys.exit(app.exec_())
