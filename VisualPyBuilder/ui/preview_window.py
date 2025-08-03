from PySide6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QLabel
from PySide6.QtCore import Qt
from ui.drag_drop_handler import DragDropHandler

class PreviewWindow(QWidget):
    def __init__(self, widget_manager):
        super().__init__()
        self.widget_manager = widget_manager
        self.setAcceptDrops(True)  # Akceptuj przeciąganie
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Nagłówek
        header = QLabel("PODGLĄD APLIKACJI")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("background-color: #e0e0e0; padding: 5px; font-weight: bold;")
        layout.addWidget(header)
        
        # Obszar podglądu
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setAlignment(Qt.AlignTop)
        self.scroll_area.setWidget(self.content_widget)
        layout.addWidget(self.scroll_area)
        
        # Inicjalny podgląd
        self.refresh_preview()
        
    def dragEnterEvent(self, event):
        """Obsługa wejścia przeciąganego elementu"""
        if event.mimeData().hasText():
            event.acceptProposedAction()
            
    def dropEvent(self, event):
        """Obsługa upuszczenia elementu"""
        DragDropHandler.handle_drop_event(event, self.widget_manager)
        
    def refresh_preview(self):
        # Wyczyść poprzedni podgląd
        while self.content_layout.count():
            child = self.content_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
                
        # Dodaj widgety z menedżera
        for widget_data in self.widget_manager.widgets:
            preview_widget = self.create_preview_widget(widget_data)
            if preview_widget:
                self.content_layout.addWidget(preview_widget)
                
    def create_preview_widget(self, widget_data):
        widget_type = widget_data['type']
        properties = widget_data.get('properties', {})
        
        try:
            # Dynamiczne tworzenie widgetów
            import PySide6.QtWidgets as QtWidgets
            widget_class = getattr(QtWidgets, widget_type)
            widget = widget_class()
            
            # Ustawianie właściwości
            for prop_name, prop_value in properties.items():
                if hasattr(widget, f'set{prop_name.capitalize()}'):
                    setter = getattr(widget, f'set{prop_name.capitalize()}')
                    setter(prop_value)
                elif hasattr(widget, prop_name):
                    setattr(widget, prop_name, prop_value)
                    
            return widget
        except Exception as e:
            error_label = QLabel(f"Błąd: {widget_type} - {str(e)}")
            error_label.setStyleSheet("color: red;")
            return error_label