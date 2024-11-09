import os
import time
from PyQt6.QtWidgets import QWidget, QListView, QPushButton, QLabel, QVBoxLayout, QSizePolicy, QLineEdit, QHBoxLayout, QFrame, QSpacerItem, QCompleter
from PyQt6.QtCore import Qt, QStringListModel, QUrl, QFile, QTextStream, QThread
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtGui import QPixmap
from PyQt6.QtSvgWidgets import QSvgWidget
from urllib.request import urlopen
from GenerateFullPokemon import generate_pokemon

class PokemonCreator(QWidget):
    def __init__(self):
        super().__init__()
        self.start_vars()
        self.get_data()
        self.load_stylesheet(self.project_folder + "/pokemon_viewer_styles.css")
        self.initUI()
        
    def load_stylesheet(self, filename):
        file = QFile(filename)
        if file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
            stream = QTextStream(file)
            self.setStyleSheet(stream.readAll())
    
    def start_vars(self):
        self.project_folder = os.path.dirname(os.path.abspath(__file__))
        self.data_folder = self.project_folder + "\Data\PokemonData"
        
    def get_data(self):
        pass

    def initUI(self):
        self.setWindowTitle('Pokemon Data Viewer')
        self.setGeometry(100, 100, 600, 650)

        # Layout principal
        layout = QVBoxLayout()
        
        # Back button
        layout_back = self.add_back_layout()
        layout_generate = self.add_generate_layout()
        
        # Create button
        
        # Loading text
        # New Pokemon information
        
        layout.addLayout(layout_back)
        layout.addStretch(1)
        layout.addLayout(layout_generate)
        layout.addStretch(1)
        
        self.setLayout(layout)
        
    def add_generate_layout(self):
        g_final_layout = QHBoxLayout()
        
        # Create Back button
        self.generate_button = QPushButton('Generate Pokemon', self)
        self.generate_button.setProperty("class", "title-selection-button")
        self.generate_button.clicked.connect(self.generate_new_pokemon)
        g_final_layout.addWidget(self.generate_button)
        
        self.loading_text = QLabel("Not Creating", self)
        self.loading_text.setProperty("class", "pokemon-name-text")
        self.loading_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        g_final_layout.addWidget(self.loading_text)
        
        return g_final_layout
        
    def generate_new_pokemon(self):
        # Change loading text to loading and disable back and generate buttons
        self.loading_text.setText("Generating...")
        self.back_button.setEnabled(False)
        self.generate_button.setEnabled(False)
        
        # Add disabled colors
        self.generate_button.setProperty("class", "title-selection-button-disabled")
        self.generate_button.style().unpolish(self.generate_button)
        self.generate_button.style().polish(self.generate_button)
        self.generate_button.update()
        
        # Add disabled colors
        self.back_button.setProperty("class", "search-button-disabled")
        self.back_button.style().unpolish(self.back_button)
        self.back_button.style().polish(self.back_button)
        self.back_button.update()
        
        self.generator = PokemonThreadCreator()
        self.generator.finished.connect(self.generate_pokemon_finished)
        self.generator.start()
        
    def generate_pokemon_finished(self):
        self.loading_text.setText("Finished")
        self.back_button.setEnabled(True)
        self.generate_button.setEnabled(True)
        self.generate_button.setProperty("class", "title-selection-button")
        self.back_button.setProperty("class", "search-button")
        del self.generator
        # Change loading text to Finished and enable back and generate buttons
        
    def add_back_layout(self):
        s_final_layout = QHBoxLayout()
        
        # Create generate button
        self.back_button = QPushButton('Back', self)
        self.back_button.setProperty("class", "search-button")
        self.back_button.clicked.connect(self.go_back)
        s_final_layout.addWidget(self.back_button)
        
        return s_final_layout
        
    def go_back(self):
        from MainMenu import OptionWindow
        self.option_window = OptionWindow()
        self.option_window.setProperty("class", "main-window")
        self.option_window.show()
        self.close()
        
class PokemonThreadCreator(QThread):
    def __init__(self):
        super().__init__()

    def run(self):
        generate_pokemon(1)
        