from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget,
    QDialog, QLabel, QLineEdit, QTableWidget, QTableWidgetItem,
    QGridLayout, QMessageBox, QHeaderView, QHBoxLayout, QFileDialog
)
import sqlite3
import sys
import pandas as pd

# Database Setup
def setup_database():
    conn = sqlite3.connect("stringing.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS StringingRecords (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        racket TEXT NOT NULL,
        string TEXT NOT NULL,
        tension TEXT NOT NULL,
        date_strung TEXT NOT NULL,
        who_strung TEXT NOT NULL
    )""")
    conn.commit()
    conn.close()

# Add/Edit Record Dialog
class AddEditRecordDialog(QDialog):
    def __init__(self, parent, record=None):
        super().__init__(parent)
        self.setWindowTitle("Add/Edit Record")
        self.layout = QGridLayout(self)

        # Input fields
        self.layout.addWidget(QLabel("Name:"), 0, 0)
        self.name = QLineEdit()
        self.layout.addWidget(self.name, 0, 1)

        self.layout.addWidget(QLabel("Racket:"), 1, 0)
        self.racket = QLineEdit()
        self.layout.addWidget(self.racket, 1, 1)

        self.layout.addWidget(QLabel("String:"), 2, 0)
        self.string = QLineEdit()
        self.layout.addWidget(self.string, 2, 1)

        self.layout.addWidget(QLabel("Tension:"), 3, 0)
        self.tension = QLineEdit()
        self.layout.addWidget(self.tension, 3, 1)

        self.layout.addWidget(QLabel("Date (MM/DD/YYYY):"), 4, 0)
        self.date_strung = QLineEdit()
        self.layout.addWidget(self.date_strung, 4, 1)

        self.layout.addWidget(QLabel("Who Strung:"), 5, 0)
        self.who_strung = QLineEdit()
        self.layout.addWidget(self.who_strung, 5, 1)

        # Save button
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_record)
        self.layout.addWidget(self.save_button, 6, 0, 1, 2)

        # Store the record being edited
        self.record = record

        if self.record:
            self.populate_fields()

    def populate_fields(self):
        self.name.setText(self.record['name'])
        self.racket.setText(self.record['racket'])
        self.string.setText(self.record['string'])
        self.tension.setText(self.record['tension'])
        self.date_strung.setText(self.record['date_strung'])
        self.who_strung.setText(self.record['who_strung'])

    def save_record(self):
        conn = sqlite3.connect("stringing.db")
        cursor = conn.cursor()
        if self.record:
            cursor.execute("""
            UPDATE StringingRecords
            SET name = ?, racket = ?, string = ?, tension = ?, date_strung = ?, who_strung = ?
            WHERE id = ?
            """, (self.name.text(), self.racket.text(), self.string.text(),
                  self.tension.text(), self.date_strung.text(), self.who_strung.text(), self.record['id']))
        else:
            cursor.execute("""
            INSERT INTO StringingRecords (name, racket, string, tension, date_strung, who_strung)
            VALUES (?, ?, ?, ?, ?, ?)""",
                           (self.name.text(), self.racket.text(), self.string.text(),
                            self.tension.text(), self.date_strung.text(), self.who_strung.text()))
        conn.commit()
        conn.close()
        QMessageBox.information(self, "Success", "Record saved successfully!")
        self.parent().load_records()
        self.close()

# Main Window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tennis Racket Stringing Tracker")
        self.resize(1000, 600)

        # Menu Bar
        self.menu_bar = self.menuBar()
        file_menu = self.menu_bar.addMenu("File")
        export_action = file_menu.addAction("Export to File")
        export_action.triggered.connect(self.export_records)

        # Main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Search and Add Record layout
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by Name")
        self.search_input.textChanged.connect(self.load_records)
        search_layout.addWidget(self.search_input)

        self.add_button = QPushButton("Add Record")
        self.add_button.clicked.connect(self.open_add_record)
        self.add_button.setFixedWidth(200)
        search_layout.addWidget(self.add_button)

        self.layout.addLayout(search_layout)

        # Table widget
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Racket", "String", "Tension", "Date", "Who Strung", "Actions"])
        self.layout.addWidget(self.table)
        self.table.setColumnHidden(0, True)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        self.load_records()

    def open_add_record(self):
        dialog = AddEditRecordDialog(self)
        dialog.exec_()

    def open_edit_record(self, record):
        dialog = AddEditRecordDialog(self, record)
        dialog.exec_()

    def delete_record(self, record_id):
        confirm = QMessageBox.question(self, "Confirm Deletion", "Are you sure you want to delete this record?",
                                       QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.No:
            return
        conn = sqlite3.connect("stringing.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM StringingRecords WHERE id = ?", (record_id,))
        conn.commit()
        conn.close()
        self.load_records()

    def load_records(self):
        conn = sqlite3.connect("stringing.db")
        cursor = conn.cursor()
        search_query = self.search_input.text()
        query = """
        SELECT id, name, racket, string, tension, date_strung, who_strung
        FROM StringingRecords
        """
        if search_query:
            query += " WHERE name LIKE ?"
            params = (f"%{search_query}%",)
        else:
            params = ()
        query += " ORDER BY id DESC"
        cursor.execute(query, params)
        records = cursor.fetchall()
        self.table.setRowCount(len(records))
        for row_index, row_data in enumerate(records):
            for col_index, col_data in enumerate(row_data):
                if col_index < 7:
                    self.table.setItem(row_index, col_index, QTableWidgetItem(str(col_data)))

            # Add buttons for Edit and Delete
            actions_layout = QHBoxLayout()
            actions_layout.setContentsMargins(5, 5, 5, 5)  # Add padding around buttons
            actions_layout.setSpacing(10)  # Add space between buttons

            edit_button = QPushButton("Edit")
            edit_button.setMinimumWidth(50)  # Set minimum width for the button
            edit_button.clicked.connect(lambda _, r=row_data: self.open_edit_record({
                'id': r[0], 'name': r[1], 'racket': r[2], 'string': r[3], 'tension': r[4], 'date_strung': r[5],
                'who_strung': r[6]
            }))
            actions_layout.addWidget(edit_button)

            delete_button = QPushButton("Delete")
            delete_button.setMinimumWidth(50)  # Set minimum width for the button
            delete_button.clicked.connect(lambda _, record_id=row_data[0]: self.delete_record(record_id))
            actions_layout.addWidget(delete_button)

            widget = QWidget()
            widget.setLayout(actions_layout)
            self.table.setCellWidget(row_index, 7, widget)
        conn.close()

    def export_records(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Export Records", "",
                                                   "CSV Files (*.csv);;Excel Files (*.xlsx)", options=options)
        if not file_path:
            return
        conn = sqlite3.connect("stringing.db")
        query = """
        SELECT name, racket, string, tension, date_strung, who_strung
        FROM StringingRecords
        """
        try:
            data = pd.read_sql_query(query, conn)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to fetch data: {e}")
            conn.close()
            return
        conn.close()
        try:
            if file_path.endswith(".csv"):
                data.to_csv(file_path, index=False)
            elif file_path.endswith(".xlsx"):
                data.to_excel(file_path, index=False, engine="openpyxl")
            else:
                QMessageBox.warning(self, "Invalid Format", "Please select a valid file format (CSV or Excel).")
                return
            QMessageBox.information(self, "Success", f"Records exported successfully to {file_path}!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to export records: {e}")

if __name__ == "__main__":
    setup_database()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
