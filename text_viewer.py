import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QFileDialog

class TextViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Text File Viewer")
        self.setGeometry(100, 100, 800, 600)

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create text edit widget
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(False)  # Make it editable
        self.text_edit.setFontPointSize(12)  # Set initial font size
        self.text_edit.ensureCursorVisible()
        layout.addWidget(self.text_edit)

        # Create button layout
        button_layout = QHBoxLayout()
        
        # Create open file button
        open_button = QPushButton("Open File")
        open_button.clicked.connect(self.open_file)
        button_layout.addWidget(open_button)

        # Add font size buttons
        increase_font_button = QPushButton("Increase Font")
        increase_font_button.clicked.connect(self.increase_font)
        button_layout.addWidget(increase_font_button)

        decrease_font_button = QPushButton("Decrease Font")
        decrease_font_button.clicked.connect(self.decrease_font)
        button_layout.addWidget(decrease_font_button)

        # Add button layout to main layout
        layout.addLayout(button_layout)

    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Open Text File",
            "",
            "Text Files (*.txt);;All Files (*)"
        )
        
        if file_name:
            try:
                with open(file_name, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.text_edit.setText(content)
                    self.text_edit.setFocus()
            except Exception as e:
                self.text_edit.setText(f"Error opening file: {str(e)}")
                self.text_edit.setFocus()

    def increase_font(self):
        current_size = self.text_edit.fontPointSize()
        # Select all text
        cursor = self.text_edit.textCursor()
        # Save current cursor
        position = cursor.position()
        cursor.select(cursor.SelectionType.Document)
        self.text_edit.setTextCursor(cursor)
        # Increase font size
        self.text_edit.setFontPointSize(current_size + 1)
        # Restore original cursor
        cursor.setPosition(position)
        self.text_edit.setTextCursor(cursor)
        self.text_edit.ensureCursorVisible()
        self.text_edit.setFocus()

    def decrease_font(self):
        current_size = self.text_edit.fontPointSize()
        if current_size > 1:  # Prevent font from becoming too small
            # Select all text
            cursor = self.text_edit.textCursor()
            # Save current cursor
            position = cursor.position()
            cursor.select(cursor.SelectionType.Document)
            self.text_edit.setTextCursor(cursor)
            # Decrease font size
            self.text_edit.setFontPointSize(current_size - 1)
            # Restore original cursor
            cursor.setPosition(position)
            self.text_edit.setTextCursor(cursor)
            self.text_edit.ensureCursorVisible()
            self.text_edit.setFocus()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TextViewer()
    window.show()
    sys.exit(app.exec()) 