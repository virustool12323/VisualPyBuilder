import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel
from PySide6.QtCore import Qt

def main():
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle("Testowe okno")
    window.setGeometry(100, 100, 400, 300)
    
    label = QLabel("Jeśli widzisz ten tekst, Qt działa!")
    label.setAlignment(Qt.AlignCenter)
    window.setCentralWidget(label)
    
    window.show()
    print("Testowe okno pokazane")
    sys.exit(app.exec())

if __name__ == "__main__":
    main()