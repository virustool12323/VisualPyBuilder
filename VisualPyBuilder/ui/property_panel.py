from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit, QCheckBox, 
    QSpinBox, QLabel, QPushButton, QGroupBox
)
from PySide6.QtCore import Qt

class PropertyPanel(QWidget):
    def __init__(self, widget_manager):
        super().__init__()
        self.widget_manager = widget_manager
        self.current_widget = None
        self.property_widgets = {}
        self.init_ui()
        
    def init_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(5, 5, 5, 5)
        
        self.info_label = QLabel("Wybierz widget, aby edytować właściwości")
        self.info_label.setWordWrap(True)
        self.layout.addWidget(self.info_label)
        
        self.properties_group = QGroupBox("Właściwości")
        self.properties_layout = QFormLayout()
        self.properties_group.setLayout(self.properties_layout)
        self.layout.addWidget(self.properties_group)
        
        self.layout.addStretch()
        
    def update_properties(self, widget_data):
        self.current_widget = widget_data
        
        # Wyczyść poprzednie właściwości
        self.clear_properties()
        
        # Ustaw nowe
        self.info_label.setText(f"Właściwości: {widget_data['type']} ({widget_data['name']})")
        
        properties = widget_data.get('properties', {})
        for prop_name, prop_value in properties.items():
            self.add_property_widget(prop_name, prop_value)
            
        self.properties_group.setVisible(True)
        
    def clear_properties(self):
        # Usuń wszystkie widgety właściwości
        for widget in self.property_widgets.values():
            self.properties_layout.removeRow(widget)
        self.property_widgets.clear()
        
    def add_property_widget(self, prop_name, prop_value):
        label = QLabel(prop_name)
        
        if isinstance(prop_value, str):
            widget = QLineEdit(prop_value)
            widget.textChanged.connect(
                lambda text, name=prop_name: self.on_property_changed(name, text)
            )
        elif isinstance(prop_value, bool):
            widget = QCheckBox()
            widget.setChecked(prop_value)
            widget.stateChanged.connect(
                lambda state, name=prop_name: self.on_property_changed(name, bool(state))
            )
        elif isinstance(prop_value, int):
            widget = QSpinBox()
            widget.setValue(prop_value)
            widget.valueChanged.connect(
                lambda value, name=prop_name: self.on_property_changed(name, value)
            )
        else:
            widget = QLabel(str(prop_value))
            
        self.property_widgets[prop_name] = widget
        self.properties_layout.addRow(label, widget)
        
    def on_property_changed(self, prop_name, value):
        if self.current_widget:
            self.widget_manager.update_widget_property(
                self.current_widget['id'], prop_name, value
            )