import sys
import hashlib
import requests
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QFileDialog, QMessageBox

# BUF_SIZE выбирается произвольно, можно изменить под свои нужды!
BUF_SIZE = 65536  # читаем данные блоками по 64 Кбайта

class KISecurityApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("KISecurity")

        self.file_label = QLabel("Файл не выбран.")
        self.scan_button = QPushButton("Выбрать файл и отсканировать")
        self.scan_button.clicked.connect(self.browse_file)

        layout = QVBoxLayout()
        layout.addWidget(self.file_label)
        layout.addWidget(self.scan_button)

        self.setLayout(layout)

    def browse_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Выберите файл")
        if filename:
            self.file_label.setText(f"Выбранный файл: {filename}")
            self.scan_file(filename)

    def scan_file(self, filename):
        try:
            sha256 = hashlib.sha256()
            with open(filename, 'rb') as f:
                while True:
                    data = f.read(BUF_SIZE)
                    if not data:
                        break
                    sha256.update(data)
            hashfunc = sha256.hexdigest()

            print("SHA256 Хеш:", hashfunc)

            page = requests.get("https://www.virustotal.com/en/file/" + hashfunc + "/analysis/")
            soup = BeautifulSoup(page.content, 'html.parser')
            title = (soup.find_all('meta', attrs={'name': 'description'}))
            result = title[0]['content'] if title else "Данные не найдены. Сайт может быть занят. Попробуйте позже."

            if "обнаружено" in result:
                QMessageBox.warning(self, "Результат VirusTotal", result)
            else:
                QMessageBox.information(self, "Результат VirusTotal", "Файл не найден в базе данных VirusTotal.")

        except FileNotFoundError:
            QMessageBox.critical(self, "Ошибка", "Файл не найден.")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    kisecurity_app = KISecurityApp()
    kisecurity_app.show()
    sys.exit(app.exec_())