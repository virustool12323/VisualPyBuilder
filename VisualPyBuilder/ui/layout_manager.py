from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QComboBox, QPushButton, QLabel
from PySide6.QtCore import Qt

class LayoutManager(QWidget):
    def __init__(self, widget_manager):
        super().__init__()
        self.widget_manager = widget_manager
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Wybór typu layoutu
        self.layout_combo = QComboBox()
        self.layout_combo.addItems(["VBoxLayout", "HBoxLayout", "GridLayout"])
        layout.addWidget(QLabel("Typ layoutu:"))
        layout.addWidget(self.layout_combo)
        
        # Przycisk dodawania layoutu
        add_layout_btn = QPushButton("Dodaj layout")
        add_layout_btn.clicked.connect(self.add_layout)
        layout.addWidget(add_layout_btn)
        
    def add_layout(self):
        layout_type = self.layout_combo.currentText()
        self.widget_manager.add_layout(layout_type)