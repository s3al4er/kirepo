import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSlider, QListWidget, QFileDialog
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent


class Kimpa(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Kimpa')
        self.setWindowIcon(QIcon('kimpa_icon.png'))

        self.player = QMediaPlayer()
        self.player.setVolume(70)  # Начальная громкость

        self.initUI()

    def initUI(self):
        # Создаем основной вертикальный layout
        main_layout = QVBoxLayout()

        # Добавляем метку для отображения текущего трека
        self.song_label = QLabel('Now Playing: Nothing')
        self.song_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.song_label)

        # Создаем кнопки воспроизведения и остановки
        control_layout = QHBoxLayout()

        # Кнопка Play (▶)
        self.play_button = QPushButton()
        self.play_button.setFont(QFont('Arial', 12))
        self.play_button.setText('▶')
        self.play_button.clicked.connect(self.playMusic)

        # Кнопка Stop (⬛)
        self.stop_button = QPushButton()
        self.stop_button.setFont(QFont('Arial', 12))
        self.stop_button.setText('⬛')
        self.stop_button.clicked.connect(self.stopMusic)

        control_layout.addStretch(1)
        control_layout.addWidget(self.play_button)
        control_layout.addWidget(self.stop_button)
        control_layout.addStretch(1)
        main_layout.addLayout(control_layout)

        # Создаем ползунок громкости
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setValue(70)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setTickInterval(10)
        self.volume_slider.setSingleStep(5)
        self.volume_slider.setToolTip('Volume')
        self.volume_slider.valueChanged.connect(self.changeVolume)
        main_layout.addWidget(self.volume_slider)

        # Создаем список истории прослушиваний
        self.history_list = QListWidget()
        self.history_list.setMaximumWidth(200)
        main_layout.addWidget(self.history_list)

        self.setLayout(main_layout)

    def playMusic(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
            self.play_button.setText('▶')
        else:
            if self.player.state() == QMediaPlayer.PausedState:
                self.player.play()
            else:
                filename, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Audio Files (*.mp3 *.wav)")
                if filename:
                    self.player.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
                    self.player.play()
                    self.song_label.setText(f'Now Playing: {filename}')
                    self.history_list.addItem(filename)

            self.play_button.setText('❚❚')

    def stopMusic(self):
        self.player.stop()
        self.play_button.setText('▶')
        self.song_label.setText('Now Playing: Nothing')

    def changeVolume(self, value):
        self.player.setVolume(value)

    def closeEvent(self, event):
        self.player.stop()
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    kimpa = Kimpa()
    kimpa.show()
    sys.exit(app.exec_())
