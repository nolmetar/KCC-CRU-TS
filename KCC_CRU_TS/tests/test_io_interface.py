from unittest import TestCase
from KCC_CRU_TS.io_interface import IOInterface


class TestIOInterface(TestCase):
    def setUp(self):
        self.io = IOInterface()


class TestInit(TestIOInterface):
    def test_initial_data_size(self):
        self.assertEqual(self.io.get_data_size(), 0)
