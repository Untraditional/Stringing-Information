import sqlite3

from PyQt5.QtWidgets import QDialog, QGridLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QMessageBox
from datetime import datetime


class AddEditRecordDialog(QDialog):
    def __init__(self, parent, record=None):
        super().__init__(parent)
        self.setWindowTitle("Add/Edit Record")
        self.layout = QGridLayout(self)

        # Input fields
        self.layout.addWidget(QLabel("Name:"), 0, 0)
        self.name = QLineEdit()
        self.name.textChanged.connect(self.check_fields)
        self.layout.addWidget(self.name, 0, 1)

        self.layout.addWidget(QLabel("Racket:"), 1, 0)
        self.racket = QLineEdit()
        self.racket.textChanged.connect(self.check_fields)
        self.layout.addWidget(self.racket, 1, 1)

        self.layout.addWidget(QLabel("String:"), 2, 0)
        self.string = QLineEdit()
        self.string.textChanged.connect(self.check_fields)
        self.layout.addWidget(self.string, 2, 1)

        self.layout.addWidget(QLabel("Tension:"), 3, 0)
        self.tension = QLineEdit()
        self.tension.textChanged.connect(self.check_fields)
        self.layout.addWidget(self.tension, 3, 1)

        self.layout.addWidget(QLabel("Date (MM/DD/YYYY):"), 4, 0)
        self.date_strung = QLineEdit()
        self.date_strung.textChanged.connect(self.check_fields)
        self.layout.addWidget(self.date_strung, 4, 1)

        # Button to set current date
        self.current_date_button = QPushButton("Set to Current Date")
        self.current_date_button.clicked.connect(self.set_current_date)
        self.layout.addWidget(self.current_date_button, 4, 2)

        self.layout.addWidget(QLabel("Who Strung:"), 5, 0)
        self.who_strung = QLineEdit()
        self.who_strung.textChanged.connect(self.check_fields)
        self.layout.addWidget(self.who_strung, 5, 1)

        # Save button with horizontal centering
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_record)
        self.save_button.setEnabled(False)  # Initially disabled
        self.save_button.setDefault(True)  # Set as the default button
        self.save_button.setMinimumWidth(150)

        button_layout = QHBoxLayout()
        button_layout.addStretch()  # Add stretch to center the button
        button_layout.addWidget(self.save_button)
        button_layout.addStretch()  # Add stretch to center the button

        self.layout.addLayout(button_layout, 6, 0, 1, 3)  # Span across three columns

        # Store the record being edited
        self.record = record

        if self.record:
            self.populate_fields()

    def populate_fields(self):
        self.name.setText(self.record['name'])
        self.racket.setText(self.record['racket'])
        self.string.setText(self.record['string'])
        self.tension.setText(self.record['tension'])
        try:
            # Convert YYYY-MM-DD to MM/DD/YYYY
            date_strung = datetime.strptime(self.record['date_strung'], "%Y-%m-%d").strftime("%m/%d/%Y")
        except ValueError:
            # If the date is invalid or already in the desired format
            date_strung = self.record['date_strung']
        self.date_strung.setText(date_strung)
        self.who_strung.setText(self.record['who_strung'])
        self.check_fields()

    def set_current_date(self):
        """Set the date field to the current date."""
        current_date = datetime.now().strftime("%m/%d/%Y")
        self.date_strung.setText(current_date)

    def save_record(self):
        # Convert the input date from MM/DD/YYYY to YYYY-MM-DD
        try:
            date_strung = datetime.strptime(self.date_strung.text(), "%m/%d/%Y").strftime("%Y-%m-%d")
        except ValueError:
            QMessageBox.critical(self, "Invalid Date", "Please enter a valid date in MM/DD/YYYY format.")
            return

        conn = sqlite3.connect("stringing.db")
        cursor = conn.cursor()
        if self.record:
            cursor.execute("""
            UPDATE StringingRecords
            SET name = ?, racket = ?, string = ?, tension = ?, date_strung = ?, who_strung = ?
            WHERE id = ?
            """, (self.name.text(), self.racket.text(), self.string.text(),
                  self.tension.text(), date_strung, self.who_strung.text(), self.record['id']))
        else:
            cursor.execute("""
            INSERT INTO StringingRecords (name, racket, string, tension, date_strung, who_strung)
            VALUES (?, ?, ?, ?, ?, ?)""",
                           (self.name.text(), self.racket.text(), self.string.text(),
                            self.tension.text(), date_strung, self.who_strung.text()))
        conn.commit()
        conn.close()
        QMessageBox.information(self, "Success", "Record saved successfully!")
        self.parent().load_records()
        self.close()

    def check_fields(self):
        """Enable or disable the Save button based on field values."""
        if (self.name.text().strip() and self.racket.text().strip() and self.string.text().strip() and
                self.tension.text().strip() and self.date_strung.text().strip() and self.who_strung.text().strip()):
            self.save_button.setEnabled(True)
        else:
            self.save_button.setEnabled(False)
