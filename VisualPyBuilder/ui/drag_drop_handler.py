from PySide6.QtCore import Qt, QMimeData, QByteArray
from PySide6.QtGui import QDrag

class DragDropHandler:
    @staticmethod
    def create_drag_data(widget_type, parent=None):
        """Tworzy dane do przeciągania"""
        mime_data = QMimeData()
        mime_data.setText(widget_type)
        return mime_data
        
    @staticmethod
    def handle_drop_event(event, widget_manager):
        """Obsługuje zdarzenie upuszczenia"""
        if event.mimeData().hasText():
            widget_type = event.mimeData().text()
            widget_manager.add_widget(widget_type)
            event.acceptProposedAction()
            return True
        return False