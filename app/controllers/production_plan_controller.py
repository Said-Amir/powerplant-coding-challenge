from fastapi import APIRouter, HTTPException
from app.models.payload import Payload
from app.services.production_plan_service import ProductionPlanService

router = APIRouter()

@router.post("/productionplan", response_model=list)
async def production_plan(payload: Payload):
    try:
        service = ProductionPlanService(payload.powerplants, payload.fuels, payload.load)
        production_plan = service.generate_production_plan()
        return production_plan
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
