import sqlite3

from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QGridLayout, QLabel, QDateEdit, QPushButton, QTableWidget, QTableWidgetItem, QDialog


class ReportDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Generate Report")
        self.setLayout(QGridLayout())

        # Input fields for date range
        self.layout().addWidget(QLabel("Start Date:"), 0, 0)
        self.start_date = QDateEdit()
        self.start_date.setCalendarPopup(True)  # Enable calendar popup for date selection
        self.start_date.setDisplayFormat("MM/dd/yyyy")
        self.start_date.setDate(QDate.currentDate())  # Set default date to today
        self.layout().addWidget(self.start_date, 0, 1)

        self.layout().addWidget(QLabel("End Date:"), 1, 0)
        self.end_date = QDateEdit()
        self.end_date.setCalendarPopup(True)  # Enable calendar popup for date selection
        self.end_date.setDisplayFormat("MM/dd/yyyy")
        self.end_date.setDate(QDate.currentDate())  # Set default date to today
        self.layout().addWidget(self.end_date, 1, 1)

        # Generate button
        self.generate_button = QPushButton("Generate")
        self.generate_button.clicked.connect(self.generate_report)
        self.layout().addWidget(self.generate_button, 2, 0, 1, 2)

        # Result table
        self.result_table = QTableWidget()
        self.result_table.setColumnCount(2)
        self.result_table.setHorizontalHeaderLabels(["Who Strung", "Rackets Count"])
        self.layout().addWidget(self.result_table, 3, 0, 1, 2)

    def generate_report(self):
        # Retrieve selected dates
        start_date = self.start_date.date().toString("yyyy-MM-dd")
        end_date = self.end_date.date().toString("yyyy-MM-dd")

        # Query the database
        conn = sqlite3.connect("stringing.db")
        cursor = conn.cursor()
        query = """
            SELECT who_strung, COUNT(*) AS rackets_count
            FROM StringingRecords
            WHERE date(date_strung) BETWEEN ? AND ?
            GROUP BY who_strung
            ORDER BY rackets_count DESC
        """
        cursor.execute(query, (start_date, end_date))
        results = cursor.fetchall()
        conn.close()

        # Display results in the table
        self.result_table.setRowCount(len(results))
        for row_index, (who_strung, count) in enumerate(results):
            self.result_table.setItem(row_index, 0, QTableWidgetItem(str(who_strung)))
            self.result_table.setItem(row_index, 1, QTableWidgetItem(str(count)))
