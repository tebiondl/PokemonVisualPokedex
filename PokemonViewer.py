from GetPandasFromFiles import get_info_from_files, get_info_from_csv, get_info_from_csv_2, get_info_from_csv_new
from JoinPokemonTables import get_pokemon_types
from HelperFunctions import fuzzy_search_pokemon, search_word, fuzzy_search_pokemon_one
import os
import pygame
from PyQt6.QtWidgets import QWidget, QListView, QPushButton, QLabel, QVBoxLayout, QSizePolicy, QLineEdit, QHBoxLayout, QFrame, QSpacerItem, QCompleter
from PyQt6.QtCore import Qt, QStringListModel, QUrl, QFile, QTextStream
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtGui import QPixmap
from PyQt6.QtSvgWidgets import QSvgWidget

class PokemonViewer(QWidget):
    def __init__(self, pokemon_type):
        super().__init__()
        self.start_vars()
        self.get_data(pokemon_type)
        self.load_stylesheet(self.project_folder + "/pokemon_viewer_styles.css")
        self.initUI()
        
    def load_stylesheet(self, filename):
        file = QFile(filename)
        if file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
            stream = QTextStream(file)
            self.setStyleSheet(stream.readAll())
    
    def start_vars(self):
        self.actual_pokemon = 0
        self.project_folder = os.path.dirname(os.path.abspath(__file__))
        self.data_folder = self.project_folder + "\Data\PokemonData"
        self.pokemon_image_size = 200
        self.type_image_size = 30
        self.stop_audio = False
        
    def get_data(self, pokemon_type):
        #self.data_files = get_info_from_files()
        #self.data_files = get_info_from_csv()
        if pokemon_type == "Normal":
            self.data_files = get_info_from_csv_2()
        elif pokemon_type == "Custom":
            self.data_files = get_info_from_csv_new()
        else:
            self.data_files = get_info_from_csv_2()

    def initUI(self):
        self.setWindowTitle('Pokemon Data Viewer')
        self.setGeometry(100, 100, 600, 650)

        # Layout principal
        layout = QVBoxLayout()
        
        # Temporal
        pygame.mixer.init()
        # Temporal
        
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        
        layout_search = self.add_search_layout()
        layout_name_buttons = self.add_name_buttons_layout()
        layout_stats_image = self.add_stats_image_layout()
        layout_description = self.add_description_layout()
        layout_types = self.add_types_layout()

        # Añadir el layout horizontal al layout principal
        layout.addLayout(layout_search)
        layout.addLayout(layout_name_buttons)
        layout.addStretch(1)
        layout.addLayout(layout_stats_image)
        layout.addStretch(1)
        layout.addLayout(layout_description)
        layout.addStretch(1)
        layout.addLayout(layout_types)

        # Establecer el layout en la ventana
        self.setLayout(layout)
        
        self.fill_pokemon_data()
        
    def add_name_buttons_layout(self):
        b_final_layout = QHBoxLayout()
        
        # Crear y añadir el botón izquierdo
        left_button = QPushButton('<--', self)
        left_button.setProperty("class", "direction-button")
        left_button.clicked.connect(lambda: self.change_pokemon(-1))
        b_final_layout.addWidget(left_button)
        
        # Add space
        b_final_layout.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        # Add a text with the name of the first pokémon
        self.texto_nombre_pokemon = QLabel("PokemonName", self)
        self.texto_nombre_pokemon.setProperty("class", "pokemon-name-text")
        self.texto_nombre_pokemon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        b_final_layout.addWidget(self.texto_nombre_pokemon)
        
        # Add space
        b_final_layout.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        
        # Crear y añadir el botón derecho
        right_button = QPushButton('-->', self)
        right_button.setProperty("class", "direction-button")
        right_button.clicked.connect(lambda: self.change_pokemon(1))
        b_final_layout.addWidget(right_button)
        
        return b_final_layout
    
    def add_types_layout(self):
        t_final_layout = QHBoxLayout()
        
        self.type_1_image = QLabel(self)
        self.type_1_image.setFixedSize(self.type_image_size, self.type_image_size)
        pixmap = QPixmap(self.data_folder + "/PokemonTypeIcons/Steel.ico")
        pixmap = pixmap.scaled(self.type_image_size, self.type_image_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.type_1_image.setPixmap(pixmap)
        t_final_layout.addWidget(self.type_1_image)
        
        self.type1_text = QLabel("Pokemon Type 1", self)
        self.type1_text.setProperty("class", "types-text")
        t_final_layout.addWidget(self.type1_text)
        
        self.type_2_image = QLabel(self)
        self.type_2_image.setFixedSize(self.type_image_size, self.type_image_size)
        pixmap = QPixmap(self.data_folder + "/PokemonTypeIcons/Steel.ico")
        pixmap = pixmap.scaled(self.type_image_size, self.type_image_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.type_2_image.setPixmap(pixmap) 
        t_final_layout.addWidget(self.type_2_image)
        
        self.type2_text = QLabel("Pokemon Type 2", self)
        self.type2_text.setProperty("class", "types-text")
        t_final_layout.addWidget(self.type2_text)

        return t_final_layout
    
    def add_search_layout(self):
        s_final_layout = QHBoxLayout()
        
        # Create Back button
        back_button = QPushButton('Back', self)
        back_button.setProperty("class", "search-button")
        back_button.clicked.connect(self.go_back)
        s_final_layout.addWidget(back_button)
        
        # Create search bar
        self.search_pokemon_bar = QLineEdit(self)
        self.search_pokemon_bar.setProperty("class", "search-bar")
        self.search_pokemon_bar.setPlaceholderText('Search Pokemon...')
        self.search_pokemon_bar.textChanged.connect(self.update_dropdown)
        self.search_pokemon_bar.returnPressed.connect(self.search_pokemon)
        
        # Create list of similar words
        self.completer = QCompleter(self)
        self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.completer.setFilterMode(Qt.MatchFlag.MatchContains)
        self.completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        self.completer.highlighted.connect(self.select_pokemon)
        self.completer_list_view = QListView()
        self.completer.setPopup(self.completer_list_view)
        self.completer_list_view.setProperty("class", "completer-search-bar")
        self.search_pokemon_bar.setCompleter(self.completer)
        
        s_final_layout.addWidget(self.search_pokemon_bar)

        button = QPushButton('Search', self)
        button.setProperty("class", "search-button")
        button.clicked.connect(self.search_pokemon)
        s_final_layout.addWidget(button)
        
        return s_final_layout
    
    def add_description_layout(self):
        d_final_layout = QHBoxLayout()
        parent_width = self.size().width()
        
        # Crear y añadir el botón izquierdo
        self.play_desc_button = QPushButton('PLAY', self)
        self.play_desc_button.setProperty("class", "play-button")
        self.play_desc_button.clicked.connect(self.play_description_audio)
        # Can occupy max 20% of the width
        self.play_desc_button.setMaximumWidth(int(parent_width * 0.2))
        d_final_layout.addWidget(self.play_desc_button)
        
        # Add space
        d_final_layout.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        
        self.description_text = QLabel("Description", self)
        self.description_text.setProperty("class", "description-text")
        self.description_text.setWordWrap(True)
        
        # Can occupy max 80% of the width
        self.description_text.setMaximumWidth(int(parent_width * 0.8))
        
        # Add space
        d_final_layout.addSpacerItem(QSpacerItem(5, 5, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        
        d_final_layout.addWidget(self.description_text)
        
        return d_final_layout
    
    def play_description_audio(self):
        
        pokemon_name = self.data_files["Pokemon"][int(self.actual_pokemon)]["PokemonName"]
        audio_path = self.data_folder + "\DescriptionAudios\\" + pokemon_name + ".wav"
        
        # Change the pygame funct when the other thing works
        if not pygame.mixer.music.get_busy():
            #url = QUrl.fromLocalFile(audio_path)
            #self.player.setSource(url)
            #self.player.play()
            
            # Temporal
            try:
                pygame.mixer.music.load(audio_path)
                pygame.mixer.music.play()
                self.play_desc_button.setText("STOP")
            except Exception as e:
                print("No such file or directory: " + audio_path)
            # Temporal
        else:
            pygame.mixer.music.stop()
            self.play_desc_button.setText("PLAY")
            
        
    def search_pokemon(self):
        pokemon_name = self.search_pokemon_bar.text().strip()
        
        if pokemon_name == "":
            return
        
        best = fuzzy_search_pokemon_one(self.data_files["Pokemon"], pokemon_name)
        
        if best:
            self.actual_pokemon = int(best["Id"])
            self.completer.popup().hide()
            self.fill_pokemon_data()
    
    def select_pokemon(self, text):
        pokemon_id = text.split(':')[0]
        self.actual_pokemon = int(pokemon_id)
        
        self.completer.popup().hide()
        self.fill_pokemon_data()
        
    def update_dropdown(self):
        search_text = self.search_pokemon_bar.text().strip().lower()
        
        results = [f'{pokemon["Id"]}: {pokemon["PokemonName"]}' for pokemon in search_word(self.data_files["Pokemon"], search_text, 0.5)]
        
        if search_text:
            model = QStringListModel(results[:10])
            self.completer.setModel(model)
        else:
            self.completer.setModel(QStringListModel([]))
    
    def add_stats_image_layout(self):
        s_final_layout = QHBoxLayout()
        layout_textos = QVBoxLayout()
        
        # Lista de textos y valores
        textos_valores = [
            ("HP", "HPValue"),
            ("Attack", "AttackValue"),
            ("Defense", "DefenseValue"),
            ("Special Attack", "SpecialAttackValue"),
            ("Special Defense", "SpecialDefenseValue"),
            ("Speed", "SpeedValue")
        ]

        # Calcular el tamaño del texto más grande
        max_texto_width = 0
        for texto, _ in textos_valores:
            label = QLabel(texto)
            label.adjustSize()
            max_texto_width = max(max_texto_width, label.width()+10)
        
        
        self.stat_labels = []
        def crear_texto_valor(texto, valor):
            layout_horizontal = QHBoxLayout()

            texto_label = QLabel(texto, self)
            texto_label.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
            texto_label.setMaximumWidth(max_texto_width)
            layout_horizontal.addWidget(texto_label)

            # Crear el valor en negrita
            valor_label = QLabel(f"<b>{valor}</b>", self)
            layout_horizontal.addWidget(valor_label)
            
            self.stat_labels.append(valor_label)
            
            return layout_horizontal
        
        # Añadir los pares de texto y valor al layout de textos
        for texto, valor in textos_valores:
            layout_textos.addLayout(crear_texto_valor(texto, valor))
            
        s_final_layout.addLayout(layout_textos)
        
        layout_textos = None
        
        # Crear y añadir la imagen
        self.imagen_label = QLabel(self)
        self.imagen_label.setFixedSize(self.pokemon_image_size, self.pokemon_image_size)
        pixmap = QPixmap(self.data_folder + "PokemonImagesGen9/001.png")
        pixmap = pixmap.scaled(self.pokemon_image_size, self.pokemon_image_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.imagen_label.setPixmap(pixmap)
        
        s_final_layout.addWidget(self.imagen_label)
        
        return s_final_layout
        
    def fill_pokemon_data(self):
        # Add the name of the pokémon
        pokemon_info = self.data_files["Pokemon"][int(self.actual_pokemon)]
        
        # Add the stats of the pokémon
        self.texto_nombre_pokemon.setText(pokemon_info["PokemonName"])
        self.stat_labels[0].setText(str(pokemon_info["Health"]))
        self.stat_labels[1].setText(str(pokemon_info["Attack"]))
        self.stat_labels[2].setText(str(pokemon_info["Defense"]))
        self.stat_labels[3].setText(str(pokemon_info["SpecialAttack"]))
        self.stat_labels[4].setText(str(pokemon_info["SpecialDefense"]))
        self.stat_labels[5].setText(str(pokemon_info["Speed"]))
        
        # Get the image of the pokémon
        if "Normal" in pokemon_info:
            image_path = self.data_folder + "\PokemonImagesGen9\\" + str(pokemon_info["Index"]).zfill(3) + ".png"
        elif "New" in pokemon_info: 
            image_path = self.data_folder + "\\newPokemonImages\\" + pokemon_info["PokemonName"] + ".png"
        else:
            pokemon_image_name = pokemon_info["PokemonName"].lower().strip().replace(" ", "-").replace("'", "").replace(".", "-")
            image_path = self.data_folder + "PokemonImages\\" + pokemon_image_name + ".png"

        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
        else:
            pixmap = QPixmap(self.data_folder + "\\red-cross.png")
            
        pixmap = pixmap.scaled(self.pokemon_image_size, self.pokemon_image_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.imagen_label.setPixmap(pixmap)

        
        # If types are in Id get the name, if not use the actual value
        if "Type1" in pokemon_info:
            type1 = pokemon_info["Type1"]
            type2 = pokemon_info["Type2"]
        elif "Type1_Id" in pokemon_info:     
            type1, type2 = get_pokemon_types(pokemon_info, self.data_files)
        else:
            type1 = "No Type"
            type2 = "No Type"
        self.type1_text.setText(str(type1).capitalize())
        
        if str(type2) == "nan":
            type2 = ""
            
        self.type2_text.setText(str(type2).capitalize())
        # Add type images
        
        pixmap = QPixmap(self.data_folder + "/PokemonTypeIcons/" + type1 + ".ico")
        pixmap = pixmap.scaled(self.type_image_size, self.type_image_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.type_1_image.setPixmap(pixmap)
        
        if type2 != "":
            pixmap = QPixmap(self.data_folder + "/PokemonTypeIcons/" + type2 + ".ico")
            pixmap = pixmap.scaled(self.type_image_size, self.type_image_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.type_2_image.setPixmap(pixmap)
        else:
            self.type_2_image.clear()
            
        # Add the description of the pokémon
        self.description_text.setText(pokemon_info["Description"])
        
        # Delete name from search bar
        self.search_pokemon_bar.clear()
        
    def change_pokemon(self, move):
        num_pokemon = len(self.data_files["Pokemon"])
        self.actual_pokemon = (int(self.actual_pokemon) + move) % num_pokemon
        
        self.fill_pokemon_data()
    
    def go_back(self):
        from MainMenu import OptionWindow
        self.option_window = OptionWindow()
        self.option_window.setProperty("class", "main-window")
        self.option_window.show()
        self.close() 