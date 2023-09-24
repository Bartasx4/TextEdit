from PyQt6.QtCore import Qt
from PyQt6.QtGui import QTextCursor, QKeyEvent
from PyQt6.QtWidgets import QTextEdit, QCompleter


class TextEdit(QTextEdit):

    def __init__(self, parent=None):
        """
        Initialize the TextEdit with an optional parent and set the initial completer to None.
        """
        super().__init__(parent)
        self.c: QCompleter | None = None

    def setCompleter(self, completer: QCompleter):
        """
        Set the QCompleter object for this TextEdit.

        Args:
            completer (QCompleter): The completer object to be set.
        """
        # Disconnect previous completer if it exists
        if self.c:
            self.c.disconnect()

        self.c = completer  # Assign the new completer

        if not self.c:
            return

        # Configure the properties for the given completer
        self.c.setWidget(self)
        self.c.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        self.c.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.c.activated[str].connect(self.insertCompletion)

    @property
    def completer(self) -> QCompleter:
        """
        Return the current completer object.

        Returns:
            QCompleter: The current completer object.
        """
        return self.c

    def insertCompletion(self, completion: str):
        """
        Insert the selected completion text at the cursor position in the TextEdit.

        Args:
            completion (str): The completion text to be inserted.
        """
        if self.c.widget() is not self:
            return

        tc = self.textCursor()
        extra = len(completion) - len(self.c.completionPrefix())
        tc.movePosition(QTextCursor.MoveOperation.Left)
        tc.movePosition(QTextCursor.MoveOperation.EndOfWord)
        tc.insertText(completion[-extra:])
        self.setTextCursor(tc)

    @property
    def textUnderCursor(self) -> str:
        """
        Extract and return the word under the cursor in the TextEdit.

        Returns:
            str: The word under the cursor.
        """
        tc = self.textCursor()
        tc.select(QTextCursor.SelectionType.WordUnderCursor)
        return tc.selectedText()

    def focusInEvent(self, e):
        """
        Override the focusInEvent. Set the widget for the completer when the TextEdit gains focus.
        """
        if self.c:
            self.c.setWidget(self)
        super().focusInEvent(e)

    def keyPressEvent(self, e: QKeyEvent):
        """
        Override the keyPressEvent to handle autocompletion logic.

        Args:
            e (QKeyEvent): The key event.
        """
        # If completer popup is visible and a known key is pressed, ignore the event
        if self.c and self.c.popup().isVisible():
            if e.key() in [Qt.Key.Key_Enter, Qt.Key.Key_Return, Qt.Key.Key_Escape, Qt.Key.Key_Tab, Qt.Key.Key_Backtab]:
                e.ignore()
                return

        isShortcut = e.modifiers() == Qt.KeyboardModifier.ControlModifier and e.key() == Qt.Key.Key_E
        if not self.c or not isShortcut:
            super().keyPressEvent(e)

        ctrlOrShift = e.modifiers() in [Qt.KeyboardModifier.ControlModifier, Qt.KeyboardModifier.ShiftModifier]
        if not self.c or (ctrlOrShift and not e.text()):
            return

        eow = "~!@#$%^&*()_+{}|:\"<>?,./;'[]\\-="  # End of word characters
        hasModifier = e.modifiers() != Qt.KeyboardModifier.NoModifier and not ctrlOrShift
        completionPrefix = self.textUnderCursor

        # Determine when to show or hide the autocompletion popup based on key press and current text
        if not isShortcut and (hasModifier or not e.text() or len(completionPrefix) < 3 or e.text()[-1] in eow):
            self.c.popup().hide()
            return

        if completionPrefix != self.c.completionPrefix():
            self.c.setCompletionPrefix(completionPrefix)
            self.c.popup().setCurrentIndex(self.c.completionModel().index(0, 0))

        # Set the geometry for the completer popup
        cr = self.cursorRect()
        cr.setWidth(self.c.popup().sizeHintForColumn(0) + self.c.popup().verticalScrollBar().sizeHint().width())
        self.c.complete(cr)
