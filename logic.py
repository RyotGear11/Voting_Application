import csv

from PyQt6.QtWidgets import *
from gui import *

class Logic(QMainWindow, Ui_MainWindow):
    def __init__(self):
        """
        Initializes the Logic class, setting up the UI
        """
        super().__init__()
        self.setupUi(self)

        self.votes = self.load_votes()

        self.john_votes: int = 0
        self.jane_votes: int = 0
        self.user_voted: bool = False

        self.radioButton_jane.setEnabled(False)
        self.radioButton_john.setEnabled(False)
        self.label_pass.setVisible(False)
        self.pushButton_results.setEnabled(False)
        self.label_already_voted.setVisible(False)
        self.pushButton_reset.setVisible(False)

        self.pushButton_id.clicked.connect(self.submit)
        self.pushButton_submit.clicked.connect(self.submit_vote)
        self.pushButton_results.clicked.connect(self.show_results)
        self.pushButton_reset.clicked.connect(self.reset)

    def load_votes(self):
        """
        Loads the 'votes.csv' file
        :return: A list of rows from 'votes.csv' file or an empty file if it doesn't exist
        """
        try:
            with open('votes.csv', 'r') as file:
                return list(csv.reader(file))
        except FileNotFoundError:
            return []

    def submit(self) -> None:
        """
        Deals with ID submission
        -If ID is valid, voter is allowed to vote
        -If ID is invalid, voter will receive an error message
        -If ID has already been used, voter will receive a message
        :return: None
        """
        try:
            id_input = self.line_id.text()

            self.label_already_voted.setVisible(False)

            if id_input == '1234567891':
                self.pushButton_reset.setVisible(True)
                return

            if not id_input.isdigit():
                raise ValueError('Try Entering ID Again. Use Only Numerical Values.')
            if len(id_input) != 8:
                raise ValueError('Try Entering ID again. ID Exceeds 8 Digits.')

            if self.id_check(id_input):
                self.label_already_voted.setVisible(True)
                self.pushButton_results.setEnabled(True)
                self.line_id.setEnabled(True)
                self.line_id.clear()
                return

            self.label_pass.setVisible(True)
            self.radioButton_jane.setEnabled(True)
            self.radioButton_john.setEnabled(True)
            self.pushButton_submit.setEnabled(True)


        except ValueError as e:
            error_message: str = str(e)
            if 'Use Only Numerical Values' in error_message:
                QMessageBox.critical(self, 'Error', str(e))
            elif 'ID Exceeds 8 Digits' in error_message:
                QMessageBox.warning(self, 'Error', str(e))
            self.line_id.clear()


    def id_check(self, voter_id):
        """
        Function checks to see if voter has already voted
        :param voter_id: ID of the voter being checked
        :return: True if ID has already voted and False if not
        """
        for row in self.votes:
            if row[0] == voter_id:
                return True
        return False

    def submit_vote(self) -> None:
        """
        Submits the vote
        -Depending on radio button selected, vote goes to John or Jane
        :return: None
        """
        if self.user_voted:
            self.label_pass.setVisible(True)
            return

        voted_can = None
        if self.radioButton_jane.isChecked():
            self.jane_votes += 1
            voted_can = 'Jane'
        elif self.radioButton_john.isChecked():
            self.john_votes += 1
            voted_can = 'John'

        if voted_can:
            self.store_csv(voted_can)
            self.votes.append([self.line_id.text(), voted_can])

        self.line_id.clear()
        self.label_pass.setVisible(False)

        self.pushButton_submit.setEnabled(False)
        self.pushButton_results.setEnabled(True)
        self.pushButton_results.setVisible(True)
        self.user_voted = True


    def store_csv(self, voted_can) -> None:
        """
        Stores vote for John or Jane in 'votes.csv' file
        :param voted_can: Name of candidate
        :return: None
        """
        vote_id = self.line_id.text()

        with open('votes.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([vote_id, voted_can])


    def show_results(self) -> None:
        """
        Shows the voter the results of the vote
        -Displays the number of votes for each candidate
        -Displays winner
        -Doing so resets the UI
        :return: None
        """
        self.john_votes = 0
        self.jane_votes = 0

        for row in self.votes:
            if row[1] == 'John':
                self.john_votes += 1
            elif row[1] == 'Jane':
                self.jane_votes += 1

        if self.john_votes > self.jane_votes:
            winner = 'John'
        elif self.jane_votes > self.john_votes:
            winner = 'Jane'
        else:
            winner = 'It\'s a tie!'

        self.reset_new()
        results = f'John: {self.john_votes} Votes\nJane: {self.jane_votes} Votes\nWinner: {winner}'
        QMessageBox.information(self, 'Voting Results', results)




    def reset_new(self) -> None:
        """
        Resets the UI to their initial state after voting or viewing results
        :return: None
        """
        self.line_id.clear()
        self.radioButton_john.setChecked(False)
        self.radioButton_jane.setChecked(False)
        self.label_already_voted.setVisible(False)
        self.pushButton_reset.setVisible(False)
        self.label_pass.setVisible(False)
        self.pushButton_results.setEnabled(False)
        self.pushButton_results.setVisible(False)
        self.pushButton_submit.setEnabled(True)
        self.user_voted = False


    def reset(self) -> None:
        """
        Resets the voting system
        -Clears the votes and all UI elements
        -Clears 'votes.csv'
        :return: None
        """
        with open('votes.csv', 'w', newline='') as file:
            pass

        self.reset_new()
        self.votes = []
        self.jane_votes = 0
        self.john_votes = 0
        self.user_voted = False