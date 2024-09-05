# app/main.py
from fastapi import FastAPI, HTTPException
from app.models.payload import Payload
from app.services.production_plan_service import ProductionPlanService
import logging

logger = logging.getLogger(__name__)

app = FastAPI()

@app.post("/productionplan")
async def create_production_plan(payload: Payload):
    try:
        # Convert Payload to the appropriate data types
        service = ProductionPlanService(
            powerplants=payload.powerplants,  # Should already be PowerPlant instances if properly defined
            fuels=payload.fuels,
            load=payload.load
        )
        production_plan = service.generate_production_plan()
        return production_plan
    except ValueError as e:
        logger.error(f"ValueError: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
