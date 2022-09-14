from unittest import TestCase
from KCC_CRU_TS.io_interface import IOInterface


class TestIOInterface(TestCase):
    def setUp(self):
        self.io = IOInterface()


class TestInit(TestIOInterface):
    def test_initial_data_size(self):
        self.assertEqual(self.io.get_data_size(), 0)


class TestRead(TestIOInterface):
    def test_data_read(self):
        size = self.io.get_data_size()
        self.io.import_data({"tmp": "../../DATA/cru_ts4.06.1901.2021.tmp.dat.nc"})
        self.assertEqual(self.io.get_data_size(), size+1)
        self.assertNotEqual(self.io.get_data_size(), size)

    def test_data_read_multiple(self):
        size = self.io.get_data_size()
        data = {
            "1": "../../DATA/cru_ts4.06.1901.2021.tmp.dat.nc",
            "2": "../../DATA/cru_ts4.06.1901.2021.tmp.dat.nc",
            "3": "../../DATA/cru_ts4.06.1901.2021.tmp.dat.nc",
            "4": "../../DATA/cru_ts4.06.1901.2021.tmp.dat.nc"
        }
        self.io.import_data(data)
        self.assertEqual(self.io.get_data_size(), size+4)
        self.assertNotEqual(self.io.get_data_size(), size)
