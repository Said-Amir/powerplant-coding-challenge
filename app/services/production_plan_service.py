# app/services/production_plan_service.py
import logging
from typing import List, Dict
from app.models.powerplant import PowerPlant
from app.models.payload import Fuels

logger = logging.getLogger(__name__)


class ProductionPlanService:
    def __init__(self, powerplants: List[PowerPlant], fuels: Fuels, load: float):
        self.powerplants = powerplants
        self.fuels = fuels
        self.load = load

    def generate_production_plan(self) -> List[Dict[str, float]]:

        # Sort powerplants by cost-effectiveness (merit order)
        sorted_powerplants = self._sort_powerplants_by_cost()

        remaining_load = self.load
        all_plants_dict = {plant.name: {'name': plant.name, 'p': 0.0, 'cost_per_mwh': 0.0} for plant in self.powerplants}

        # Proceed with other plants, making sure to respect pmin and pmax
        for index, plant in enumerate(sorted_powerplants):
            if remaining_load <= 0:
                break

            effective_pmax = plant.pmax
            if plant.type == 'windturbine':
                effective_pmax = plant.pmax * (self.fuels.wind / 100)
                
            # Ensure we don't use more power than needed and respect pmin
            power_to_generate = min(effective_pmax, remaining_load)

            # Check if we can reach the pmin with a part of the previous powerplant load 
            if power_to_generate < plant.pmin:
                if index >= 1:
                    missing_load = plant.pmin - power_to_generate
                    previous_plant_load = all_plants_dict[sorted_powerplants[index-1].name]['p']
                    if (previous_plant_load - sorted_powerplants[index-1].pmin) > missing_load:
                        all_plants_dict[sorted_powerplants[index-1].name]['p'] -= missing_load
                        all_plants_dict[plant.name]['p'] = round(plant.pmin, 1)
                        all_plants_dict[plant.name]['cost_per_mwh'] = self._calculate_cost_per_mwh(plant)
                        remaining_load = 0
                        break
                    else:
                        continue
                else:
                    continue
            # Adjust power to meet the exact load and respect pmin
            power_to_generate = max(plant.pmin, power_to_generate)

            all_plants_dict[plant.name]['p'] = round(power_to_generate, 1)
            all_plants_dict[plant.name]['cost_per_mwh'] = self._calculate_cost_per_mwh(plant)
            remaining_load -= power_to_generate

        # Convert the dictionary to a list
        final_production_plan = list(all_plants_dict.values())

        # Separate used and unused plants
        used_plants = [plant for plant in final_production_plan if plant['p'] > 0]
        unused_plants = [plant for plant in final_production_plan if plant['p'] == 0]

        used_plants.sort(key=lambda x: x['cost_per_mwh'])

        final_production_plan = used_plants + unused_plants

        # Remove cost_per_mwh from the final output
        for plant in final_production_plan:
            del plant['cost_per_mwh']

        if remaining_load > 0:
            logger.error("Insufficient capacity to meet the load requirement")
            raise ValueError("Insufficient capacity to meet the load requirement")

        return final_production_plan

    def _sort_powerplants_by_cost(self) -> List[PowerPlant]:
        sorted_powerplants = []

        for plant in self.powerplants:
            cost_per_mwh = 0
            if plant.type == 'gasfired':
                cost_per_mwh = self.fuels.gas * (1 / plant.efficiency)
            elif plant.type == 'turbojet':
                cost_per_mwh = self.fuels.kerosine * (1 / plant.efficiency)

            sorted_powerplants.append({
                'name': plant.name,
                'type': plant.type,
                'efficiency': plant.efficiency,
                'pmin': plant.pmin,
                'pmax': plant.pmax,
                'cost_per_mwh': cost_per_mwh
            })

        sorted_powerplants.sort(key=lambda x: x['cost_per_mwh'])

        # Convert dicts back to PowerPlant instances
        return [PowerPlant(**p) for p in sorted_powerplants]

    def _calculate_cost_per_mwh(self, plant: PowerPlant) -> float:
        if plant.type == 'gasfired':
            return self.fuels.gas * (1 / plant.efficiency)
        elif plant.type == 'turbojet':
            return self.fuels.kerosine * (1 / plant.efficiency)
        return 0.0
