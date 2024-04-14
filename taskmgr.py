import sys
import psutil
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QPushButton, QLineEdit, QLabel, QMessageBox


class TaskManager(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Task Manager')
        self.setMinimumWidth(600)

        # Список задач
        self.task_list = QListWidget()

        # Поле ввода для команды
        self.command_input = QLineEdit()
        self.command_input.setPlaceholderText('Введите команду для выполнения')

        # Кнопки
        self.add_button = QPushButton('Добавить задачу')
        self.add_button.clicked.connect(self.add_task)
        self.kill_button = QPushButton('Завершить выбранную задачу')
        self.kill_button.clicked.connect(self.kill_selected_task)
        self.refresh_button = QPushButton('Обновить список')
        self.refresh_button.clicked.connect(self.refresh_tasks)

        # Макеты
        vbox = QVBoxLayout()
        vbox.addWidget(QLabel('Список запущенных задач:'))
        vbox.addWidget(self.task_list)

        hbox = QHBoxLayout()
        hbox.addWidget(self.command_input)
        hbox.addWidget(self.add_button)
        vbox.addLayout(hbox)

        vbox.addWidget(self.kill_button)
        vbox.addWidget(self.refresh_button)

        self.setLayout(vbox)
        self.refresh_tasks()  # При запуске приложения сразу обновляем список задач

    def refresh_tasks(self):
        self.task_list.clear()
        for proc in psutil.process_iter(['pid', 'name']):
            self.task_list.addItem(f'{proc.info["pid"]}: {proc.info["name"]}')

        self.task_list.sortItems()  # Сортируем задачи по PID

    def add_task(self):
        command = self.command_input.text().strip()
        if command:
            try:
                proc = psutil.Popen(command, shell=True)
                self.task_list.addItem(f'{proc.pid}: {command}')
                self.command_input.clear()
            except Exception as e:
                QMessageBox.critical(self, 'Ошибка', f'Не удалось запустить задачу: {e}')

    def kill_selected_task(self):
        selected_item = self.task_list.currentItem()
        if selected_item:
            task_info = selected_item.text()
            pid = int(task_info.split(':')[0].strip())
            try:
                process = psutil.Process(pid)
                process.terminate()  # Завершаем процесс
                selected_row = self.task_list.row(selected_item)
                self.task_list.takeItem(selected_row)
            except psutil.NoSuchProcess:
                QMessageBox.critical(self, 'Ошибка', 'Выбранный процесс уже завершен')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    manager = TaskManager()
    manager.show()
    sys.exit(app.exec_())
