from adapters.database.score_model import ScoreModel
from domain.models.score import Score


def score_entity_to_model(score: Score) -> ScoreModel:
    """Map Score domain entity to SQLAlchemy ScoreModel."""
    return ScoreModel(
        id=score.id,
        offer_id=score.offerId,
        size=score.size,
        offer=score.offer,
        bag_cost=score.bagCost,
        utility=score.utility,
        created_at=score.createdAt,
    )


def score_model_to_entity(model: ScoreModel) -> Score:
    """Map SQLAlchemy ScoreModel to Score domain entity."""
    return Score(
        id=model.id,
        offerId=model.offer_id,
        size=model.size,
        offer=model.offer,
        bagCost=model.bag_cost,
        utility=model.utility,
        createdAt=model.created_at,
    )
