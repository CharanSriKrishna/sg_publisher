import os

class GetPaths:
    def __init__(self, path):
        self.root_path = path

    def get_scene_path(self, shot_data):
        """

        :return:
        """
        prj_code = None
        seq_name = None
        shot_name = None
        step_name = None
        prj = shot_data.get('project')
        if prj:
            prj_code = prj.get('name')
        sequence = shot_data.get('entity.Shot.sg_sequence')
        if sequence:
            seq_name = sequence.get('name')
        entity = shot_data.get('entity')
        if entity:
            shot_name = entity.get('name')
        step = shot_data.get('step')
        if step:
            step_name = step.get('name')

        print(self.root_path, prj_code, seq_name, shot_name, step_name)
        self.scene_path = '{0}/{1}/sequences/{2}/{3}/{4}/work/silhouette/'.format(self.root_path, prj_code, seq_name,
                                                                             shot_name, step_name)
        self.publish_path = '{0}/{1}/sequences/{2}/{3}/{4}/publish/silhouette/'.format(self.root_path, prj_code, seq_name,
                                                                             shot_name, step_name)
        #return self.scene_path
        return [self.get_all_files(self.scene_path), self.get_all_files(self.publish_path)]

    def get_all_files(self, path):
        """
        Function to get all the versions
        :param path:
        :return:
        """
        all_files = []
        for root, dirs, files in os.walk(path):
            #print(root, dirs, files)
            for file in files:
                file_path = os.path.join(root, file)
                all_files.append(file_path)
        return all_files