from adapters.database.mappers import offer_entity_to_model, offer_model_to_entity


def test_offer_entity_to_model_maps_every_field(existing_offer):
    model = offer_entity_to_model(existing_offer)

    assert model.id == existing_offer.id
    assert model.post_id == existing_offer.postId
    assert model.user_id == existing_offer.userId
    assert model.description == existing_offer.description
    assert model.size == existing_offer.size
    assert model.fragile == existing_offer.fragile
    assert model.offer == existing_offer.offer
    assert model.created_at == existing_offer.createdAt


def test_offer_model_to_entity_maps_every_field(existing_offer):
    model = offer_entity_to_model(existing_offer)
    entity = offer_model_to_entity(model)

    assert entity == existing_offer
