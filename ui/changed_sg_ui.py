# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'changed_sg_ui.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1002, 437)
        font = QFont()
        font.setPointSize(11)
        MainWindow.setFont(font)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.comboBox = QComboBox(self.centralwidget)
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.addItem("")
        self.comboBox.setItemText(0, "Select project")
        self.comboBox.setCurrentIndex(0)

        self.verticalLayout.addWidget(self.comboBox)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.task_list_listWidget = QListWidget(self.centralwidget)
        self.task_list_listWidget.setObjectName(u"task_list_listWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.task_list_listWidget.sizePolicy().hasHeightForWidth())
        self.task_list_listWidget.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.task_list_listWidget)

        self.task_details_treeWidget = QTreeWidget(self.centralwidget)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, f"Paths")
        self.task_details_treeWidget.setHeaderItem(__qtreewidgetitem)

        self.work_path = QTreeWidgetItem(self.task_details_treeWidget)
        self.work_path.setText(0, "Work Path")

        self.publish_path = QTreeWidgetItem(self.task_details_treeWidget)
        self.publish_path.setText(0, "Publish Path")

        self.task_details_treeWidget.setFont(font)


        self.horizontalLayout.addWidget(self.task_details_treeWidget)


        self.verticalLayout.addLayout(self.horizontalLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1002, 26))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
    # retranslateUi

