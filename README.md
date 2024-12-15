
# Tennis Racket Stringing Information Tracker

This Python application is a desktop tool for managing and tracking tennis racket stringing records. It allows users to add, edit, delete, search, and report stringing records, making it ideal for personal or small business use.

## Features

- **Add/Edit/Delete Records**: Manage stringing records with details such as name, racket, string, tension, date, and stringer.
- **Search Records**: Easily find records by name using the search bar.
- **Import/Export Data**: Import data from Excel or CSV files and export records to Excel or CSV formats.
- **Generate Reports**: Create reports based on stringing records within a specific date range.
- **Database Backup**: Automatically back up the database on application launch.
- **Responsive Design**: User-friendly interface with table views and pop-up dialogs.

## Technologies Used

- **Python**: Core programming language.
- **PyQt5**: For building the graphical user interface (GUI).
- **SQLite**: Lightweight database for storing stringing records.
- **Pandas**: For handling and processing data during import/export.
- **datetime**: For date manipulation and formatting.

## Installation

1. **Clone the Repository**:

    ```bash
    git clone <repository-url>
    cd <repository-folder>
    ```

2. **Install Dependencies**:

    Make sure Python is installed on your system (version 3.7+ is recommended). Then install the required Python libraries:

    ```bash
    pip install PyQt5 pandas
    ```

3. **Run the Program**:

    ```bash
    python main.py
    ```

## How to Use

1. **Launch the Program**: Open the application by running `main.py`.
2. **Add a Record**: Click the "Add Record" button to add a new stringing record.
3. **Edit a Record**: Use the "Edit" button next to a record in the table to modify its details.
4. **Delete a Record**: Click the "Delete" button to remove a record.
5. **Search Records**: Enter a name in the search bar to filter the records.
6. **Import/Export Data**: Use the "File" menu to import or export data.
7. **Generate Reports**: Select a date range from the "File" menu to generate a report.

## File Structure

```
.
├── main.py                # Entry point for the application
├── main_window.py         # Contains the MainWindow class
├── AddEditRecordDialog.py  # Dialog for adding/editing records
├── ReportDialog.py       # Dialog for generating reports
├── database_utils.py      # Handles database setup and management
├── backup_utils.py        # Handles database backup functionality
├── README.md              # Documentation
└── stringing.db           # SQLite database (created on first run)
```

## Future Improvements

- Add user authentication for multi-user support.
- Enable cloud syncing for database backups.
- Enhance reporting with charts and graphs.


---

Enjoy tracking your tennis racket stringing records with ease!
