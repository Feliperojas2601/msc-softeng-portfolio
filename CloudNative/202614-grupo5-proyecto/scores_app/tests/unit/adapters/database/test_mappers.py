from adapters.database.mappers import score_entity_to_model, score_model_to_entity


def test_score_entity_to_model_maps_every_field(existing_score):
    model = score_entity_to_model(existing_score)

    assert model.id == existing_score.id
    assert model.offer_id == existing_score.offerId
    assert model.size == existing_score.size
    assert model.offer == existing_score.offer
    assert model.bag_cost == existing_score.bagCost
    assert model.utility == existing_score.utility
    assert model.created_at == existing_score.createdAt


def test_score_model_to_entity_maps_every_field(existing_score):
    model = score_entity_to_model(existing_score)
    entity = score_model_to_entity(model)

    assert entity == existing_score
