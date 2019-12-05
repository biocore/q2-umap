import unittest
import pkg_resources
import os
import shutil


class TestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.to_remove = []

    def get_data_path(self, filename):
        # adapted from qiime2.plugin.testing.TestPluginBase and biocore/unifrac
        return pkg_resources.resource_filename(self.package,
                                               'data/%s' % filename)

    def create_data_path(self, filename):
        file_path = self.get_data_path(filename)
        dir_path = os.path.split(file_path)[0]
        self.to_remove.append(file_path)
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)
            self.to_remove.append(dir_path)
        return file_path

    def tearDown(self) -> None:
        for path in self.to_remove:
            if os.path.isfile(path):
                os.remove(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)
