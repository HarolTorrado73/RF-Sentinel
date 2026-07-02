"""Router de clasificación."""

from fastapi import APIRouter, Depends

from rf_sentinel.api.dependencies import get_classifier
from rf_sentinel.api.schemas import ClassificationRequest, SignalResponse
from rf_sentinel.classification.base import Classifier

router = APIRouter(prefix="/classify", tags=["classification"])


@router.post("", response_model=SignalResponse)
async def classify_signal(
    request: ClassificationRequest,
    classifier: Classifier = Depends(get_classifier),  # noqa: B008
) -> SignalResponse:
    result = classifier.classify(
        {
            "frequency": request.frequency,
            "bandwidth": request.bandwidth,
            "power": request.power,
        }
    )
    return SignalResponse(
        id=1,
        frequency=request.frequency,
        bandwidth=request.bandwidth,
        power=request.power,
        modulation=result.get("modulation", "Unknown"),
        classification=result.get("type", "Unknown"),
        confidence=result.get("confidence", 0.0),
    )
