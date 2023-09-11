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
        # setting the username manually
        self.user = 'alam'

        project_details = self.sg.get_projects(user_name=self.user)

        self.last_publish = None
        self.total_publishes = 0

        self.recent_version = None
        self.total_versions = 0

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
        self.work_path.clear()
        self.publish_path.clear()

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
        """
        opens a context menu at the position of click with open current version and open last publish
        :param position:
        :return:
        """
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
        opens the file in path if path exits
        """
        if path is not None:
            try:
                os.startfile(path)
            except Exception as e:
                QMessageBox.information(self, "Message", f"Unable to open file")
        else :
            QMessageBox.information(self, "Message", f"No file Found")

    def get_selected_task(self, data):
        """
        get the path details of the selected tasks
        :param data:
        :return:
        """
        item_data = data.data(Qt.UserRole)
        self.task_id = item_data.get('id')

        # setting the path manually
        self.path_cls = GetPaths('C:/Users/s8/OneDrive - Autodesk/Desktop/Publish')

        paths = self.path_cls.get_scene_path(item_data)

        self.work_path.clear()
        self.publish_path.clear()

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
            publish_action = QAction("Publish current Version", self)
            context_menu.addAction(publish_action)
            publish_action.triggered.connect(self.publish_version)
            context_menu.exec_(self.task_details_treeWidget.mapToGlobal(position))

        if item.parent() in [self.publish_path, self.work_path]:
            context_menu = QMenu(self)
            open_file = QAction("Open", self)
            context_menu.addAction(open_file)
            open_file.triggered.connect(lambda: self.open_file(item.text(0)))
            context_menu.exec_(self.task_details_treeWidget.mapToGlobal(position))

    def new_version(self):
        """
        function to create a new version file
        :return:
        """
        file_type = 'txt'
        file_name = 'example'
        version = self.total_versions+1
        if version == 1:
            os.makedirs(self.path_cls.scene_path)
        name = "{}_v{:03d}.{}".format(file_name, version, file_type)
        path = os.path.join(self.path_cls.scene_path, name)
        with open(path, "w") as file:
            file.write("demo\n")

    def publish_version(self):
        file_name = 'demo_publish'
        publish = self.total_publishes+1
        if publish == 1:
            os.makedirs(self.path_cls.publish_path)
        #print(self.recent_version)
        file_type = self.recent_version.split('.')
        name = "{}_pv{:03d}.{}".format(file_name, publish, file_type[len(file_type)-1])
        path = os.path.join(self.path_cls.publish_path, name)
        self.last_publish = path
        with open(self.recent_version, 'rb') as source_file, open(path, 'wb') as destination_file:

            chunk_size = 1024
            while True:
                chunk = source_file.read(chunk_size)
                if not chunk:
                    break
                destination_file.write(chunk)
        details = {
            'name': name,
            'path': path,
            'task_id': self.task_id,
            'project_id': self.proj_id
        }
        self.sg.publish_tosg(details)


if __name__ == '__main__':
    import qdarkstyle as qdarkstyle

    app = QApplication()
    mainWindow = MainWindow()
    mainWindow.show()
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyside2())
    sys.exit(app.exec_())
