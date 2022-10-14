from pathlib import Path
import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, QDateEdit, QMessageBox, QFileDialog)
from forms.mainwindow.ui_mainwindow import Ui_MainWindow

from setting.settingup import Settingup

BASE_DIR = Path(__file__).parent


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.action_opendatabase.triggered.connect(self.open_db_file)
        self.ui.comboBox_tables.currentTextChanged.connect(lambda name_of_table: setupFunctional.fill_table(self.ui.tableWidget_table, name_of_table))
        self.ui.pushButton_filter.clicked.connect(lambda _: setupFunctional.fill_table(self.ui.tableWidget_table, self.ui.comboBox_tables.currentText(), True))

    def open_db_file(self):
        """Trigger function to open file dialog
        - create the instance of Settingup
        - set trigger to combobox
        - garbage collection
        """
        global setupFunctional

        path_to_bd: str = QFileDialog.getOpenFileName(self, "Select database", BASE_DIR.__str__(), "Database Files (*.db)")[0]
        setupFunctional = Settingup(self.ui.comboBox_tables, path_to_bd) if path_to_bd != '' else 0
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
