from unittest import TestCase


class TestScore(TestCase):
    """"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def assert_template(self, result_path, template_path=None):
        if not template_path:
            template_path = result_path + '_template.xml'
        with open(template_path, 'r') as myfile:
            template = myfile.read()
        result_path = result_path + '.xml'
        with open(result_path, 'r') as myfile:
            result = myfile.read()
        self.assertEqual(template, result)
