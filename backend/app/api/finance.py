from fastapi import APIRouter, HTTPException

from app.schemas import PropertyValuationRequest, PropertyValuationResponse
from app.services.property_valuation import calculate_property_valuation

router = APIRouter(prefix="/api/finance", tags=["finance"])


@router.post("/property/valuation", response_model=PropertyValuationResponse)
async def get_property_valuation(req: PropertyValuationRequest) -> PropertyValuationResponse:
    try:
        return calculate_property_valuation(req.graph, req.district)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e
