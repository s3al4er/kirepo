import sys
import os
import tarfile
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QFileDialog

class CatpkgInstaller(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Catpkg Installer')
        self.layout = QVBoxLayout()

        self.label = QLabel('Выберите .catpkg файл для установки:')
        self.layout.addWidget(self.label)

        self.choose_button = QPushButton('Выбрать файл')
        self.choose_button.clicked.connect(self.chooseFile)
        self.layout.addWidget(self.choose_button)

        self.install_button = QPushButton('Установить')
        self.install_button.clicked.connect(self.installPackage)
        self.layout.addWidget(self.install_button)

        self.setLayout(self.layout)

    def chooseFile(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, 'Выберите .catpkg файл', '', 'Catpkg Files (*.catpkg);;All Files (*)', options=options)
        if file_name:
            self.catpkg_path = file_name
            self.label.setText(f'Выбран файл: {self.catpkg_path}')

    def installPackage(self):
        if hasattr(self, 'catpkg_path'):
            # Переименование .catpkg в .tar.gz
            tarball_path = self.catpkg_path.replace('.catpkg', '.tar.gz')
            os.rename(self.catpkg_path, tarball_path)

            # Распаковка tar.gz
            with tarfile.open(tarball_path, 'r:gz') as tar:
                tar.extractall(path='.')

            # Запуск скрипта установки setuppkg.sh
            setup_script = os.path.join(os.path.dirname(tarball_path), 'setuppkg.sh')
            if os.path.exists(setup_script):
                os.system(f'bash {setup_script}')
            else:
                print(f'Ошибка: скрипт установки {setup_script} не найден.')

            # Очистка временных файлов (раскомментируйте, если нужно)
            # os.remove(tarball_path)

            self.label.setText('Установка завершена.')
        else:
            self.label.setText('Ошибка: файл не выбран.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    installer = CatpkgInstaller()
    installer.show()
    sys.exit(app.exec_())
