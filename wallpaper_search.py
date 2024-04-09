#!/usr/bin/python3
import os
import sys
import requests
import threading
import random
import string
from PIL import Image
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox
 
DOWNLOAD_DIR = ""
 
def generate_id():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
 
def get_ext(url):
    ext = os.path.splitext(url)[1]
    return ext
 
def download_wallpaper(url):
    print(f"Загрузка {url}")
    res = requests.get(url, allow_redirects=True)
    download_path = os.path.join(DOWNLOAD_DIR, f"{generate_id()}{get_ext(url)}")
    open(download_path, 'wb').write(res.content)
    print(f"Загрузка завершена {url}")
        
 
def wallpaper_search_api(query):
    query_url = f"https://wallhaven.cc/api/v1/search?q={query}" 
    res = requests.get(query_url)
    response = res.json()
    dl_links = [wallpaper["path"] for wallpaper in response["data"]]
    return dl_links
 
class WallpaperDownloader(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
 
    def initUI(self):
        self.setWindowTitle('Загрузчик Обоев')
        layout = QVBoxLayout()
 
        self.query_edit = QLineEdit()
        layout.addWidget(QLabel('Поисковый запрос:'))
        layout.addWidget(self.query_edit)
 
        self.directory_edit = QLineEdit(DOWNLOAD_DIR)
        self.directory_edit.setReadOnly(True)
        layout.addWidget(QLabel('Каталог загрузки:'))
        layout.addWidget(self.directory_edit)
 
        browse_button = QPushButton('Обзор...')
        browse_button.clicked.connect(self.choose_directory)
        layout.addWidget(browse_button)
 
        download_button = QPushButton('Загрузить')
        download_button.clicked.connect(self.download)
        layout.addWidget(download_button)
 
        stop_button = QPushButton('Остановить')
        stop_button.clicked.connect(self.stop_download)
        layout.addWidget(stop_button)
 
        self.setLayout(layout)
 
    def choose_directory(self):
        directory = QFileDialog.getExistingDirectory(self, 'Выбрать каталог', DOWNLOAD_DIR)
        if directory:
            self.directory_edit.setText(directory)
 
    def download(self):
        query = self.query_edit.text().replace(' ', '+')
        if not query:
            QMessageBox.critical(self, 'Ошибка', 'Введите поисковый запрос.')
            return
 
        global DOWNLOAD_DIR
        DOWNLOAD_DIR = self.directory_edit.text()
        os.makedirs(DOWNLOAD_DIR, exist_ok=True)
 
        wallpapers = wallpaper_search_api(query)
        if not wallpapers:
            QMessageBox.information(self, 'Информация', 'Обои не найдены по данному запросу.')
            return
 
        for wallpaper in wallpapers:
            download_wallpaper(wallpaper)
            QApplication.processEvents()  # Обновляем интерфейс после каждой загрузки
 
        QMessageBox.information(self, 'Информация', 'Загрузка завершена!')
 
    def stop_download(self):
        QMessageBox.information(self, 'Информация', 'Загрузка остановлена!')
        # Можно добавить дополнительные действия по остановке загрузки здесь
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WallpaperDownloader()
    window.show()
    sys.exit(app.exec_())
