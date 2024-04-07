# native python libraries

import os
import re
from pprint import pformat

# qt stuff
from PyQt6.QtCore import QSize, QDate, Qt
from PyQt6 import QtGui
from PyQt6.QtWidgets import (
    # high level stuff
    QMainWindow,
    # widgets
    QWidget, QPushButton, QDateEdit, QLabel, QLineEdit, QComboBox, QFileDialog,
    QCheckBox, QDialogButtonBox, QSpinBox, QTextEdit, QPlainTextEdit,
    # layout stuff
    QFrame, QSplitter, QVBoxLayout, QHBoxLayout
)

# custom functions
from utils.timestamp import timestamp_url
from utils.parsing import parse_team
from utils.csv   import validate_csv_fields, twb_csv_header, twb_csv_row, region_list, version_list


# Main window class
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("yt-timestamp-to-twb v1.0")
        self.setWindowIcon(QtGui.QIcon('assets/bigband.png'))

        #######################################################################
        ### Left pane layouting (Options form)

        # Output file
        self.outfile_name = None
        self.outfile_label = QLabel("No output csv file selected")
        self.outfile_open_button = QPushButton("Choose output csv file...")
        self.outfile_open_button.clicked.connect(self.choose_outfile)

        # Event name
        self.event_label = QLabel("Event name")
        self.event_input = QLineEdit()
        self.event_input.textChanged.connect(self.check_start_button)

        # Date picker
        self.date_label = QLabel("Event date")
        self.date_picker = QDateEdit(
            calendarPopup=True, 
            displayFormat='yyyy-MM-dd', 
            date=QDate.currentDate()
        )

        # Region selector
        self.region_label = QLabel("Event region")
        self.region_combobox = QComboBox()
        self.region_list = region_list
        self.region_combobox.addItems(self.region_list)

        # Netplay
        self.netplay_checkbox = QCheckBox("Netplay event?")
        self.netplay_checkbox.setChecked(True)

        # Version
        self.version_label = QLabel("Game version")
        self.version_combobox = QComboBox()
        self.version_list = version_list
        self.version_combobox.addItems(self.version_list)

        # URL
        self.url_label = QLabel("Vod URL")
        self.url_input = QLineEdit()
        self.url_input.textChanged.connect(self.check_start_button)

        # Start button
        self.start_button = QPushButton("Create CSV")
        self.start_button_font = self.start_button.font()
        self.start_button_font.setBold(True)
        self.start_button.setFont(self.start_button_font)
        self.start_button.clicked.connect(self.start_processing)
        self.start_button.setEnabled(False)

        self.left_pane_layout = QVBoxLayout()
        self.left_pane_layout.setContentsMargins(0,0,0,0)
        self.left_pane_layout.addWidget(self.outfile_label)
        self.left_pane_layout.addWidget(self.outfile_open_button)
        self.left_pane_layout.addWidget(self.event_label)
        self.left_pane_layout.addWidget(self.event_input)
        self.left_pane_layout.addWidget(self.date_label)
        self.left_pane_layout.addWidget(self.date_picker)
        self.left_pane_layout.addWidget(self.region_label)
        self.left_pane_layout.addWidget(self.region_combobox)
        self.left_pane_layout.addWidget(self.netplay_checkbox)
        self.left_pane_layout.addWidget(self.version_label)
        self.left_pane_layout.addWidget(self.version_combobox)
        self.left_pane_layout.addWidget(self.url_label)
        self.left_pane_layout.addWidget(self.url_input)
        self.left_pane_layout.addWidget(self.start_button)

        self.left_pane_container = QWidget()
        self.left_pane_container.setFixedSize(QSize(275,400))
        self.left_pane_container.setLayout(self.left_pane_layout)

        #######################################################################
        ### Centre pane layouting (Input box)

        self.centre_pane_label = QLabel("Paste your timestamps here")
        self.centre_pane_text = QPlainTextEdit()
        self.centre_pane_layout = QVBoxLayout()
        self.centre_pane_layout.addWidget(self.centre_pane_label)
        self.centre_pane_layout.addWidget(self.centre_pane_text)
        self.centre_pane_container = QWidget()
        self.centre_pane_container.setFixedSize(QSize(450,540))
        self.centre_pane_container.setLayout(self.centre_pane_layout)

        #######################################################################
        ### Right pane layouting (Output text console)

        # Widget that displays console output, timestamp results
        self.right_pane_label = QLabel("Console / Log")
        self.right_pane_text = QTextEdit()
        self.right_pane_text.setReadOnly(True)
        self.right_pane_text.setEnabled(False)
        self.right_pane_layout = QVBoxLayout()
        self.right_pane_layout.addWidget(self.right_pane_label)
        self.right_pane_layout.addWidget(self.right_pane_text)
        self.right_pane_container = QWidget()
        self.right_pane_container.setFixedSize(QSize(850,540))
        self.right_pane_container.setLayout(self.right_pane_layout)

        #######################################################################
        ### Main layout (Three side-by-side panes)

        self.main_layout = QHBoxLayout()
        self.main_layout.addWidget(self.left_pane_container)
        self.main_layout.addWidget(self.centre_pane_container)
        self.main_layout.addWidget(self.right_pane_container)
        self.main_container = QWidget()
        self.main_container.setLayout(self.main_layout)

        self.setCentralWidget(self.main_container)

    def choose_outfile(self):
        filename = QFileDialog.getSaveFileName(
            self, 
            caption='Save File',
            filter="Timestamp Files (*.csv)"
        )
        if filename[0]:
            self.outfile_name = filename[0]
            self.outfile_label.setText(self.outfile_name)
            self.check_start_button()

    # Enable the start button if all required options are filled in
    def check_start_button(self):
        if (self.outfile_name
           and self.event_input.text()
           and self.url_input.text()):
            self.start_button.setEnabled(True)
        else:
            self.start_button.setEnabled(False)

    def print_output_line(self, line): 
        self.right_pane_text.append(line)

    def start_processing(self):
        self.left_pane_container.setEnabled(False)
        self.centre_pane_container.setEnabled(False)
        self.right_pane_text.clear()
        self.print_output_line("Processing...")

        # extract GUI options into variables
        if self.netplay_checkbox.isChecked():
            NETPLAY = 1
        else:
            NETPLAY = 0
        EVENT        = self.event_input.text()
        DATE         = self.date_picker.date().toString(Qt.DateFormat.ISODate)
        REGION       = self.region_combobox.currentText()
        VERSION      = self.version_combobox.currentText()
        BASE_URL     = self.url_input.text()
        outfile_name = self.outfile_name
        csv_list     = [twb_csv_header()]

        mmss_pattern  =       r"(\d+):(\d+)\s+([^\s\(\<\)\>][^\(\<\)\>]*[^\s\(\<\)\>])\s*([\(\<].+[\)\>])?\s+([versuVERSU\.]+)\s+([^\s\(\<\)\>][^\(\<\)\>]*[^\s\(\<\)\>])\s*([\(\<].+[\)\>])?"
        hmmss_pattern = r"(\d+):" + mmss_pattern

        teams_all_supplied = True

        for timestamp_line in self.centre_pane_text.toPlainText().splitlines():
            p1name = "_"; p2name = "_"
            p1char1 = "N"; p1char2 = "N"; p1char3 = "N"
            p2char1 = "N"; p2char2 = "N"; p2char3 = "N"

            hmmss_match = re.search(hmmss_pattern, timestamp_line)
            mmss_match  = re.search(mmss_pattern, timestamp_line)

            # Capture group behavior depending if its a 12:34 or 1:23:45 stamp
            if hmmss_match:
                # self.print_output_line(f"Found match {timestamp_line}!")
                # self.print_output_line(pformat(hmmss_match.groups()))
                groups = hmmss_match.groups()
                h = int(groups[0])
                m = int(groups[1])
                s = int(groups[2])
                p1name = groups[3]
                p1team = groups[4]
                p2name = groups[6]
                p2team = groups[7]

            elif mmss_match:
                # self.print_output_line(f"Found mmss match {timestamp_line}!")
                # self.print_output_line(pformat(mmss_match.groups()))
                groups = mmss_match.groups()
                h = 0
                m = int(groups[0])
                s = int(groups[1])
                p1name = groups[2]
                p1team = groups[3]
                p2name = groups[5]
                p2team = groups[6]

            else: 
                self.print_output_line(f"ERROR: No match found for {timestamp_line}!")
                continue

            # Generate timestamped url
            url = timestamp_url(BASE_URL, h, m, s)

            # Parse out teams if they were supplied
            # TODO implement parse_team
            if p1team: 
                p1char1, p1char2, p1char3 = parse_team(p1team)
            else:
                teams_all_supplied = False
            if p2team:
                p2char1, p2char2, p2char3 = parse_team(p2team)
            else:
                teams_all_supplied = False

            csv_list.append(
                twb_csv_row(
                    EVENT, DATE, REGION, NETPLAY, VERSION,
                    p1name, p1char1, p1char2, p1char3,
                    p2name, p2char1, p2char2, p2char3,
                    url
                )
            )

            self.print_output_line(f"Generated row for {p1name},{p1char1},{p1char2},{p1char3},{p2name},{p2char1},{p2char2},{p2char3},{url}")


        self.print_output_line("\nFinished!")
        with open(self.outfile_name, "w") as f:
            f.write("\n".join(csv_list))
        self.print_output_line(f"CSV data written to {self.outfile_name}.")

        if not teams_all_supplied:
            self.print_output_line(f"Not all characters were specified. Remember to manually fill in teams!")

        self.left_pane_container.setEnabled(True)
        self.centre_pane_container.setEnabled(True)