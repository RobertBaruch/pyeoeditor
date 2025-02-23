from PyQt6.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, 
                            QWidget, QPushButton, QFileDialog)
from PyQt6.QtGui import QRawFont
from line_numbered_text_edit import LineNumberedTextEdit

class TextViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Text File Viewer")
        self.setGeometry(100, 100, 800, 600)

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create horizontal layout for line numbers and text edit
        editor_layout = QHBoxLayout()
        layout.addLayout(editor_layout)

        # Create text edit widget
        self.text_edit = LineNumberedTextEdit()
        self.text_edit.setReadOnly(False)
        self.text_edit.setFontPointSize(12)
        self.set_preferred_font()
        self.text_edit.ensureCursorVisible()
        editor_layout.addWidget(self.text_edit)

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

    def _change_font_size(self, delta):
        if delta < 0 and self.text_edit.fontPointSize() <= 1:  # Prevent font from becoming too small
            return
            
        # Get current cursor and scrollbar positions
        cursor = self.text_edit.textCursor()
        scrollbar = self.text_edit.verticalScrollBar()
        
        # Calculate cursor's position relative to viewport
        cursor_rect = self.text_edit.cursorRect(cursor)
        cursor_center = cursor_rect.center()
        viewport_offset = cursor_center.y()

        # Get current size and save cursor position
        current_size = self.text_edit.fontPointSize()
        position = cursor.position()
        
        # Change font size (select all text and apply new size)
        cursor.select(cursor.SelectionType.Document)
        self.text_edit.setTextCursor(cursor)
        self.text_edit.setFontPointSize(current_size + delta)
        
        # Restore cursor position
        cursor.setPosition(position)
        self.text_edit.setTextCursor(cursor)
        self.text_edit.ensureCursorVisible()

        # Where's the current cursor?
        cursor_rect = self.text_edit.cursorRect(cursor)
        cursor_center = cursor_rect.center()

        # Where's the current scrollbar?
        scrollbar = self.text_edit.verticalScrollBar()

        scrollbar_adjustment = cursor_center.y() - viewport_offset
        scrollbar.setValue(scrollbar.value() + scrollbar_adjustment)

        self.text_edit.setFocus()        

    def increase_font(self):
        self._change_font_size(1)

    def decrease_font(self):
        self._change_font_size(-1)

    def set_preferred_font(self):
        preferred_fonts = [
            "Consolas",
            "DejaVu Sans Mono",
            "Courier New",
            "Monaco",
            "Menlo"
        ]
        
        # Test characters to check (as a string)
        test_chars = "ĉĝĥĵŝŭ“”"
        
        for font_family in preferred_fonts:
            font = self.text_edit.font()
            font.setFamily(font_family)
            raw_font = QRawFont.fromFont(font)
            
            # Check if font supports all test characters
            supports_all = all(raw_font.supportsCharacter(char) for char in test_chars)
            
            if font.exactMatch() and supports_all:
                self.text_edit.setFont(font)
                print(f"Using font: {font_family}")
                return 