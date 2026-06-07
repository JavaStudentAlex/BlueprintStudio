from fastapi import APIRouter

from app.schemas import FuseRequest, FuseResponse
from app.services.fusion import fuse_graphs

router = APIRouter(prefix="/api/fusion", tags=["fusion"])


@router.post("", response_model=FuseResponse)
async def fuse_endpoint(request: FuseRequest) -> FuseResponse:
    fused, warnings = fuse_graphs(request.architecture, request.mep)
    return FuseResponse(fused_graph=fused, warnings=warnings)
