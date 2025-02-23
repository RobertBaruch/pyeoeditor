import sys
from PyQt6.QtWidgets import QApplication
from text_viewer import TextViewer

def main():
    app = QApplication(sys.argv)
    window = TextViewer()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
