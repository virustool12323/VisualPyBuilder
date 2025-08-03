import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import VisualPyBuilderMainWindow

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("VisualPyBuilder")
    app.setApplicationVersion("1.0.0")
    
    window = VisualPyBuilderMainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()