import sys
import os
from PokemonViewer import PokemonViewer
#from CreatePokemonWindow import PokemonCreator
from PyQt6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt, QStringListModel, QUrl, QFile, QTextStream

class OptionWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.project_folder = os.path.dirname(os.path.abspath(__file__))
        self.load_stylesheet(self.project_folder + "/pokemon_viewer_styles.css")
        
        self.setWindowTitle("Ventana de Selección")
        self.setGeometry(100, 100, 300, 400)
        
        layout = QVBoxLayout()
        
        # Add space
        layout.addSpacerItem(QSpacerItem(40, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        
        # Add a text with the name of the first pokémon
        self.title = QLabel("THE POKÉMON POKÉDEX", self)
        self.title.setProperty("class", "title-text")
        layout.addWidget(self.title)
        
        # Add space
        layout.addSpacerItem(QSpacerItem(60, 60, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        # Botón opción 1
        self.option1_button = QPushButton("Normal Pokémon", self)
        self.option1_button.setProperty("class", "title-selection-button")
        self.option1_button.clicked.connect(self.open_main_window_option1)
        layout.addWidget(self.option1_button)

        # Add space
        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        
        # Botón opción 2
        self.option2_button = QPushButton("Custom Pokémon", self)
        self.option2_button.setProperty("class", "title-selection-button")
        self.option2_button.clicked.connect(self.open_main_window_option2)
        layout.addWidget(self.option2_button)
        
        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        
        # Button to create new custom pokemon
        self.new_pokemon_button = QPushButton("Create Pokémon", self)
        self.new_pokemon_button.setProperty("class", "title-selection-button")
        self.new_pokemon_button.clicked.connect(self.open_create_pokemon_window)
        layout.addWidget(self.new_pokemon_button)

        # Add space
        layout.addSpacerItem(QSpacerItem(40, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        
        # Establecer layout
        self.setLayout(layout)
        
    def load_stylesheet(self, filename):
        file = QFile(filename)
        if file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
            stream = QTextStream(file)
            self.setStyleSheet(stream.readAll())

    def open_main_window_option1(self):
        # Abrir la ventana principal con la opción 1 seleccionada
        self.main_window = PokemonViewer(pokemon_type="Normal")
        self.main_window.setProperty("class", "main-window")
        self.main_window.show()
        self.close()  # Cerrar la ventana de selección al abrir la principal

    def open_main_window_option2(self):
        # Abrir la ventana principal con la opción 2 seleccionada
        self.main_window = PokemonViewer(pokemon_type="Custom")
        self.main_window.setProperty("class", "main-window")
        self.main_window.show()
        self.close()  # Cerrar la ventana de selección al abrir la principal
        
    def open_create_pokemon_window(self):
        #self.main_window = PokemonCreator()
        self.main_window.setProperty("class", "main-window")
        self.main_window.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Crear y mostrar la ventana de opciones
    option_window = OptionWindow()
    option_window.setProperty("class", "main-window")
    option_window.show()

    sys.exit(app.exec())