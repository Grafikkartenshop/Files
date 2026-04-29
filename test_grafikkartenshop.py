import unittest
from unittest.mock import patch, MagicMock
from grafikkartenshop import Grafikkartenshop
from grafikkarte import Grafikkarte

class TestGrafikkartenshop(unittest.TestCase):

    @patch('grafikkartenshop.DatabaseManager')
    def test_grafikkarteEinkaufen_erfolgreich(self, MockDB):
        db_instance = MockDB.return_value
        db_instance.get_shop_data.return_value = {
            'shopID': 1, 'name': 'TestShop', 'umsatz': 0, 'budget': 1000
        }
        db_instance.get_all_gpus.return_value = []
        
        shop = Grafikkartenshop(1)
        test_gpu = Grafikkarte("RTX 4090", "NVIDIA", "ASUS", 24, "GDDR6X", 500, 1000)
        test_gpu.setArtikelNr(123)
        test_gpu.setBestand(5)
        shop._Grafikkartenshop__alleGrafikkarten = [test_gpu]
        erfolg = shop.grafikkarteEinkaufen(123, 1)
        self.assertTrue(erfolg)
        self.assertEqual(shop.getBudget(), 500)
        db_instance.execute_query.assert_called()

if __name__ == '__main__':
    unittest.main()