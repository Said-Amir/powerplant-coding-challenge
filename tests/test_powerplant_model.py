import unittest
from app.models.powerplant import PowerPlant

class TestPowerPlantModel(unittest.TestCase):

    def test_valid_powerplant(self):
        plant = PowerPlant(
            name="gasfiredbig1",
            type="gasfired",
            efficiency=0.9,
            pmin=200,
            pmax=500
        )
        self.assertEqual(plant.name, "gasfiredbig1")
        self.assertEqual(plant.type, "gasfired")
        self.assertEqual(plant.efficiency, 0.9)
        self.assertEqual(plant.pmin, 200)
        self.assertEqual(plant.pmax, 500)

    def test_negative_values(self):
        with self.assertRaises(ValueError):
            PowerPlant(
                name="gasfiredbig1",
                type="gasfired",
                efficiency=-0.9,
                pmin=-200,
                pmax=-500
            )

    def test_pmax_less_than_pmin(self):
        with self.assertRaises(ValueError):
            PowerPlant(
                name="gasfiredbig1",
                type="gasfired",
                efficiency=0.9,
                pmin=300,
                pmax=200
            )

if __name__ == '__main__':
    unittest.main()
