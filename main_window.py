import sqlite3

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QMainWindow, QTableWidget, \
    QHeaderView, QMessageBox, QTableWidgetItem, QFileDialog
import sqlite3
import pandas as pd
from AddEditRecordDialog import AddEditRecordDialog
from ReportDialog import ReportDialog
from datetime import datetime
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tennis Racket Stringing Information Tracker")
        self.resize(1000, 600)

        # Set custom icon for the application window
        self.setWindowIcon(QIcon("icon.ico"))

        # Menu Bar
        self.menu_bar = self.menuBar()
        file_menu = self.menu_bar.addMenu("File")
        export_action = file_menu.addAction("Export to File")
        export_action.triggered.connect(self.export_records)

        import_action = file_menu.addAction("Import from File")
        import_action.triggered.connect(self.import_records)

        report_action = file_menu.addAction("Generate Report")
        report_action.triggered.connect(self.open_report_dialog)

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
        query += " ORDER BY date(date_strung) DESC"  # Sort by date_strung in descending order
        cursor.execute(query, params)
        records = cursor.fetchall()
        self.table.setRowCount(len(records))
        for row_index, row_data in enumerate(records):
            for col_index, col_data in enumerate(row_data):
                # Convert date column from YYYY-MM-DD to MM/DD/YYYY
                if col_index == 5:  # date_strung column index
                    try:
                        col_data = datetime.strptime(col_data, "%Y-%m-%d").strftime("%m/%d/%Y")
                    except ValueError:
                        pass
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

    def import_records(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Import Records", "",
                                                   "Excel Files (*.xlsx);;CSV Files (*.csv)", options=options)
        if not file_path:
            return

        try:
            # Read the file into a DataFrame
            if file_path.endswith(".csv"):
                data = pd.read_csv(file_path)
            elif file_path.endswith(".xlsx"):
                data = pd.read_excel(file_path, engine="openpyxl")
            else:
                QMessageBox.warning(self, "Invalid Format", "Please select a valid file format (CSV or Excel).")
                return

            # Strip extra spaces from column names
            data.columns = data.columns.str.strip()

            # Validate and ensure the file has the required columns
            required_columns = ["Name", "Racket", "String", "Tension", "Date Strung", "Who Strung"]
            if not all(col in data.columns for col in required_columns):
                QMessageBox.critical(self, "Invalid File",
                                     "The file must contain the following columns:\n" + ", ".join(required_columns))
                return

            # Replace missing values with "-no data-"
            data.fillna("-no data-", inplace=True)

            conn = sqlite3.connect("stringing.db")
            cursor = conn.cursor()

            # Ensure all date entries are strings
            data["Date Strung"] = data["Date Strung"].astype(str)

            for _, row in data.iterrows():
                try:
                    # Convert date format from YYYY-MM-DD to MM/DD/YYYY if applicable
                    try:
                        date_strung = datetime.strptime(row["Date Strung"], "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
                    except ValueError:
                        # Fallback if the date format doesn't match
                        date_strung = row["Date Strung"]

                    cursor.execute("""
                        INSERT INTO StringingRecords (name, racket, string, tension, date_strung, who_strung)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (row["Name"], row["Racket"], row["String"], row["Tension"], date_strung, row["Who Strung"]))
                except Exception as e:
                    QMessageBox.warning(self, "Data Error", f"Failed to import record: {row}\nError: {e}")

            conn.commit()
            conn.close()

            QMessageBox.information(self, "Success", "Records imported successfully!")
            self.load_records()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to import records: {e}")

    def open_report_dialog(self):
        dialog = ReportDialog(self)
        dialog.exec_()
