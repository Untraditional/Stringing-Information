from PyQt5.QtWidgets import (
    QApplication
)
import sys
from backup_utils import backup_database_on_launch # used to back up the database
from main_window import MainWindow
from database_utils import setup_database


if __name__ == "__main__":
    setup_database()
    backup_database_on_launch()  # Backup the database before launching the app
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
