from PySide6.QtWidgets import (
    QMainWindow, QDockWidget, QTreeWidget, QTreeWidgetItem,
    QSplitter, QWidget, QVBoxLayout, QMenuBar, QStatusBar, QMessageBox
)
from PySide6.QtCore import Qt
from ui.widget_palette import WidgetPalette
from ui.property_panel import PropertyPanel
from ui.preview_window import PreviewWindow
from core.widget_manager import WidgetManager

class VisualPyBuilderMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.widget_manager = WidgetManager()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("VisualPyBuilder - Wizualny kreator aplikacji Python")
        self.setGeometry(100, 100, 1200, 800)
        
        # Menu
        self.create_menu()
        
        # Centralny widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Splitter główny
        main_splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(main_splitter)
        
        # Lewy panel - paleta widgetów
        self.widget_palette = WidgetPalette(self.widget_manager)
        palette_dock = QDockWidget("Paleta Widgetów")
        palette_dock.setWidget(self.widget_palette)
        self.addDockWidget(Qt.LeftDockWidgetArea, palette_dock)
        
        # Środkowy panel - edytor
        self.preview_window = PreviewWindow(self.widget_manager)
        main_splitter.addWidget(self.preview_window)
        
        # Prawy panel - właściwości
        self.property_panel = PropertyPanel(self.widget_manager)
        property_dock = QDockWidget("Właściwości")
        property_dock.setWidget(self.property_panel)
        self.addDockWidget(Qt.RightDockWidgetArea, property_dock)
        
        # Dolny panel - struktura
        self.structure_tree = QTreeWidget()
        self.structure_tree.setHeaderLabels(["Struktura Projektu"])
        structure_dock = QDockWidget("Struktura")
        structure_dock.setWidget(self.structure_tree)
        self.addDockWidget(Qt.BottomDockWidgetArea, structure_dock)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Gotowy")
        
        # Połączenia
        self.widget_manager.widget_added.connect(self.update_structure)
        self.widget_manager.widget_selected.connect(self.property_panel.update_properties)
        self.widget_manager.widget_updated.connect(self.preview_window.refresh_preview)
        
    def create_menu(self):
        menubar = self.menuBar()
        
        # Menu Plik
        file_menu = menubar.addMenu("Plik")
        
        new_action = file_menu.addAction("Nowy")
        new_action.triggered.connect(self.new_project)
        
        open_action = file_menu.addAction("Otwórz")
        open_action.triggered.connect(self.open_project)
        
        save_action = file_menu.addAction("Zapisz")
        save_action.triggered.connect(self.save_project)
        
        export_action = file_menu.addAction("Eksportuj do Python")
        export_action.triggered.connect(self.export_to_python)
        
        file_menu.addSeparator()
        exit_action = file_menu.addAction("Zamknij")
        exit_action.triggered.connect(self.close)
        
        # Menu Widok
        view_menu = menubar.addMenu("Widok")
        view_menu.addAction("Resetuj układ")
        
        # Menu Pomoc
        help_menu = menubar.addMenu("Pomoc")
        about_action = help_menu.addAction("O programie")
        about_action.triggered.connect(self.show_about)
        
    def new_project(self):
        self.widget_manager.clear()
        self.status_bar.showMessage("Nowy projekt utworzony")
        
    def open_project(self):
        self.status_bar.showMessage("Otwieranie projektu...")
        
    def save_project(self):
        self.status_bar.showMessage("Projekt zapisany")
        
    def export_to_python(self):
        try:
            from core.code_generator import CodeGenerator
            generator = CodeGenerator(self.widget_manager.widgets)
            code = generator.generate()
            
            # Zapis do pliku
            filename = "wygenerowana_aplikacja.py"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(code)
            
            QMessageBox.information(self, "Eksport", f"Kod wygenerowany i zapisany do: {filename}")
            self.status_bar.showMessage(f"Wyeksportowano do {filename}")
            
        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Błąd podczas eksportu: {str(e)}")
            
    def show_about(self):
        QMessageBox.about(self, "O programie", 
                         "VisualPyBuilder v1.0\nWizualny kreator aplikacji Python + PySide6")
                         
    def update_structure(self):
        self.structure_tree.clear()
        for widget_data in self.widget_manager.widgets:
            item = QTreeWidgetItem([f"{widget_data['type']} ({widget_data['name']})"])
            self.structure_tree.addTopLevelItem(item)