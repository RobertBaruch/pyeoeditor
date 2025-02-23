from PyQt6.QtWidgets import QTextEdit
from PyQt6.QtGui import QPainter
from PyQt6.QtCore import Qt, QRect
from line_number_area import LineNumberArea

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

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
            cursor = self.textCursor()
            cursor.insertBlock()
        else:
            super().keyPressEvent(event) 