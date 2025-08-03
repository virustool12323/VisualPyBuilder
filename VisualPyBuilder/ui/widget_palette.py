from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QListWidget, QListWidgetItem
)
from PySide6.QtCore import Qt
from ui.drag_drop_handler import DragDropHandler

class WidgetPalette(QWidget):
    def __init__(self, widget_manager):
        super().__init__()
        self.widget_manager = widget_manager
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        
        self.list_widget = QListWidget()
        self.list_widget.setDragEnabled(True)
        self.list_widget.setDragDropMode(QListWidget.DragOnly)
        
        # Dodaj widgety do palety
        widgets = [
            ('QPushButton', 'Przycisk'),
            ('QLabel', 'Etykieta'),
            ('QLineEdit', 'Pole tekstowe'),
            ('QTextEdit', 'Obszar tekstowy'),
            ('QComboBox', 'Lista rozwijana'),
            ('QCheckBox', 'Pole wyboru'),
            ('QRadioButton', 'Przycisk radio')
        ]
        
        for widget_type, display_name in widgets:
            item = QListWidgetItem(display_name)
            item.setData(Qt.UserRole, widget_type)
            self.list_widget.addItem(item)
            
        layout.addWidget(self.list_widget)
        
        # Przycisk do testowania
        add_button = QPushButton("Dodaj testowy widget")
        add_button.clicked.connect(self.add_test_widget)
        layout.addWidget(add_button)
        
    def add_test_widget(self):
        # Tymczasowo dla testów
        current_item = self.list_widget.currentItem()
        if current_item:
            widget_type = current_item.data(Qt.UserRole)
            self.widget_manager.add_widget(widget_type)