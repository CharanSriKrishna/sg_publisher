from shotgun_api3.shotgun import Shotgun
import getpass


class ShotgunCon:
    def __init__(self):
        self.__sg = Shotgun(
            'https://samit.shotgunstudio.com',
        )


    def get_projects(self, user_name=getpass.getuser()):
        """
        Get the projects that the user is part of
        :param user_name:name of the user
        :return:
        """
        user_id = self.get_shotgun_user_id(user_name)['id']
        proj_fields = ['name', 'id']
        proj_filter = [
            ["is_demo", "is_not", True],
            ['is_template', 'is_not', True],
            ["users", "in", {"type": "HumanUser", "id": user_id}],
        ]

        projects = self.__sg.find('Project', proj_filter, proj_fields)
        return projects

    def get_shotgun_user_id(self, user_name=getpass.getuser()):
        """
        function to get the user id from the username
        :param user_name:
        :return:
        """
        filers = [
            ['login', 'is', user_name]
        ]
        fields = ['id']
        return self.__sg.find_one('HumanUser', filers, fields)

    def find_active_task(self, project_id, user_name=getpass.getuser(),):
        """
        find all the tasks that are active for that user
        :param user_name:
        :return:
        """
        user_id = self.get_shotgun_user_id(user_name)['id']
        task_status_list = ['wtg', 'rdy', 'ip', 'rev', 'yts', 'fr']
        filters = [
            ['project', 'is', {'type': 'Project', 'id': project_id}],
            ['sg_status_list', 'in', task_status_list],
            ['task_assignees.HumanUser.id', 'is', user_id],
        ]

        fields = [
            'content', 'step', 'sg_status_list', 'task_assignees', 'start_date', 'due_date', 'entity', 'project',
            'entity.Shot.sg_sequence'
        ]
        active_task_data = self.__sg.find('Task', filters, fields)
        return active_task_data

    def publish_tosg(self, details):
        """
        code to publish the file to the shotgrid webpage
        :param details:
        :return:
        """
        Publish_data = {
            'code': details['name'].split('.')[0],
            'name': details['name'],
            "task": {"type": "Task", "id": details['task_id']},
            'project': {'type': 'Project', 'id': details['project_id']}
        }
        new_publish = self.__sg.create("PublishedFile", Publish_data)
        self.__sg.upload("PublishedFile", new_publish["id"], details['path'], field_name="path")
        print(new_publish)
        print("published")


if __name__ == '__main__':
    obj = ShotgunCon()
    print(obj.get_shotgun_user_id('baigalam2359@gmail.com'))
