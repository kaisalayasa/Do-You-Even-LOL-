import sys
import random
import os
import json
import requests
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QMessageBox
)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QByteArray
from PyQt5.QtWidgets import QSizePolicy




def load_champions(json_path='champions.json'):
    if not os.path.exists(json_path):
        print(f"Champions file not found at: {os.path.abspath(json_path)}")
        return {}
    try:
        with open(json_path, 'r') as f:
            champ_data = json.load(f)
            print("Champions data loaded successfully.")
            return champ_data
    except json.JSONDecodeError as e:
        print(f"Error decoding champions JSON: {e}")
        return {}
    except Exception as e:
        print(f"Unexpected error loading champions: {e}")
        return {}


def choose_random_ability(champ_list, champ_data, ability_list_choices):
    while True:
        random_champ = random.choice(champ_list)
        random_ability = random.choice(ability_list_choices)
        ability_info = champ_data.get(random_champ, {}).get(random_ability)
        if ability_info:
            ability_name = ability_info.get('name', 'Unknown Ability')
            ability_icon = ability_info.get('icon', '')
            return ability_name, ability_icon, random_ability, random_champ



class SimpleGUI(QWidget):
    def __init__(self, config, champ_data):
        super().__init__()
        self.config = config
        self.champ_data = champ_data
        self.champ_list = list(champ_data.keys())
        self.ability_list_choices = ['Passive', 'Q', 'W', 'E', 'R']
        self.streak = 0
        self.current_ability = None
        self.initUI()
        self.start_new_round()

    def initUI(self):
        self.setWindowTitle('do you even lol')
        self.setGeometry(100, 100, 800, 600)

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(20, 20, 20, 20)

        self.streak_label = QLabel(f"Streak: {self.streak}")
        self.streak_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.streak_label.setStyleSheet("""
            color: white; 
            font-size: 18px; 
            background-color: #222; 
            border: 2px solid #555; 
            padding: 5px;
            border-radius: 5px;
        """)
        self.streak_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)  # Ensure it only takes as much space as needed
        self.main_layout.addWidget(self.streak_label)



        self.background_label = QLabel(self)
        background_path = self.config.get("background_image_path", "doyouevenlol.jpg")
        self.background_pixmap = QPixmap(background_path) if os.path.exists(background_path) else None
        self.update_background_image()
        self.background_label.lower()

        self.central_layout = QVBoxLayout()
        self.central_layout.setAlignment(Qt.AlignCenter)

        self.central_image = QLabel()
        self.central_image.setAlignment(Qt.AlignCenter)
        self.central_image.setStyleSheet("""
            border: 3px solid #b8860b;
            background-color: #222;
        """)
        self.central_layout.addWidget(self.central_image)

        self.ability_name_label = QLabel("Ability Name")
        self.ability_name_label.setAlignment(Qt.AlignCenter)
        self.ability_name_label.setStyleSheet("""
            color: white;
            font-size: 20px;
            background-color: #333;
            border: 2px solid #555;
            padding: 5px;
        """)
        self.central_layout.addWidget(self.ability_name_label)

        self.main_layout.addLayout(self.central_layout)

        self.button_layout = QHBoxLayout()
        self.button_layout.setSpacing(20)
        self.button_layout.setAlignment(Qt.AlignCenter)

        buttons_info = [
            ('Passive', self.on_passive_clicked),
            ('Q', self.on_q_clicked),
            ('W', self.on_w_clicked),
            ('E', self.on_e_clicked),
            ('R', self.on_r_clicked)
        ]

        for name, func in buttons_info:
            button = QPushButton(name)
            button.setFixedSize(100, 40)
            button.setStyleSheet("""
                QPushButton {
                    font-size: 16px;
                    background-color: #444;
                    color: white;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #555;
                }
                QPushButton:pressed {
                    background-color: #333;
                }
            """)
            button.clicked.connect(func)
            self.button_layout.addWidget(button)

        self.main_layout.addLayout(self.button_layout)

        self.feedback_label = QLabel("")
        self.feedback_label.setAlignment(Qt.AlignCenter)
        self.feedback_label.setStyleSheet("color: yellow; font-size: 16px;")
        self.main_layout.addWidget(self.feedback_label)

        self.details_widget = QWidget()
        self.details_layout = QHBoxLayout()
        self.details_layout.setAlignment(Qt.AlignCenter)

        self.champ_ability_label = QLabel("")
        self.champ_ability_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.champ_ability_label.setStyleSheet("color: white; font-size: 16px;")
        self.details_layout.addWidget(self.champ_ability_label)

        self.details_widget.setLayout(self.details_layout)
        self.details_widget.hide()
        self.main_layout.addWidget(self.details_widget)

        self.setLayout(self.main_layout)

    def start_new_round(self):
        self.feedback_label.setText("")
        self.details_widget.hide()

        self.current_ability = choose_random_ability(self.champ_list, self.champ_data, self.ability_list_choices)
        ability_name, ability_icon, _, _ = self.current_ability

        self.central_pixmap = self.load_image_from_url(ability_icon)
        if self.central_pixmap is not None and not self.central_pixmap.isNull():
            scaled_pixmap = self.central_pixmap.scaled(256, 256, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.central_image.setPixmap(scaled_pixmap)
        else:
            self.central_image.setText("Ability Image")
            self.central_image.setAlignment(Qt.AlignCenter)
            self.central_image.setStyleSheet("color: white; font-size: 16px;")

        self.ability_name_label.setText(ability_name)

    def load_image_from_url(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            image_data = response.content
            pixmap = QPixmap()
            if pixmap.loadFromData(QByteArray(image_data)):
                return pixmap
            else:
                return None
        except requests.exceptions.RequestException:
            return None

    def handle_guess(self, guessed_ability_type):
        actual_ability_type = self.current_ability[2]
        if guessed_ability_type == actual_ability_type:
            self.streak += 1
            self.streak_label.setText(f"Streak: {self.streak}")
            self.feedback_label.setText("Correct!")
            self.feedback_label.setStyleSheet("color: green; font-size: 16px;")
            self.start_new_round()
        else:
            self.feedback_label.setText("Wrong Guess!")
            self.feedback_label.setStyleSheet("color: red; font-size: 16px;")
            self.end_game()

    def on_passive_clicked(self):
        self.handle_guess('Passive')

    def on_q_clicked(self):
        self.handle_guess('Q')

    def on_w_clicked(self):
        self.handle_guess('W')

    def on_e_clicked(self):
        self.handle_guess('E')

    def on_r_clicked(self):
        self.handle_guess('R')

    def end_game(self):
   
        ability_name, _, ability_type, champ_name = self.current_ability

        msg = QMessageBox()
        msg.setWindowTitle("Game Over")
        msg.setText(f"Incorrect Guess!\nYour streak: {self.streak}\n\n"
                    f"Champion: {champ_name}\nAbility: {ability_name} ({ability_type})")
        msg.setIcon(QMessageBox.Warning)
        msg.setStandardButtons(QMessageBox.Retry | QMessageBox.Close)
        msg.setDefaultButton(QMessageBox.Retry)
        ret = msg.exec_()

        if ret == QMessageBox.Retry:
            self.streak = 0
            self.streak_label.setText(f"Streak: {self.streak}")
            self.start_new_round()
        else:
            QApplication.quit()


    def resizeEvent(self, event):
        self.update_background_image()
        super().resizeEvent(event)

    def update_background_image(self):
        if self.background_pixmap:
            self.background_label.setPixmap(self.background_pixmap.scaled(
                self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation))
            self.background_label.setGeometry(0, 0, self.width(), self.height())




def load_config(json_path='config.json'):
    if not os.path.exists(json_path):
        print(f"Configuration file not found at: {os.path.abspath(json_path)}")
        return {}
    try:
        with open(json_path, 'r') as file:
            config = json.load(file)
            print("Configuration loaded successfully.")
            return config
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON configuration: {e}")
        return {}
    except Exception as e:
        print(f"Unexpected error loading configuration: {e}")
        return {}




def main():
    champ_data = load_champions('champions.json')
    if not champ_data:
        print("No champion data available. Exiting application.")
        sys.exit(1)

    config = load_config('config.json')

    app = QApplication(sys.argv)

    app_icon_path = config.get("lol icon.png", "lol icon.png")
    if os.path.exists(app_icon_path):
        app.setWindowIcon(QIcon(app_icon_path))

    gui = SimpleGUI(config, champ_data)
    gui.show()

    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()
