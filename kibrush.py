import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QFileDialog, QColorDialog, QVBoxLayout, QHBoxLayout, QWidget, QPushButton
from PyQt5.QtGui import QIcon, QPainter, QPen, QColor, QImage
from PyQt5.QtCore import Qt, QPoint


class PaintApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Kibrush')
        self.setGeometry(100, 100, 800, 600)

        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(Qt.white)
        self.last_point = QPoint()

        main_menu = self.menuBar()
        file_menu = main_menu.addMenu('File')
        color_menu = main_menu.addMenu('Color')

        # Create actions for File menu
        save_action = QAction('Save', self)
        save_action.triggered.connect(self.save)
        file_menu.addAction(save_action)

        open_action = QAction('Open', self)
        open_action.triggered.connect(self.open)
        file_menu.addAction(open_action)

        # Create actions for Color menu
        color_action = QAction('Choose Color', self)
        color_action.triggered.connect(self.choose_color)
        color_menu.addAction(color_action)

        self.canvas = PaintCanvas(self)
        self.setCentralWidget(self.canvas)

    def save(self):
        file_path, _ = QFileDialog.getSaveFileName(self, 'Save Image', '', 'PNG(*.png);;JPEG(*.jpg *.jpeg)')
        if file_path:
            self.image.save(file_path)

    def open(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open Image', '', 'Images (*.png *.jpg *.jpeg)')
        if file_path:
            self.image = QImage(file_path)
            self.canvas.update()

    def choose_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.canvas.set_pen_color(color)

    def closeEvent(self, event):
        if self.maybe_save():
            event.accept()
        else:
            event.ignore()

    def maybe_save(self):
        return True  # Implement saving check if needed


class PaintCanvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.pen_color = Qt.black
        self.last_point = QPoint()

    def set_pen_color(self, color):
        self.pen_color = color

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(self.rect(), self.parent.image, self.parent.image.rect())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.last_point = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            painter = QPainter(self.parent.image)
            painter.setPen(QPen(self.pen_color, 5, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.drawLine(self.last_point, event.pos())
            self.last_point = event.pos()
            self.update()

    def sizeHint(self):
        return self.parent.size()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PaintApp()
    window.show()
    sys.exit(app.exec_())
