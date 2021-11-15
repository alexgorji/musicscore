from unittest import TestCase

from common.helpers import _check_type, _check_types, _check_permitted_value


class TestHelpers(TestCase):
    def test_check_type(self):
        """
        value is None and none is False
        """
        with self.assertRaises(TypeError):
            _check_type('some_value', None, type_=int, none=False)
        """
        value is None and none is True
        """
        _check_type('some_value', None, type_=int, none=True)
        """
        value is of wrong type
        """
        with self.assertRaises(TypeError):
            _check_type('some_value', 5.4, type_=int)
        """
        value is of right type
        """
        _check_type('some_value', 5.4, type_=float)

    def test_check_types(self):
        """
        values is None and none is False
        """
        with self.assertRaises(TypeError):
            _check_types('some_value', None, types=(int,), none=False)

        """
        values is None and none is True
        """
        _check_types('some_value', None, types=(int,), none=True)
        """
        values is strings
        """
        with self.assertRaises(TypeError):
            _check_types('some_value', 'None', types=(int,))
        """
        values has no __iter__
        """
        with self.assertRaises(TypeError):
            _check_types('some_value', 1, types=(int,))

        """
        values has wrong type
        """
        with self.assertRaises(TypeError):
            _check_types('some_value', [1, 'str'], types=(int,))

        """
        values has the right type
        """
        _check_types('some_value', [1, 2, 3], types=(int,))

        """
        values has the right types
        """
        _check_types('some_value', [1, 2, 3, '5.5'], types=(int, str,))

    def test_check_permitted_value(self):
        permitted_values = [1, 2, 3, 'o']
        _check_permitted_value('some_value', 3, permitted_values)
        _check_permitted_value('some_value', 'o', permitted_values)
        with self.assertRaises(ValueError):
            _check_permitted_value('some_value', 4, permitted_values)
