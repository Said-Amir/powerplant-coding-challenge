import unittest
from app.models.payload import Payload, Fuels
from app.models.powerplant import PowerPlant

class TestFuelsModel(unittest.TestCase):

    def test_valid_fuels(self):
        fuels = Fuels(
            gas=50.0,
            kerosine=80.0,
            co2=20.0,
            wind=30.0
        )
        self.assertEqual(fuels.gas, 50.0)
        self.assertEqual(fuels.kerosine, 80.0)
        self.assertEqual(fuels.co2, 20.0)
        self.assertEqual(fuels.wind, 30.0)

    def test_negative_fuel_values(self):
        with self.assertRaises(ValueError):
            Fuels(
                gas=-50.0,
                kerosine=80.0,
                co2=20.0,
                wind=30.0
            )

class TestPayloadModel(unittest.TestCase):

    def setUp(self):
        self.valid_payload = Payload(
            load=1000.0,
            fuels=Fuels(
                gas=50.0,
                kerosine=80.0,
                co2=20.0,
                wind=30.0
            ),
            powerplants=[
                PowerPlant(name="windpark1", type="windturbine", efficiency=1.0, pmin=0, pmax=100)
            ]
        )

    def test_valid_payload(self):
        payload = self.valid_payload
        self.assertEqual(payload.load, 1000.0)
        self.assertIsInstance(payload.fuels, Fuels)
        self.assertEqual(len(payload.powerplants), 1)

    def test_negative_load(self):
        with self.assertRaises(ValueError, msg='Load must be non-negative'):
            Payload(
                load=-1000.0,
                fuels=self.valid_payload.fuels,
                powerplants=self.valid_payload.powerplants
            )

    def test_invalid_powerplants(self):
        with self.assertRaises(ValueError, msg=('Powerplants list must not be empty')):
            Payload(
                load=1000.0,
                fuels=self.valid_payload.fuels,
                powerplants=[]
            )

if __name__ == '__main__':
    unittest.main()
