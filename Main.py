import os
import sys
from pprint import pprint

from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from ui.changed_sg_ui import Ui_MainWindow
from src.ShotgunCon import ShotgunCon
from src.get_path import GetPaths

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        # QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.setWindowIcon(QIcon('{}/icons/shotgun.png'.format(CURRENT_PATH)))

        self.sg = ShotgunCon()
        self.user = 'alam'

        project_details = self.sg.get_projects(user_name=self.user)

        self.last_publish = None
        self.recent_version = None
        self.total_versions = 0
        self.total_publishes = 0
        self.task_id = None
        self.proj_id = None

        k = 1
        for proj in project_details:
            self.comboBox.addItem("")
            self.comboBox.setItemText(k, proj['name'])
            self.comboBox.setItemData(k, proj['id'])
            k += 1

        self.comboBox.activated.connect(self.display_tasks)
        self.task_list_listWidget.itemClicked.connect(self.get_selected_task)

    def display_tasks(self):
        """
        Display all the tasks belonging to a user that are active for each projects
        :return:
        """
        if self.comboBox.currentData() == None:
            QMessageBox.information(self, "Message", f"Please Select a Project first")
            return

        self.task_list_listWidget.clear()
        self.task_details_treeWidget.clear()
        self.proj_id = self.comboBox.currentData()
        sg_data = self.sg.find_active_task(self.comboBox.currentData(), user_name=self.user)
        # pprint(sg_data)
        for task in sg_data:

            # Creates a QListWidgetItem
            prj_name = self.comboBox.currentText()
            shot_name = None
            item_to_add = QListWidgetItem()

            entity = task.get('entity')
            if entity:
                shot_name = entity.get('name')

            # project = i.get('project')
            # if project:
            #     prj_name = project.get('name')
            # Setting your QListWidgetItem Text

            field_name = '{0}_{1}_{2}'.format(prj_name, shot_name, task.get('content'))
            item_to_add.setText(field_name)

            # Setting your QListWidgetItem Data
            item_to_add.setData(Qt.UserRole, task)

            # Add the new rule to the QListWidget
            self.task_list_listWidget.addItem(item_to_add)

            self.task_list_listWidget.setContextMenuPolicy(Qt.CustomContextMenu)
            self.task_list_listWidget.customContextMenuRequested.connect(self.open_context)

    def open_context(self, position):
        item = self.task_list_listWidget.itemAt(position)
        react = self.task_list_listWidget.visualItemRect(item)
        if item is not None:

            context_menu = QMenu(self)

            open_version = QAction("Open Current Version", self)
            context_menu.addAction(open_version)
            open_version.triggered.connect(lambda: self.open_file(self.recent_version))

            open_publish = QAction("Open Last Publish", self)
            context_menu.addAction(open_publish)
            open_publish.triggered.connect(lambda: self.open_file(self.last_publish))

            context_menu.exec_(self.task_list_listWidget.mapToGlobal(react.center()))

    def open_file(self, path):
        """
        opens the file in path
        """
        try:
            os.startfile(path)
        except Exception as e:
            QMessageBox.information(self, "Message", f"Unable to open file")

    def get_selected_task(self, data):
        """
        get the path details of the selected tasks
        :param data:
        :return:
        """
        item_data = data.data(Qt.UserRole)
        self.task_id = item_data.get('id')
        self.path_cls = GetPaths('C:/Users/s8/OneDrive - Autodesk/Desktop/checking')
        paths = self.path_cls.get_scene_path(item_data)

        self.task_details_treeWidget.clear()
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, f"Paths")
        self.task_details_treeWidget.setHeaderItem(__qtreewidgetitem)

        self.work_path = QTreeWidgetItem(self.task_details_treeWidget)
        self.work_path.setText(0, "Work Path")

        self.publish_path = QTreeWidgetItem(self.task_details_treeWidget)
        self.publish_path.setText(0, "Publish Path")

        if paths[0]:
            paths[0].sort(reverse=True)
            for path in paths[0]:
                child_item_1 = QTreeWidgetItem(self.work_path)
                child_item_1.setText(0, f"{path}")
            self.recent_version = paths[0][0]
            self.total_versions = len(paths[0])

        if paths[1]:
            paths[1].sort(reverse=True)
            for path in paths[1]:
                child_item_2 = QTreeWidgetItem(self.publish_path)
                child_item_2.setText(0, f"{path}")
            self.total_publishes = len(paths[1])
            self.last_publish = paths[1][0]

        self.task_details_treeWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.task_details_treeWidget.customContextMenuRequested.connect(self.save_version_context)

    def save_version_context(self, position):
        """
        context menu for creating a new version
        :param position: position of the click
        :return:
        """
        item = self.task_details_treeWidget.itemAt(position)
        if item.text(0) == 'Work Path':
            context_menu = QMenu(self)
            save_action = QAction("Create New Version", self)
            context_menu.addAction(save_action)
            save_action.triggered.connect(self.new_version)
            context_menu.exec_(self.task_details_treeWidget.mapToGlobal(position))

        if item.text(0) == 'Publish Path':
            context_menu = QMenu(self)
            publish_action = QAction("Publish Last Version", self)
            context_menu.addAction(publish_action)
            publish_action.triggered.connect(self.publish_version)
            context_menu.exec_(self.task_details_treeWidget.mapToGlobal(position))

        if item.parent() == self.publish_path or item.parent() == self.work_path:
            context_menu = QMenu(self)
            open_file = QAction("Open", self)
            context_menu.addAction(open_file)
            open_file.triggered.connect(lambda: self.open_file(item.text(0)))
            context_menu.exec_(self.task_details_treeWidget.mapToGlobal(position))



    def publish_version(self):
        file_name = 'example_publish'
        publish = self.total_publishes+1
        #if publish == 1:
            #os.makedirs(self.path_cls.publish_path)
        print(self.recent_version)
        types = self.recent_version.split('.')
        name = "{}_v{:03d}.{}".format(file_name, publish, types[len(types)-1])
        path = os.path.join(self.path_cls.publish_path, name)
        self.last_publish = path
        with open(self.recent_version, 'rb') as source_file, open(path, 'wb') as destination_file:
            # Read and write in chunks to handle large files efficiently
            chunk_size = 1024  # You can adjust the chunk size as needed
            while True:
                chunk = source_file.read(chunk_size)
                if not chunk:
                    break
                destination_file.write(chunk)
        # with open(self.recent_version, "r") as file:
        #     file_data = file.read()
        # print(file_data)
        # with open(path, "w") as file:
        #     file.write(file_data)
        self.sg.publish_tosg(name, path, self.task_id, self.proj_id)
        #pass

    def new_version(self):
        """
        function to create a new version file
        :return:
        """
        file_name = 'example'
        version = self.total_versions+1
        if version == 1:
            os.makedirs(self.path_cls.scene_path)
        name = "{}_v{:03d}.txt".format(file_name, version)
        path = os.path.join(self.path_cls.scene_path, name)
        with open(path, "w") as file:
            file.write("demo\n")


if __name__ == '__main__':
    import qdarkstyle as qdarkstyle

    app = QApplication()
    mainWindow = MainWindow()
    mainWindow.show()
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyside2())
    sys.exit(app.exec_())
