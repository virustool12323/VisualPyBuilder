from PySide6.QtCore import QObject, Signal

class WidgetManager(QObject):
    widget_added = Signal()
    widget_selected = Signal(dict)
    widget_updated = Signal()
    
    def __init__(self):
        super().__init__()
        self.widgets = []  # Lista słowników z danymi widgetów
        self.layouts = []  # Lista layoutów
        self.selected_widget = None
        
    def add_widget(self, widget_type, name=None):
        if name is None:
            name = f"{widget_type.lower()}_{len(self.widgets) + 1}"
            
        widget_data = {
            'id': len(self.widgets),
            'type': widget_type,
            'name': name,
            'properties': self.get_default_properties(widget_type)
        }
        
        self.widgets.append(widget_data)
        self.widget_added.emit()
        return widget_data
        
    def add_layout(self, layout_type, name=None):
        if name is None:
            name = f"{layout_type.lower()}_{len(self.layouts) + 1}"
            
        layout_data = {
            'id': len(self.layouts),
            'type': layout_type,
            'name': name,
            'widgets': []
        }
        
        self.layouts.append(layout_data)
        self.widget_added.emit()
        return layout_data
        
    def get_default_properties(self, widget_type):
        defaults = {
            'QPushButton': {'text': 'Przycisk', 'enabled': True},
            'QLabel': {'text': 'Etykieta', 'alignment': 'AlignLeft'},
            'QLineEdit': {'placeholderText': '', 'enabled': True},
            'QTextEdit': {'plainText': '', 'enabled': True},
            'QComboBox': {'items': [], 'currentIndex': 0},
            'QCheckBox': {'text': 'Checkbox', 'checked': False},
            'QRadioButton': {'text': 'Radio', 'checked': False}
        }
        return defaults.get(widget_type, {})
        
    def select_widget(self, widget_data):
        self.selected_widget = widget_data
        self.widget_selected.emit(widget_data)
        
    def update_widget_property(self, widget_id, property_name, value):
        for widget in self.widgets:
            if widget['id'] == widget_id:
                widget['properties'][property_name] = value
                self.widget_updated.emit()
                break
                
    def clear(self):
        self.widgets = []
        self.layouts = []
        self.selected_widget = None
        self.widget_added.emit()