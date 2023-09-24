import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QCompleter, QVBoxLayout, QWidget

from TextEdit import TextEdit


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        # Sample word list for autocompletion:
        words = ["apple", "banana", "cherry", "date", "elderberry", "fig", "grape"]

        # Create a QCompleter object with the word list:
        completer = QCompleter(words)

        # Create TextEdit object and set the QCompleter:
        self.text_edit = TextEdit()
        self.text_edit.setCompleter(completer)

        layout.addWidget(self.text_edit)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.setWindowTitle("TextEdit with Autocompletion")
        self.setGeometry(100, 100, 400, 200)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
