class CodeGenerator:
    def __init__(self, widgets):
        self.widgets = widgets
        
    def generate(self):
        code = self.generate_header()
        code += self.generate_class()
        code += self.generate_main()
        return code
        
    def generate_header(self):
        return '''#!/usr/bin/env python3
# Wygenerowano za pomocą VisualPyBuilder

from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QPushButton, QLabel, QLineEdit, QTextEdit, QComboBox,
    QCheckBox, QRadioButton
)
import sys

'''
        
    def generate_class(self):
        code = '''class GeneratedApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Wygenerowana aplikacja")
        self.setGeometry(100, 100, 600, 400)
        
'''
        
        # Layout główny
        code += '        main_layout = QVBoxLayout()\n'
        
        # Generowanie widgetów
        for widget_data in self.widgets:
            widget_code = self.generate_widget(widget_data)
            code += f'        {widget_code}\n'
            
        # Dodawanie do layoutu
        for widget_data in self.widgets:
            code += f'        main_layout.addWidget(self.{widget_data["name"]})\n'
            
        code += '        self.setLayout(main_layout)\n\n'
        
        # Metody (jeśli potrzebne)
        code += self.generate_methods()
        
        code += '''
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GeneratedApp()
    window.show()
    sys.exit(app.exec())
'''
        
        return code
        
    def generate_widget(self, widget_data):
        widget_type = widget_data['type']
        name = widget_data['name']
        properties = widget_data.get('properties', {})
        
        # Tworzenie widgetu
        code = f'self.{name} = {widget_type}()'
        
        # Ustawianie właściwości
        for prop_name, prop_value in properties.items():
            if isinstance(prop_value, str):
                code += f'\n        self.{name}.set{prop_name.capitalize()}("{prop_value}")'
            elif isinstance(prop_value, bool):
                code += f'\n        self.{name}.set{prop_name.capitalize()}({str(prop_value).lower()})'
            else:
                code += f'\n        self.{name}.set{prop_name.capitalize()}({prop_value})'
                
        return code
        
    def generate_methods(self):
        # Tymczasowo puste - można rozbudować
        return '    def placeholder_method(self):\n        pass\n\n'
        
    def generate_main(self):
        return ''