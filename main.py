from pathlib import Path
import sys
from typing import Sequence
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, QDateEdit, QMessageBox, QFileDialog)
from forms.mainwindow.ui_mainwindow import Ui_MainWindow

from setting.settingup import Settingup, SYSTEM_ROWS

BASE_DIR = Path(__file__).parent


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.action_opendatabase.triggered.connect(self.open_db_file)
        self.ui.comboBox_tables.currentTextChanged.connect(lambda name_of_table: setupFunctional.fill_table(self.ui.tableWidget_table, name_of_table))
        self.ui.pushButton_add.clicked.connect(lambda _: setupFunctional.create_record_ref(self.ui.tableWidget_table, self.ui.comboBox_tables.currentText()))
        self.ui.pushButton_delete.clicked.connect(lambda _: setupFunctional.delete_record_ref(self.ui.tableWidget_table, self.ui.comboBox_tables.currentText()))
        self.ui.pushButton_update.clicked.connect(lambda _: setupFunctional.update_records_ref(self.ui.tableWidget_table, self.ui.comboBox_tables.currentText()))
        self.ui.pushButton_filter.clicked.connect(lambda _: setupFunctional.fill_table(self.ui.tableWidget_table, self.ui.comboBox_tables.currentText(), True))
        ###########################
        self.ui.pushButton_report.clicked.connect(lambda _: None) 
        ###########################

    def open_db_file(self) -> None | QMessageBox:
        """Trigger function to open file dialog and validate it
        - create the instance of Settingup
        - set trigger to combobox
        """
        global setupFunctional

        path_to_bd: str = QFileDialog.getOpenFileName(self, "Select database", BASE_DIR.__str__(), "Database Files (*.db)")[0]

        # Validate db's path
        if not path_to_bd:
            Settingup.clear_combobox_widget(self.ui.comboBox_tables)
            Settingup.clear_table_widget(self.ui.tableWidget_table)
            return QMessageBox.information(self, "Information", "Incorrect database's path")

        setupFunctional = Settingup(self.ui.comboBox_tables, path_to_bd)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
