from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QMessageBox
from PyQt5.QtGui import QPixmap, QFont, QIcon
from PyQt5.QtCore import Qt
from PyQt5 import uic
from sys import argv
import random


class Cards_war(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("BlackJack.ui", self)

        # * some ui changes
        self.setWindowFlag(Qt.WindowCloseButtonHint, True)
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, False)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, False)
        self.setWindowIcon(QIcon('icon/blackjack-62.png'))
        self.setFixedSize(self.size())
        self.setWindowTitle("BlackJack.ui")

        # * finding dealer cards
        self.dealer_card1 = self.findChild(QLabel, "dealer_card1")
        self.dealer_card2 = self.findChild(QLabel, "dealer_card2")
        self.dealer_card3 = self.findChild(QLabel, "dealer_card3")
        self.dealer_card4 = self.findChild(QLabel, "dealer_card4")
        self.dealer_card5 = self.findChild(QLabel, "dealer_card5")

        # * finding player cards
        self.player_card1 = self.findChild(QLabel, "player_card1")
        self.player_card2 = self.findChild(QLabel, "player_card2")
        self.player_card3 = self.findChild(QLabel, "player_card3")
        self.player_card4 = self.findChild(QLabel, "player_card4")
        self.player_card5 = self.findChild(QLabel, "player_card5")

        # * finding buttons
        self.Hit_button = self.findChild(QPushButton, "pushButton")
        self.Stand_button = self.findChild(QPushButton, "pushButton_2")
        self.reset_button = self.findChild(QPushButton, "pushButton_3")
        self.dealer_button = self.findChild(QPushButton, "pushButton_4")
        self.Start_button = self.findChild(QPushButton, "pushButton_5")

        # * finding labels
        self.dealer_points_label = self.findChild(QLabel, "dealer_points")
        self.player_points_label = self.findChild(QLabel, "player_points")

        # * connecting buttons
        self.Hit_button.clicked.connect(self.hit_button_clicked)
        self.Stand_button.clicked.connect(self.stand_button_clicked)
        self.reset_button.clicked.connect(self.reset_button_clicked)
        self.dealer_button.clicked.connect(self.dealr_button_clicked)
        self.Start_button.clicked.connect(self.start_button_clicked)

        # * inserting the deck of cards
        self.card_type = ['diamonds', 'clubs', 'hearts', 'spades']
        self.all_card = ['2', '3', '4', '5', '6', '7', '8',
                         '9', '10', 'jack', 'queen', 'king', 'ace', ]
        self.deck = {}
        for type in self.card_type:
            value = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, '1_11']
            for idx, card in enumerate(self.all_card):
                self.deck[type + '_' + card] = value[idx]

        # *save the original deck
        self.deck_original = self.deck.copy()
        # *shuffle the deck
        self.deck = self.suffeling_dec(self.deck)

        # * intial stats of the game
        self.reset_button.setEnabled(False)
        self.Stand_button.setEnabled(False)
        self.dealer_button.setEnabled(False)
        self.Hit_button.setEnabled(False)

        # * intialize the backcolor of the cards
        self.card_back = 'blue'
        self.cardback = QPixmap(
            f'fronts/{self.card_back}.svg')
        self.green_placeholde = QPixmap(
            f'fronts/Green.png')

        # * initializing the game and showing the cards

        # * status of the game
        self.statusbar.setFont(QFont("Arial", 12, QFont.Bold))
        self.show()
        

            #! 1- Intializing the game


    def cards_intialize(self):
        # * resting the game

        self.player_score = 0
        self.dealer_score = 0
        self.player_cards_num = 2
        self.dealer_cards_num = 2
        self.dealer_active_ace = 0
        self.player_active_ace = 0

        self.dealer_covered_card = ''
        self.Stand_button.setText("Stand")
        self.dealer_points_label.setText("Dealer points : ??")
        self.Is_dealer_firstcard = True
        self.Is_player_turn = False
        self.Is_player_standed = False
        self.dealer_button.setEnabled(False)
        self.Hit_button.setEnabled(True)
        self.Stand_button.setEnabled(True)
        # * dealer cards + default 2 cards by random
        self.dealer_card1_value = self.card_on_board(
            self.dealer_card1, self.dealer_score)
        # * covering dealer's first card
        self.dealer_card1.setPixmap(self.cardback)
        self.dealer_card2_value = self.card_on_board(
            self.dealer_card2, self.dealer_score)
        self.dealer_card3_value = self.card_on_board(0, self.dealer_score)
        self.dealer_card4_value = self.card_on_board(0, self.dealer_score)
        self.dealer_card5_value = self.card_on_board(0, self.dealer_score)

        self.Is_player_turn = True
        # * player cards - deafult 2 cards by random
        self.player_card1_value = self.card_on_board(
            self.player_card1, self.player_score)
        self.player_card2_value = self.card_on_board(
            self.player_card2, self.player_score)
        self.player_card3_value = self.card_on_board(0, self.player_score)
        self.player_card4_value = self.card_on_board(0, self.player_score)
        self.player_card5_value = self.card_on_board(0, self.player_score)

        # * the 6 green card places
        self.dealer_card3.setPixmap(self.green_placeholde)
        self.dealer_card4.setPixmap(self.green_placeholde)
        self.dealer_card5.setPixmap(self.green_placeholde)
        self.player_card3.setPixmap(self.green_placeholde)
        self.player_card4.setPixmap(self.green_placeholde)
        self.player_card5.setPixmap(self.green_placeholde)

        self.player_points_label.setText(
            f"Player points : {self.player_score}")
        if self.player_score < 15:
            self.Stand_button.setEnabled(False)
        self.statusbar.showMessage(f"")
        self.show_winner()

    def start_button_clicked(self):
        self.cards_intialize()
        self.Start_button.setEnabled(False)
        self.reset_button.setEnabled(True)


            #! 2- dealing the cards


    def suffeling_dec(self, deck):  # * shuffeling using Keys
        self.decK_keys = list(deck.keys())
        random.shuffle(self.decK_keys)
        self.suffled_values = []
        for key in self.decK_keys:
            if key in self.deck_original:
                self.suffled_values.append(self.deck_original[key])
        return dict(zip(self.decK_keys, self.suffled_values))

    def card_on_board(self, card, score):
        stored_score = score
        if card == 0:
            return stored_score
        else:
            card_key = list(self.deck.keys())[0]
            card_value = self.deck[card_key]
            score = self.score_calc(card_value, stored_score)
            if self.Is_player_turn:
                self.player_score = score
            else:
                self.dealer_score = score

            if self.Is_dealer_firstcard:
                self.dealer_covered_card = card_key
                self.Is_dealer_firstcard = False
            del self.deck[card_key]
            card_name = QPixmap(f'fronts/{card_key}.svg')
            card.setPixmap(card_name)
            return card_value


            #! 3- claculating the score
            
            
    def score_calc(self, card_value, score):
        stored_score = int(score)
        if card_value == '1_11':
            if stored_score < 11:
                card_value = 11
                if self.Is_player_turn:
                    self.player_active_ace += 1
                else:
                    self.dealer_active_ace += 1
            else:
                card_value = 1
        else:
            card_value = int(card_value)
        stored_score += card_value
        return stored_score

    def check_player_score(self):

        if self.player_score >= 21:
            self.show_winner()
            if self.player_active_ace > 0:
                self.player_score -= 10
                self.player_active_ace -= 1


            #! 4- showing the winner


    def check_dealer_score(self):
        if self.dealer_score >= 21:
            self.show_winner()
            if self.dealer_active_ace > 0:
                self.dealer_score -= 10
                self.dealer_active_ace -= 1

    def show_dealer_1stCard(self):
        self.dealer_card1.setPixmap(
            QPixmap(f'fronts/{self.dealer_covered_card}.svg'))

    def show_winner(self):
        if self.player_score >= 21 or self.dealer_score >= 21:
            msg = QMessageBox()

            if self.player_score == self.dealer_score == 21:
                self.show_dealer_1stCard()
                msg.setText("Push - 2 -blackjacks")
                self.statusbar.showMessage("Push - Both player and dealer have 21")
            elif self.player_score == 21 and self.dealer_score != 21:
                if self.player_cards_num == 2 :
                    msg.setText("BlackJack! You win!")
                    self.statusbar.showMessage("BlackJack! You win!")
                else:
                    msg.setText("You win! by getting 21")
                    self.statusbar.showMessage("21! You win!")
            elif self.dealer_score == 21 and self.player_score != 21:
                self.show_dealer_1stCard()
                if self.dealer_cards_num == 2:
                    msg.setText("BlackJack! Dealer wins!")
                    self.statusbar.showMessage("BlackJack! Dealer wins!")
                else :
                    msg.setText("Dealer win! by getting 21")
                    self.statusbar.showMessage("BlackJack! Dealer wins!")
            elif self.player_score > 21:
                msg.setText("You lose!")
                self.statusbar.showMessage("You lose!")
            elif self.dealer_score > 21:
                msg.setText("Dealer loses!")
                self.statusbar.showMessage("Dealer loses!")

            msg.setWindowTitle("Game Over")
            msg.setWindowIcon(QIcon("icon/question.png"))
            msg.setInformativeText("Do you want to play again?")
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msg.setStyleSheet("background-color: rgb(255,255,255)")
            ret = msg.exec()
            if ret == QMessageBox.Yes:
                self.reset_button_clicked()
            elif ret == QMessageBox.No:
                app.exit()

    def check_closer_to21(self):
        if self.player_score > self.dealer_score:
            msg = QMessageBox()
            msg.setText(
                f"Player win, [Score is : {self.player_score} to {self.dealer_score} ]")
            self.statusbar.showMessage("Player won ")
        elif self.player_score < self.dealer_score:
            msg = QMessageBox()
            msg.setText(
                f"dealer win, [score is : {self.dealer_score} to {self.player_score} ]")
            self.statusbar.showMessage("Dealer won ")
        else:
            msg = QMessageBox()
            msg.setText(
                f"draw, [score is : {self.dealer_score} to {self.player_score} ]")
            self.statusbar.showMessage("Draw ")
        msg.setWindowTitle("Game Over")
        msg.setWindowIcon(QIcon("icon/question.png"))
        msg.setInformativeText("Do you want to play again?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setStyleSheet("background-color: rgb(255,255,255)")
        ret = msg.exec()
        if ret == QMessageBox.Yes:
            self.reset_button_clicked()
        elif ret == QMessageBox.No:
            app.exit()
            
            
            #! 5- Buttons functions on clicking -- start button on #! 1 - initializing the game

    def stand_button_clicked(self):
        if not self.Is_player_standed:
            self.Hit_button.setEnabled(False)
            self.dealer_button.setEnabled(True)
            self.show_dealer_1stCard()
            self.dealer_points_label.setText(
                f"Dealer points : {self.dealer_score}")
            self.Is_player_standed = True
            self.Stand_button.setText("Dealer Stand")
        elif self.Is_player_standed:
            self.check_player_score()
            self.check_closer_to21()

    def dealr_button_clicked(self):
        self.Is_player_turn = False
        if self.dealer_cards_num == 2:
            self.dealer_card3_value = self.card_on_board(
                self.dealer_card3, self.dealer_score)

        elif self.dealer_cards_num == 3:
            self.dealer_card4_value = self.card_on_board(
                self.dealer_card4, self.dealer_score)

        elif self.dealer_cards_num == 4:
            self.dealer_card5_value = self.card_on_board(
                self.dealer_card5, self.dealer_score)
        self.dealer_cards_num += 1
        self.dealer_points_label.setText(
            f"Dealer points : {self.dealer_score}")
        self.check_dealer_score()
         
    def hit_button_clicked(self):
        # *player 1 on first hit, uncover dealer card
        if self.Is_player_turn:
            if self.player_cards_num == 2:
                self.player_card3_value = self.card_on_board(
                    self.player_card3, self.player_score)
            elif self.player_cards_num == 3:
                self.player_card4_value = self.card_on_board(
                    self.player_card4, self.player_score)
            elif self.player_cards_num == 4:
                self.player_card5_value = self.card_on_board(
                    self.player_card5, self.player_score)
            else:
                self.Hit_button.setEnabled(False)

            self.player_points_label.setText(
                f"Player points : {self.player_score}")
            if self.player_score > 15:
                self.Stand_button.setEnabled(True)
            self.player_cards_num += 1
            self.check_player_score()

    def reset_button_clicked(self):
        self.deck = self.deck_original
        self.deck = self.suffeling_dec(self.deck)
        self.cards_intialize()


app = QApplication(argv)
mainWindow = Cards_war()
app.exec_()


