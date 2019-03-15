from unittest import TestCase


class TestScore(TestCase):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def assert_template(self, path_):
        template_path = path_ + '_template.xml'
        with open(template_path, 'r') as myfile:
            template = myfile.read()
        result_path = path_ + '.xml'
        with open(result_path, 'r') as myfile:
            result = myfile.read()
        self.assertEqual(template, result)
