import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QFileDialog
from PyQt6.QtGui import QPainter, QColor, QTextFormat
from PyQt6.QtCore import Qt, QRect, QSize

class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor

    def sizeHint(self):
        return QSize(self.editor.line_number_area_width(), 0)

    def paintEvent(self, event):
        self.editor.line_number_area_paint_event(event)

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

class LineNumberedTextEdit(QTextEdit):
    def __init__(self):
        super().__init__()
        self.line_number_area = LineNumberArea(self)
        
        self.document().blockCountChanged.connect(self.update_line_number_area_width)
        self.verticalScrollBar().valueChanged.connect(self.line_number_area.update)
        self.textChanged.connect(self.line_number_area.update)
        self.update_line_number_area_width()

    def line_number_area_width(self):
        digits = len(str(max(1, self.document().blockCount())))
        space = 3 + self.fontMetrics().horizontalAdvance('9') * digits
        return space

    def update_line_number_area_width(self):
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.line_number_area.setGeometry(
            QRect(cr.left(), cr.top(),
                  self.line_number_area_width(), cr.height()))

    def line_number_area_paint_event(self, event):
        painter = QPainter(self.line_number_area)
        painter.fillRect(event.rect(), Qt.GlobalColor.lightGray)

        # Get the first visible block
        viewport_offset = self.verticalScrollBar().value()
        page_bottom = viewport_offset + self.viewport().height()
        
        block = self.document().begin()
        block_number = 0
        top = self.document().documentLayout().blockBoundingRect(block).top() - viewport_offset

        while block.isValid():
            bottom = top + self.document().documentLayout().blockBoundingRect(block).height()
            
            if top >= 0 and top <= page_bottom:
                number = str(block_number + 1)
                painter.setPen(Qt.GlobalColor.black)
                painter.drawText(0, int(top), self.line_number_area.width(),
                               self.fontMetrics().height(),
                               Qt.AlignmentFlag.AlignRight, number)

            block = block.next()
            top = bottom
            block_number += 1
            
            if top > page_bottom:
                break

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TextViewer()
    window.show()
    sys.exit(app.exec()) 