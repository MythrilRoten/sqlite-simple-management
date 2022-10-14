# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.3.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QHBoxLayout,
    QHeaderView, QMainWindow, QMenu, QMenuBar,
    QPushButton, QSizePolicy, QStatusBar, QTableWidget,
    QTableWidgetItem, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(793, 571)
        self.action_about = QAction(MainWindow)
        self.action_about.setObjectName(u"action_about")
        self.action_instructions = QAction(MainWindow)
        self.action_instructions.setObjectName(u"action_instructions")
        self.action_opendatabase = QAction(MainWindow)
        self.action_opendatabase.setObjectName(u"action_opendatabase")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.tableWidget_table = QTableWidget(self.centralwidget)
        self.tableWidget_table.setObjectName(u"tableWidget_table")
        self.tableWidget_table.setMinimumSize(QSize(750, 0))

        self.gridLayout.addWidget(self.tableWidget_table, 1, 0, 1, 2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButton_view = QPushButton(self.centralwidget)
        self.pushButton_view.setObjectName(u"pushButton_view")
        self.pushButton_view.setMinimumSize(QSize(100, 0))

        self.horizontalLayout.addWidget(self.pushButton_view)

        self.pushButton_add = QPushButton(self.centralwidget)
        self.pushButton_add.setObjectName(u"pushButton_add")
        self.pushButton_add.setMinimumSize(QSize(100, 0))

        self.horizontalLayout.addWidget(self.pushButton_add)

        self.pushButton_filter = QPushButton(self.centralwidget)
        self.pushButton_filter.setObjectName(u"pushButton_filter")
        self.pushButton_filter.setMinimumSize(QSize(100, 0))

        self.horizontalLayout.addWidget(self.pushButton_filter)

        self.pushButton_delete = QPushButton(self.centralwidget)
        self.pushButton_delete.setObjectName(u"pushButton_delete")
        self.pushButton_delete.setMinimumSize(QSize(100, 0))

        self.horizontalLayout.addWidget(self.pushButton_delete)


        self.gridLayout.addLayout(self.horizontalLayout, 2, 1, 1, 1)

        self.comboBox_tables = QComboBox(self.centralwidget)
        self.comboBox_tables.setObjectName(u"comboBox_tables")
        self.comboBox_tables.setMinimumSize(QSize(100, 0))
        self.comboBox_tables.setMaximumSize(QSize(200, 16777215))
        self.comboBox_tables.setSizeAdjustPolicy(QComboBox.AdjustToContents)

        self.gridLayout.addWidget(self.comboBox_tables, 0, 0, 1, 1, Qt.AlignLeft)

        self.pushButton_report = QPushButton(self.centralwidget)
        self.pushButton_report.setObjectName(u"pushButton_report")
        self.pushButton_report.setMinimumSize(QSize(50, 0))
        self.pushButton_report.setMaximumSize(QSize(130, 16777215))

        self.gridLayout.addWidget(self.pushButton_report, 0, 1, 1, 1, Qt.AlignRight)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 793, 22))
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        self.menuFunction = QMenu(self.menubar)
        self.menuFunction.setObjectName(u"menuFunction")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menuFunction.menuAction())
        self.menu.addAction(self.action_about)
        self.menu.addAction(self.action_instructions)
        self.menuFunction.addAction(self.action_opendatabase)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.action_about.setText(QCoreApplication.translate("MainWindow", u"About programm", None))
        self.action_instructions.setText(QCoreApplication.translate("MainWindow", u"Instructions", None))
        self.action_opendatabase.setText(QCoreApplication.translate("MainWindow", u"Open database", None))
        self.pushButton_view.setText(QCoreApplication.translate("MainWindow", u"View", None))
        self.pushButton_add.setText(QCoreApplication.translate("MainWindow", u"Add", None))
        self.pushButton_filter.setText(QCoreApplication.translate("MainWindow", u"Filter", None))
        self.pushButton_delete.setText(QCoreApplication.translate("MainWindow", u"Delete", None))
        self.pushButton_report.setText(QCoreApplication.translate("MainWindow", u"Report", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"Menu", None))
        self.menuFunction.setTitle(QCoreApplication.translate("MainWindow", u"Function", None))
    # retranslateUi

