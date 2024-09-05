import unittest
from unittest.mock import patch
from app.models.payload import Fuels
from app.models.powerplant import PowerPlant
from app.services.production_plan_service import ProductionPlanService

class TestProductionPlanService(unittest.TestCase):

    def setUp(self):
        # Setup common test data
        self.fuels = Fuels(
            gas=13.4,
            kerosine=50.8,
            co2=20.0,
            wind=60.0
        )
        
        self.powerplants = [
            PowerPlant(name="windpark1", type="windturbine", efficiency=1.0, pmin=0, pmax=150),
            PowerPlant(name="windpark2", type="windturbine", efficiency=1.0, pmin=0, pmax=36),
            PowerPlant(name="gasfiredbig1", type="gasfired", efficiency=0.53, pmin=100, pmax=460),
            PowerPlant(name="gasfiredbig2", type="gasfired", efficiency=0.53, pmin=100, pmax=460),
            PowerPlant(name="gasfiredsomewhatsmaller", type="gasfired", efficiency=0.37, pmin=40, pmax=210),
            PowerPlant(name="tj1", type="turbojet", efficiency=0.3, pmin=0, pmax=16)
        ]

    def test_successful_production_plan(self):
        service = ProductionPlanService(self.powerplants, self.fuels, load=910)
        result = service.generate_production_plan()
        
        expected = [
            {
                "name": "windpark1",
                "p": 90.0
            },
            {
                "name": "windpark2",
                "p": 21.6
            },
            {
                "name": "gasfiredbig1",
                "p": 460.0
            },
            {
                "name": "gasfiredbig2",
                "p": 338.4
            },
            {
                "name": "gasfiredsomewhatsmaller",
                "p": 0.0
            },
            {
                "name": "tj1",
                "p": 0.0
            }
        ]
        
        self.assertEqual(result, expected)

    def test_insufficient_capacity(self):
        service = ProductionPlanService(self.powerplants, self.fuels, load=2000)
        
        with self.assertRaises(ValueError) as context:
            service.generate_production_plan()
        
        self.assertEqual(str(context.exception), "Insufficient capacity to meet the load requirement")

    def test_zero_load(self):
        service = ProductionPlanService(self.powerplants, self.fuels, load=0)
        result = service.generate_production_plan()
        
        expected = [
            {"name": "windpark1", "p": 0.0},
            {"name": "windpark2", "p": 0.0},
            {"name": "gasfiredbig1", "p": 0.0},
            {"name": "gasfiredbig2", "p": 0.0},
            {"name": "gasfiredsomewhatsmaller", "p": 0.0},
            {"name": "tj1", "p": 0.0}
        ]
        
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
