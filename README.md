# PyQt6 TextEdit with Autocompletion

A custom implementation of `QTextEdit` from PyQt6 that features an integrated autocompletion mechanism.

## Features

- Autocompletion using `QCompleter`.
- Case-insensitive matching.
- Easy to extend and integrate into existing PyQt6 applications.

## Prerequisites

- Make sure you have PyQt6 installed.

```bash
pip install pyqt6
```

## Usage
To use the custom `TextEdit` in your PyQt6 application:

```python
from TextEdit import TextEdit
```

Then, integrate `TextEdit` into your PyQt6 application as you would with any other widget.

### Example

```python
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

```