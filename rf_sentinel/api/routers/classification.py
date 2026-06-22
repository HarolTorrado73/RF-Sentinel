"""Router de clasificación."""

from fastapi import APIRouter, Depends

from rf_sentinel.api.dependencies import get_classifier
from rf_sentinel.api.schemas import SignalResponse

router = APIRouter(prefix="/classify", tags=["classification"])


@router.post("", response_model=SignalResponse)
async def classify_signal(
    frequency: float,
    bandwidth: float,
    power: float,
    classifier= Depends(get_classifier),  # noqa: B008
) -> SignalResponse:
    result = classifier.classify(
        {"frequency": frequency, "bandwidth": bandwidth, "power": power}
    )
    return SignalResponse(
        id=1,
        frequency=frequency,
        bandwidth=bandwidth,
        power=power,
        modulation=result.get("modulation", "Unknown"),
        classification=result.get("type", "Unknown"),
        confidence=result.get("confidence", 0.0),
    )
